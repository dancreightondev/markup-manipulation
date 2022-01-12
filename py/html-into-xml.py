from bs4 import BeautifulSoup as BS
from pathlib import Path
import os as OS
import sys
import re


def find_errant_unicode(string):

    # Define the regular expression to use when parsing
    regex = "&([^;]+);"

    # Parse string for errant unicode
    regex_result = re.findall(regex, string)
    if regex_result is not None:
        print(f"Errant unicode found: {regex_result}")
    else:
        print("No errant unicode found, or regex operation failed")

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
    with open(xml_filename, mode="r", encoding="utf-8") as xf:
        xml_contents = xf.read()
        xml = BS(xml_contents, "xml")

        # While doing so, search the source for errant unicode for later auditing
        errant_xml_chars = find_errant_unicode(xml_contents)

    # Read the HTML contents
    with open(html_filename, mode="r", encoding="utf-8") as hf:
        html_contents = hf.read()
        html = BS(html_contents, "xml")

        # While doing so, search the source for errant unicode for later auditing
        errant_html_chars = find_errant_unicode(html_contents)

    # Find the appropriate content to replace (XML object with attribute type="text/html")
    obj_to_replace = xml.find(attrs={"type" : "text/html"})

    # Edit HTML to add hashes either side of the content
    # (this is specific to the intended use of this program but is not required for it to run - delete this section or comment it out if it's not needed for you)
    wrap_content_with_hashes(html, html.find("div"))

    # Replace HTML reference with HTML code in the XML file
    obj_to_replace.replaceWith(html)

    # Return the modified & prettified XML
    return xml


def main():
    
    # Look at all XML files in the current directory
    filepaths = Path(OS.getcwd()).rglob("*.xml")
    for file in filepaths:

        # Convert the filename to a string so it can be used elsewhere
        xml_filename = str(file)

        # Read the XML contents
        xml = ""
        with open(xml_filename, mode="r", encoding="utf-8") as xf:
            xml_contents = xf.read()
            xml = BS(xml_contents, "xml")

        # Find HTML object in XML file
        html_object = xml.find(attrs={"type" : "text/html"})

        # Get HTML filename from the data attribute on this object if the object exists
        if html_object is not None:
            html_filename = html_object["data"]

            # Replace the XML's HTML object with the corresponding HTML code
            new_xml = replace_xml_with_html(xml_filename, html_filename).prettify()

            # Print success message
            edited_file = xml_filename.split("\\")[-1]
            print(f"Edited {edited_file} successfully")

            # Write XML to file
            with open (xml_filename, mode="w", encoding="utf-8") as xf:
                xf.write(new_xml)
                print(f"Saved {edited_file} successfully")

        #If the object doesn't exist... 
        else:

            # Add ignored files to a list for later auditing
            ignored_files = []
            ignored_files.append(xml_filename)
            
            # Print ignore message
            ignored_file = xml_filename.split("\\")[-1]
            print(f"Ignoring {ignored_file} as no HTML reference was found")

        # Space messages out for readability
        print("\n")

print(f"Scanning in current directory: {str(OS.getcwd())}\n")
confirm = input("Confirm? (Y/n): ")
if confirm.upper() == "Y":
    original_stdout = sys.stdout
    sys.stdout = open("log.txt", "w")
    main()
    sys.stdout = original_stdout
    input("\nCompleted.\nSee 'log.txt' for details and any errors.\nPress any key to exit... ")
