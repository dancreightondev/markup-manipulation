from bs4 import BeautifulSoup as BS
from pathlib import Path
import os as OS

def print_xml_from_file(filename):
    print(BS(open(filename).read(), "lxml").prettify())

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
    with open(xml_filename, "r") as xf:
        xml_contents = xf.read()
        xml = BS(xml_contents, "lxml")

    # Read the HTML contents
    with open(html_filename, "r") as hf:
        html_contents = hf.read()
        html = BS(html_contents, "html.parser")

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
        if not str(file).endswith("imsmanifest.xml"):
            xml_filename = str(file)

            # Read the XML contents
            xml = ""
            with open(xml_filename, "r") as xf:
                xml_contents = xf.read()
                xml = BS(xml_contents, "lxml")

            # Find HTML object in XML file
            html_object = xml.find(attrs={"type" : "text/html"})

            # Get HTML filename from the data attribute on this object if the object exists
            if html_object is not None:
                html_filename = html_object["data"]

                # Replace HTML object in the XML with the HTML code
                new_xml = replace_xml_with_html(xml_filename, html_filename).prettify()

                edited_file = xml_filename.split("\\")[-1]
                print(f"Edited {edited_file} successfully")
                #print(f"{new_xml}\n")
                
            else:
                ignored_file = xml_filename.split("\\")[-1]
                print(f"Ignoring {ignored_file} as no HTML reference was found")

main()
