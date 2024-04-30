from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import os
import re
from pdfminer.high_level import extract_pages, extract_text
import unicodedata
import whisper
from pathlib import Path
import json

# media dict with the following structure
#  {fileLocation: string, 
#   fileType: string, 
#   downloadUrl: string, 
#   accessDate: string}

# processed media dict with the following structure
#  {media: dict, 
#   title: string, 
#   text: string, 
#   identifier: int}

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    # texts = soup.findAll(text=True)
    # visible_texts = filter(tag_visible, texts)  
    # return u" ".join(t.strip() for t in visible_texts)
    return soup.get_text()

def title_from_html(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string
    return title

def get_all_links(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

def remove_control_characters(s):
 return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")


#data collection
def download_media():
    print("Downloading media.")

def checkType(media):
    print("checkingType")
    return media["fileType"]

#pre processing data
def extractTitle(fileLocation):
    print("extracting title")
    title = Path(fileLocation).stem
    return title

def extractIdentifier(media):
    print("extracting identifier")
    return ""

def extractTextBody(media):
    print("extracting Text body")
    return ""

def transcribe(sourcePath):
    print("transcribing")
    model = whisper.load_model("base")
    audio = whisper.load_audio(sourcePath)
    result = model.transcribe(audio)
    # result["segments"] also has timestamps
    return result["text"]

#interface for next module
def saveProcessedMedia(processedMedia):
    if processedMedia["media"]["fileLocation"] == "":
        src_path = "0_media/"
    else:
        path = Path(processedMedia["media"]["fileLocation"])
        src_path = str(path.parent)
    dest_path = src_path + "/processed/" + path.stem + ".json"
    print("saving media at " + dest_path)
    with open(dest_path, 'w') as fp:
        json.dump(processedMedia, fp, sort_keys=True, indent=4)

def loadProcessedMedia(media):
    path = Path(media["fileLocation"])
    src_path = str(path.parent)
    dest_path = src_path + "/processed/" + path.stem + ".json"
    print(Path(dest_path))
    if Path(dest_path).is_file():
        with open(dest_path, 'r') as fp:
            processedMedia = json.load(fp)
        return processedMedia
    else:
        print("this media has not been processed before")
        processMedia(media)
        loadProcessedMedia(media)

#input media, output processedMedia
def processMedia(media):
    print("processing media")
    type = checkType(media)
    sourcePath = media["fileLocation"]
    if type == "web":
        url = media["downloadUrl"]
        title = title_from_html(url)
        text = text_from_html(url)
    if type == "audio" or type == "video":
        print(sourcePath)
        text = transcribe(sourcePath) 
        title = extractTitle(sourcePath)
    if type == "pdf":
        text = extract_text(sourcePath)
        title = extractTitle(sourcePath)
    if type == "text":
        f = open(sourcePath, "r")
        text = f.read()
        f.close()
        title = extractTitle(sourcePath)

    textWithoutControlCharacters = remove_control_characters(text)    
    processedMedia = {"media": media, "identifier": 0, "title": title, "text": textWithoutControlCharacters}
    saveProcessedMedia(processedMedia)