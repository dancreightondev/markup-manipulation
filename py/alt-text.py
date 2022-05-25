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

    # Initialise an array to store parsed data
    parsed_data = []
    
    # Iterate through matching elements
    for element in elements:

        # Get alt text for element
        try:
            alt_text = element.attrib["alt"]
        except:
            alt_text = ""

        # Iterate through element attributes
        attributes.append(element.attrib)
        for attribute in attributes:

            # Iterate through the attributes' values
            for value in attribute.values():

                # Get the image and audio filenames
                if value.startswith('images/'):
                    img_filename = value.split('/', 1)[-1]

                    # Create a data row
                    row = [xml_filename,img_filename,alt_text]

                    # Record the new row
                    parsed_data.append(row)
    
    # Return parsed data
    return parsed_data

def export_to_excel(data_frame, overwrite=False):

    # Set the filename prefix
    prefix = "alt-text.py_output"

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
    
    # Initialise the `DataFrame`
    data = PD.DataFrame(columns=["QTI filename","Image filename in Media Library","Image alt text"])
    
    # Parse the files
    print("Parsing files")

    # Iterate through the files in the current directory
    for file in OS.listdir(OS.getcwd()):

        # Only look at the XML files
        if not file.endswith(".xml"): 
            continue
        # ...that aren't the manifest
        elif file == "imsmanifest.xml":
            continue

        # Parse the XML file and extract the data we need
        parsed_data = parse_xml_file(file)

        # Add a row for each line of the parsed data
        for row in parsed_data:
            data.loc[len(data)] = row

    # Print success message 
    print("Parsed all files successfully")
    
    # Export the data to an Excel spreadsheet
    print("Exporting to a new Excel file")
    export_to_excel(data)
    
    # Print success message
    print("Exported successfully")

print(f"This program will look for files in the current directory:\n\n{str(OS.getcwd())}\n")
confirm = input("Confirm? (Y/n): ")
if confirm.upper() == "Y":
    print("Starting...\n")
    main()
    input("\nPress any key to continue... ")
