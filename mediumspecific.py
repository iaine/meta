"""
Pleasecholder for Medium Specific Reading
"""
from bs4 import BeautifulSoup
import json

#@todo: add in getting from URL

with open("making-the-metaverse-what-it-is-how-it-will-be-built-and-why-it-matters-3710f7570b04") as fh:
    data = fh.read()
fh.closed

html_data = soup = BeautifulSoup(data, 'html.parser')

#could be useful to read the JSON at somepoint to get the medium specific parts. 
scripts = html_data.find_all('script')
for script in scripts:
    if 'window.__PRELOADED_STATE__ =' in script.text:

        jsonStr = script.text.strip()
        #jsonStr = jsonStr.split('[')[1].strip()
        #jsonStr = jsonStr.split(']')[0].strip()
        jsonStr = jsonStr.replace("'", '"')

        jsonObj = json.loads(jsonStr)

        print(jsonObj)
