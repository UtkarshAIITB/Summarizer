from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from fpdf import FPDF
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from summarize import *
import re
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch, cm


local_server = True
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.htm')


@app.route('/text')
def text():
    global input
    input = "Enter text"
    return render_template('text.htm', input = input)


@app.route('/textupload', methods = ['GET', 'POST'])
def upload_text():
    # pdf = FPDF()
    # pdf.add_page()
    # pdf.set_font("Arial", size = 10)

    short = request.form['text']                                  #input the updated text
    short = short.replace("\n", "")

    canvas = Canvas('summary.pdf')
    canvas.drawString(1*inch , 10*inch, short)
    canvas.save()
    
    fileobj = open("summary.pdf", 'rb')
    pdfreader = PyPDF2.PdfFileReader(fileobj)
    page = pdfreader.numPages
    text = ""

    for x in range(page):
        pageObj = pdfreader.getPage(x)
        parts = pageObj.extractText()
        text += parts

    text = text.replace("/n" , " ")

    with open('summary.txt', 'w', encoding = 'utf-8') as s:
        s.truncate(0)
        s.write(text)

    short = generate_summary('summary.txt', 2)
    fileobj.close()

    return render_template('text.htm' ,short = short)


@app.route('/pdf')
def pdf1():
    return render_template('pdf.htm')


@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    ALLOWED_EXTENSIONS = {'pdf'}                                      #extensions allowed for submitting
    if request.method == 'POST':
        f = request.files['file']
        global file_name
        f.save(secure_filename(f.filename))
        file_name = f.filename
        extension = file_name.rsplit(".",1)[1]

        if extension == "pdf":
        #return('file uploaded successfully')
        
            fileobj = open(file_name, 'rb')
            pdfreader = PyPDF2.PdfFileReader(fileobj)
            page = pdfreader.numPages                                      #stores total no. of pages
            text = ""
                
            for x in range(page):
                pageObj = pdfreader.getPage(x)
                parts = pageObj.extractText()                      #extracts the text from the pdf file of a particular page in parts
                #parts = parts.replace(' ', '-')
                text +=parts                                               #stored the complete data of pdf in the text 

                #text = re.sub("-"," ", text)
            text = text.replace("\n", " ")

            with open('summary.txt', 'w', encoding = 'utf-8') as s:        #storing the extracted data from pdf into text file 
                s.write(text)

            final = generate_summary("summary.txt", 2) 
            fileobj.close()

        else:
            final = "File not supported. Submit only '.pdf' files."
        

    return render_template('pdf.htm', final = final)

@app.route('/audio')
def audio():
    return render_template('audio.htm')

if __name__ == "__main__":
    app.run(debug = True)