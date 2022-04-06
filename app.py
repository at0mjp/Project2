from flask import Flask, render_template, request, redirect
from flask_bootstrap5 import Bootstrap
import PyPDF2
from werkzeug.utils import secure_filename
import os
from os import abort

app = Flask(__name__)
bootstrap = Bootstrap(app)

user = {}


@app.route('/')
def index():  # put application's code here

    pdfFileObj = open('static/sample_resume.pdf', 'rb')

    # Creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Getting number of pages in pdf file
    pages = pdfReader.numPages

    # Loop for reading all the Pages
    for i in range(pages):
        # Creating a page object
        pageObj = pdfReader.getPage(i)
        # Printing Page Number
        print("Page No: ", i)
        # Extracting text from page
        # And splitting it into chunks of lines
        text = pageObj.extractText().split('\n')
        # Finally the lines are stored into list
        # For iterating over list a loop is used
        user['name'] = text[5]
        user['email'] = text[18]

        '''for i in range(len(text)):
            # Printing the line
            # Lines are seprated using "\n"
            print(text[i], end="\n")
            # For Seprating the Pages
        '''
    # closing the pdf file object
    pdfFileObj.close()
    return render_template("index.html", user=user)


# normally this info would be in a config file, but it is fine here for now
# specifies the size, type and path for the user's upload in apply route
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD EXTENSIONS'] = ['.pdf']
app.config['UPLOAD PATH'] = 'uploads'


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    # python section for upload functionality
    if request.method == "POST":
        if request.files:                           # if there are files...
            resume = request.files["file"]          # "file" because it is the name of the input on apply.html
            print(resume)                           # for testing... prints the file name in the terminal

            # save the file to the uploads directory and uses the file's name as the filename
            resume.save(os.path.join(app.config['UPLOAD PATH'], resume.filename))

            return redirect(request.url)            # returns to the page after submitting the file

    return render_template("apply.html")





@app.route('/display')
def display():
    return render_template("display.html")
    # python section for text extraction and submission button


if __name__ == '__main__':
    app.run(debug=True)
