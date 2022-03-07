from bs4 import BeautifulSoup as BS
import glob
import os as OS
from lxml import etree as ET
import pandas as PD

def parse_xml_file(xml_filename):
    
    # Parse XML
    tree = ET.parse(xml_filename, parser=ET.XMLParser(encoding="cp1252"))
    
    # Get the root of the XML element tree
    root = tree.getroot()
    
    # Search for objects with an attribute value containing `images/*` or `audio/*`
    elements = root.xpath(".//*[@*[contains(.,'images/') or contains(.,'audio/')]]")
    
    # Initialise an array to store attributes
    attributes = []

    # Initialise an array to store filenames
    filenames = []
    
    # Iterate through matching elements
    for element in elements:

        # Iterate through their attributes
        attributes.append(element.attrib)
        for attribute in attributes:

            # Iterate through the attributes' values
            for value in attribute.values():

                # Get the image and audio filenames
                if (value.startswith('images/') or value.startswith('audio/')) and (value.lower() != "audio/mp3"):
                    filename = value.split('/', 1)[-1]
                    filenames.append(filename)

    # Define image extensions
    img_extensions = (".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".bmp", ".dib", ".heif", ".heic", ".svg", ".svgz", ".eps")

    # Store image filenames
    img_filenames = [i for i in filenames if i.lower().endswith(img_extensions)]

    # Remove duplicate image filenames
    img_filenames = list(dict.fromkeys(img_filenames))
    
    # Store audio filenames
    audio_filenames = [n for n in filenames if n.lower().endswith(".mp3")]

    # Remove duplicate audio filenames
    audio_filenames = list(dict.fromkeys(audio_filenames))

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
