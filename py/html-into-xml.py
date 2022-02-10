from bs4 import BeautifulSoup as BS
import glob
import os as OS
import sys
import re
import pandas as PD


def find_errant_unicode(string):

    # Define the regular expression to use when parsing
    regex = "&([^;]+);"

    # Parse string for errant unicode
    regex_result = re.findall(regex, string)

    # Return the result
    return regex_result


def wrap_content_with_hashes(html, obj):

    # Create a new tag for the hashes at the beginning
    pre_hashes = html.new_tag("p")
    pre_hashes.string = "###"

    # Insert the tag at the beginning (position 0)
    obj.insert(0, pre_hashes)

    # Create a new tag for the hashes at the end
    end_hashes = html.new_tag("p")
    end_hashes.string = "###"

    # Insert the tag at the end (append it)
    obj.append(end_hashes)
    

def replace_xml_with_html(xml_filename, html_filename):
    
    # Initialise empty strings to store the XML and HTML contents respectively
    xml = ""
    html = ""

    # Read the XML contents
    with open(xml_filename, mode="r", encoding="cp1252") as xf:
        xml_contents = xf.read()
        xml = BS(xml_contents, "xml")

        # While doing so, search the source for errant unicode for later auditing
        xml_u = find_errant_unicode(xml_contents)

    # Read the HTML contents
    with open(html_filename, mode="r", encoding="cp1252") as hf:
        html_contents = hf.read()
        html = BS(html_contents, "xml")

        # While doing so, search the source for errant unicode for later auditing
        html_u = find_errant_unicode(html_contents)
        u = xml_u + html_u

    # Find the appropriate content to replace (XML object with attribute type="text/html")
    obj_to_replace = xml.find(attrs={"type" : "text/html"})

    # Edit HTML to add hashes either side of the content
    # (this is specific to the intended use of this program but is not required for it to run - delete this section or comment it out if it's not needed for you)
    wrap_content_with_hashes(html, html.find("div"))

    # Replace HTML reference with HTML code in the XML file
    obj_to_replace.replaceWith(html)

    # Return the modified & prettified XML
    return xml, u


def export_to_excel(data_frame, overwrite=False):

    # Set the filename prefix
    prefix = "html-into-xml.py_output"

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

    # Initialise a DataFrame so data can be exported to Excel
    headings = ["Filename", "Comment(s)", "Errant unicode character(s)"]
    xlsx_contents = PD.DataFrame(columns=headings)

    # Initialise an array to store errant unicode characters
    errant_unicode = []
    
    # Look at all XML files in the current directory
    filepaths = glob.glob("*.xml")
    for file in filepaths:

        # Initialise an array to store any comments about the files we are looking at
        file_comments = []

        # Convert the filename to a string so it can be used elsewhere
        xml_filename = str(file)

        # Read the XML contents
        xml = ""
        with open(xml_filename, mode="r", encoding="cp1252") as xf:
            xml_contents = xf.read()
            xml = BS(xml_contents, "xml")

        # Find HTML object in XML file
        html_object = xml.find(attrs={"type" : "text/html"})

        # If the HTML object exists
        if html_object != None:

            # Get HTML filename from the data attribute on this object 
            html_filename = html_object["data"]

            # Clear `new_xml`
            new_xml = ""
            
            # Reset `errant_unicode`
            errant_unicode = []
            
            # Replace the XML's HTML object with the corresponding HTML code, and take note of any errant unicode characters
            new_xml, errant_unicode = replace_xml_with_html(xml_filename, html_filename)

            # Let the user know if any errant unicode was found
            if len(errant_unicode) != 0:
                comment = f"Errant Unicode characters found in {xml_filename}: {', '.join(errant_unicode)}"
                print(comment)
                comment = "Errant Unicode characters found"
                file_comments.append(comment)

            # Print success message
            edited_file = xml_filename.split("\\")[-1]
            print(f"Edited {edited_file} successfully\n")

            # Write XML to file
            with open(xml_filename, mode="w", encoding="cp1252") as xf:
                xf.write(str(new_xml.prettify()))
                print(f"Saved {edited_file} successfully\n")

        # If the object doesn't exist... 
        else:
            
            # Let the user know the file was ignored
            ignored_file = xml_filename.split("\\")[-1]
            comment = f"Ignored editing {ignored_file} as no HTML reference was found\n"
            print(comment)
            comment = "No HTML reference found"
            file_comments.append(comment)

        # Make DataFrame row for Excel export
        data_row = [xml_filename.split("\\")[-1], "; ".join(file_comments), "; ".join(errant_unicode)]

        # Add it to the main DataFrame
        xlsx_contents.loc[len(xlsx_contents)] = data_row


    # Export details to Excel
    xlsx_filename = export_to_excel(xlsx_contents, overwrite=False)
    print(f"Exported details to {xlsx_filename}")


print(f"This program will look for files in the current directory:\n\n{str(OS.getcwd())}\n")
confirm = input("Confirm? (Y/n): ")
if confirm.upper() == "Y":
    print("Starting...\n")
    main()
    input("\nPress any key to continue... ")
