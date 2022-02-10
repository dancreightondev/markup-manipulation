from bs4 import BeautifulSoup as BS
import glob
import os as OS
import xml.etree.ElementTree as ET
import pandas as PD

def make_data_frame(qti_filename, img_filenames, audio_filenames, img_count, audio_count):
    
    # Make the data frame according the the provided arguments
    data_frame = PD.DataFrame({"QTI filename" : qti_filename,
                   "Image filename(s) in Media Library" : img_filenames,
                   "Audio file(s) ID" : audio_filenames,
                   "Number of images in item" : img_count,
                   "Number of audio files in item" : audio_count},
                   index=[0])
    
    # Return the data frame
    return data_frame

def get_image_names_from_html_file(html_filename):
    
    # Open the provided HTML file
    with open(html_filename) as html:
        
        # Parse the HTML content
        content = BS(html, features="html.parser")

        # Initialise an array to store image filenames
        filenames = []

        # Iterate through all img objects in the HTML code
        for attr in content.find_all("img"):

            # Store the filename in the src tag for later
            filenames.append(attr["src"].split("/", 1)[-1])

    # Return the list of filenames
    return filenames

def parse_xml_file(xml_filename):
    
    # Parse XML
    tree = ET.parse(xml_filename)
    
    # Get the root of the XML element tree
    root = tree.getroot()

    # Object attribute to search for. The objects that link to a file seem to always have the 'data' attribute
    attr = "data"
    
    # Find all objects by attribute
    objs = root.findall(".//*[@{}]".format(attr))

    # Initialise an array to store filenames
    filenames = []
    
    # Iterate through the found objects
    for o in objs:

        # Get filenames from found objects, as per the specified attribute (attr)
        data = o.attrib[attr]

        # Tidy up the filename
        filename = data.split("/", 1)[-1]

        # Store for processing later
        filenames.append(filename)

    # Store HTML filenames
    html_filenames = [n for n in filenames if n.endswith(".html")]

    # Initialise an array to store image filenames
    img_filenames = []

    # Iterate through the HTML files
    for h in html_filenames:

        # Store image filenames
        img_filenames.extend(get_image_names_from_html_file(h))
    
    # Store MP3 filenames
    audio_filenames = [n for n in filenames if n.endswith(".mp3")]

    # Collate parsed data
    parsed_data = {"QTI filename" : xml_filename,
                  "Image filename(s) in Media Library" : ', '.join(img_filenames),
                  "Audio file(s) ID" : ', '.join(audio_filenames),
                  "Number of images in item" : str(len(img_filenames)),
                  "Number of audio files in item" : str(len(audio_filenames))}

    # Return parsed data
    return parsed_data

def export_to_excel(data_frame, overwrite=False):

    # Set the filename prefix
    prefix = "xml-to-excel.py_output"

    # If overwriting, ...
    if overwrite:
        # Set the filepath
        outfilepath = OS.getcwd() + "\\" + f"{prefix}.xlsx"
    
    # If not overwriting, ...
    else:
        # Set a new filename iteratively so any previous files are not overwritten
        filepaths = glob.glob(f"{prefix}*.xlsx")
        if len(list(filepaths)) == 0:
            outfilepath = OS.getcwd() + "\\" + f"{prefix}.xlsx"
        else:
            outfilepath = OS.getcwd() + "\\" + f"{prefix}{len(list(filepaths))+1}.xlsx"

    # Export to an Excel file
    data_frame.to_excel(outfilepath, index=False)

    # Return the filepath it was saved to
    return outfilepath

def main():
    
    # Initialise an array to store the data to go in the spreadsheet
    sheet_data = [] 
    
    # Attempt to parse the files
    try:
        print("Parsing files")

        # Iterate through the files in the current directory
        for file in OS.listdir(OS.getcwd()):

            # Only look at the XML files
            if not file.endswith('.xml'): 
                continue

            # Parse the XML file and extract the data we need
            parsed_data = parse_xml_file(file)

            # Save the data we need ready for export
            sheet_data.append(parsed_data)

    # Error handling     
    except Exception as e:
        print(e)
    except:
        print("An unknown error occurred")

    # Print success message if no errors occurred
    else:
        print("Parsed all files successfully")
    
    # Attempt to export to Excel
    try:
        print("Exporting to a new Excel file")

        # Export the data to an Excel spreadsheet
        export_to_excel(PD.DataFrame(sheet_data))

    # Error handling
    except Exception as e:
        print(e)
    except:
        print("An unknown error occurred")
    
    # Print success message if no errors occurred
    else:
        print("Exported successfully")

print(f"This program will look for files in the current directory:\n\n{str(OS.getcwd())}\n")
confirm = input("Confirm? (Y/n): ")
if confirm.upper == "Y":
    print("Starting...\n")
    main()
    input("\nPress any key to continue... ")
