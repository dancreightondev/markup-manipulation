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

    # Define image extensions
    img_extensions = (".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".bmp", ".dib", ".heif", ".heic", ".svg", ".svgz", ".eps")

    # Store image filenames
    img_filenames = [i for i in filenames if i.lower().endswith(img_extensions)]
    
    # Store MP3 filenames
    audio_filenames = [n for n in filenames if n.lower().endswith(".mp3")]

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
    
    # Parse the files
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

    # Print success message 
    print("Parsed all files successfully")
    
    # Export the data to an Excel spreadsheet
    print("Exporting to a new Excel file")
    export_to_excel(PD.DataFrame(sheet_data))
    
    # Print success message
    print("Exported successfully")

print(f"This program will look for files in the current directory:\n\n{str(OS.getcwd())}\n")
confirm = input("Confirm? (Y/n): ")
if confirm.upper() == "Y":
    print("Starting...\n")
    main()
    input("\nPress any key to continue... ")