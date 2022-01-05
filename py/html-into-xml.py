from bs4 import BeautifulSoup as BS

def print_xml_from_file(filename):
    print(BS(open(filename).read(), "lxml").prettify())


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

    # Replace XML object with HTML
    obj_to_replace.replaceWith(html)

    # Return the modified & prettified XML
    return xml.prettify()


def main():
    new_xml = replace_xml_with_html("test.xml", "test.html")
    print(new_xml)

main()
