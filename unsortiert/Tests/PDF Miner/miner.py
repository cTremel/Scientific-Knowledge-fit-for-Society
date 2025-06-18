import os
import re
from pdfminer.high_level import extract_pages, extract_text
import unicodedata
import whisper

videoSource = "Expert Interviews/"
transcriptTextPath = videoSource + "text/"
transcriptFullPath = videoSource + "full/"
directory = os.fsencode(videoSource)
model = whisper.load_model("base")

for file in os.listdir(directory):
   videopath = os.fsdecode(file)
   if videopath.endswith(".mp4"):
      audio = whisper.load_audio(videoSource + videopath)
      result = model.transcribe(audio)
      #print(result)
      #print(result.keys()) dict_keys(['text', 'segments', 'language'])
      #print(result["segments"]) are the timestamps
      
      transcriptTextPath_path = transcriptTextPath + videopath
      transcriptFullPath_path = transcriptFullPath + videopath
         
      file = open((transcriptTextPath_path + ".txt"), "w")
      file.write(result['text'])
      file.close
      file = open((transcriptFullPath_path + ".txt"), "w")
      file.write(str(result))
      file.close
   


""" def remove_control_characters(s):
 return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

src_folder = "Tier 1/"
extracted_folder = "Tier 1/extracted"
cleaned_folder = "Tier 1/cleaned"
directory = os.fsencode(src_folder)
    
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".pdf"): 
        src_path = src_folder + filename
        extracted_path = extracted_folder + filename
        cleaned_path = cleaned_folder + filename
        text = extract_text(src_path)
        textNoControlCharacters = remove_control_characters(text)
        for mode in ["extracted/", "cleaned/"]:
         file = open((src_folder + mode + filename + ".txt"), "w")
         if mode == "extracted/":
            file.write(text)
         if mode == "cleaned/":
            file.write(textNoControlCharacters)
         file.close
        continue
     else:
         continue
 """
