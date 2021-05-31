from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from summarize import *
import re

local_server = True
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.htm')

@app.route('/pdf')
def pdf1():
    return render_template('pdf.htm')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
       f = request.files['file']
       global file_name
       f.save(secure_filename(f.filename))
       file_name = f.filename
       return('file uploaded successfully')

@app.route('/pdfpage')
def pdf():
    fileobj = open(file_name, 'rb')
    pdfreader = PyPDF2.PdfFileReader(fileobj)
    page = pdfreader.numPages                         #stores total no. of pages
    text = ""

    for x in range(page):
        pageObj = pdfreader.getPage(x)
        parts = pageObj.extractText()                  #extracts the text from the pdf file of a particular page in parts
        #parts = parts.replace(' ', '-')
        text +=parts                                   #stored the complete data of pdf in the text 

    #text = re.sub("-"," ", text)
    text = text.replace("\n", " ")

    with open('summary.txt', 'w', encoding = 'utf-8') as s:                #storing the extracted data from pdf into text file 
        s.write(text)

    return( generate_summary("summary.txt", 2) )
    
    fileobj.close()
    #return render_template('pdf.htm' , page = page)


if __name__ == "__main__":
    app.run(debug = True)