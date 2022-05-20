'''
Extract the text from the HTML. 
For now, a copy is local but really ought to point back to Medium
'''
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

url_to_open="https://nickclegg.medium.com/making-the-metaverse-what-it-is-how-it-will-be-built-and-why-it-matters-3710f7570b04"

req = Request(url_to_open)
req.add_header('User-agent' , 'Crawling')
data = urlopen(req)

#@todo: add in getting from URL
#with open("making-the-metaverse-what-it-is-how-it-will-be-built-and-why-it-matters-3710f7570b04") as fh:
#    data = fh.read()
#fh.closed

html_data = soup = BeautifulSoup(data, 'html.parser')

body = ""
paras = html_data.find_all('p')
for para in paras:
    body += para.text

#remove the extraneous links at the bottom and keep the main text.
text_body = body.split('--')[0]
print(text_body)

#dump the paragraph text for processing. 
with open("metaverse.txt", "w") as fh:
    fh.write(text_body)
fh.closed
