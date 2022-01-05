# markup-manipulation
A set of Python programs that manipulate XML and HTML files in various ways. I primarily used these for tasks at work that would otherwise be very mundane to do by hand.

`xml-to-excel.py` — Scans an XML file for specific data and outputs it to an Excel workbook.
`html-into-xml.py` — Inserts the code from a HTML file into a given place in an XML file.

## `xml-to-excel.py`
### Dependencies
- pandas (v1.3.5) `python -m pip install -U pandas`
    - Used to export data to an Excel workbook.
- Beautiful Soup (v4.10.0) `python -m pip install -U beautifulsoup4`
    - Used to parse HTML files.
---
Repository maintained by [@dancreightondev](https://twitter.com/dancreightondev).