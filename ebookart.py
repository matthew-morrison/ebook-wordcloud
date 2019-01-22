from wordcloud import WordCloud
from bs4 import BeautifulSoup
from os import path
import zipfile
import tempfile
import sys

#epub files are glorified HTML files packaged into a ZIP with extra information.

# requires bs4 and wordcloud from pip

filename = sys.argv[1]
contentfile = "content.opf" # content.opf holds chapter and image information, chapters are all different HTML files.
tempdir = tempfile.TemporaryDirectory() #lives in /tmp, auto deleted

if ".epub" not in filename:
    print("not valid epub file")
    exit()

with zipfile.ZipFile(filename,'r') as zip_ref: #extract all files from zipped epub to temp
    zip_ref.extractall(tempdir.name)

# this codeblock finds all of the chapter pages from the content page and stores them.
contents = open(path.join(tempdir.name, contentfile), 'r')
soup = BeautifulSoup(contents, "lxml")
megastr = " "
items = soup.find_all('item')
files = []
for item in items:
    #if "The_eye_of_the_world_split_" in item['href']:
    if "application/xhtml+xml" in item['media-type']:
        files.append(item['href'])

# this codeblock finds all text from the chapter pages and concatenates them
for file in files:
    soupy = BeautifulSoup(open(path.join(tempdir.name,file),'r'), 'html.parser')
    megastr+= soupy.text
     
print("Prepare for mega core-hogging")
wc = WordCloud(max_words=200000, width=2048, height=2048).generate(megastr)
wc.to_file(filename+".png")
