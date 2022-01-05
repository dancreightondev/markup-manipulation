import os
import xml.etree.ElementTree as ET
from pandas import DataFrame
from bs4 import BeautifulSoup as BS

def makeDataFrame(fnameQti, fnamesImg, fnamesAud, numImg, numAud):
    df = DataFrame({"QTI filename" : fnameQti,
                   "Image filename(s) in Media Library" : fnamesImg,
                   "Audio file(s) ID" : fnamesAud,
                   "Number of images in item" : numImg,
                   "Number of audio files in item" : numAud},
                   index=[0])
    return df

def getImgNamesFromHtmlFile(fname):
    with open(fname) as html: # Open the provided HTML file
        content = BS(html, features="html.parser") # Parse the HTML content
        fnames = [] # Initialise an array to store image filenames
        for attr in content.find_all("img"): # Iterate through all img objects in the HTML code
            fnames.append(attr["src"].split("/", 1)[-1]) # Store the filename in the src tag for later
    return fnames

def parseXmlFile(file):
    tree = ET.parse(file) # Parse XML
    root = tree.getroot() # Get the root of the XML element tree
    attr = "data" # Object attribute to search for. The objects that link to a file seem to always have the 'data' attribute
    objs = root.findall(".//*[@{}]".format(attr)) # Find all objects by attribute
    fnames = []
    for o in objs: # Iterate through the found objects
        data = o.attrib[attr] # Get filenames from found objects, as per the specified attribute (attr)
        fname = data.split("/", 1)[-1] # Tidy up the filename
        fnames.append(fname) # Store for processing later
    fnamesHtml = [n for n in fnames if n.endswith(".html")] # Store HTML filenames
    fnamesImg = [] # Initialise an array to store image filenames
    for h in fnamesHtml: # Iterate through the HTML files
        fnamesImg.extend(getImgNamesFromHtmlFile(h)) # Store image filenames
    fnamesAud = [n for n in fnames if n.endswith(".mp3")] # Store MP3 filenames
    parsedData = {"QTI filename" : file,
                  "Image filename(s) in Media Library" : ', '.join(fnamesImg),
                  "Audio file(s) ID" : ', '.join(fnamesAud),
                  "Number of images in item" : str(len(fnamesImg)),
                  "Number of audio files in item" : str(len(fnamesAud))} # Collate parsed data
    return parsedData

def exportXlsx(df):
    df.to_excel('qti-export.xlsx', sheet_name='qti.py', index=False) # Save provided pandas DataFrame to qti-export.xlsx in a sheet called qti.py

def main():
    inp = "Scan XML files in current directory:\n\n{}\n\nConfirm? (Y/n): "
    curdir = os.path.dirname(os.path.realpath(__file__))
    confirm = input(inp.format(curdir))
    if(confirm.upper() != "Y"):
        return
    else:
        print("\nStarting...\n")
        sheetData = [] # Initialise an array to store the data to go in the spreadsheet
        try:
            print("Parsing files")
            for file in os.listdir(curdir): # Iterate through the files in the current directory
                if not file.endswith('.xml'): continue # Only look at the XML files
                parsedData = parseXmlFile(file) # Parse the XML file and extract the data we need
                sheetData.append(parsedData) # Save the data we need ready for export
        except Exception as e:
            print(e)
        except:
            print("An unknown error occurred")
        else:
            print("Parsed all files successfully")
            
        try:
            print("Exporting to a new Excel file")
            exportXlsx(DataFrame(sheetData)) # Export the data to an Excel spreadsheet
        except Exception as e:
            print(e)
        except:
            print("An unknown error occurred")
        else:
            print("Exported successfully")

main()
input("\nPress Enter to exit ")
