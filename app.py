from flask import Flask, render_template
from flask_bootstrap5 import Bootstrap
import PyPDF2

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


@app.route('/apply')
def apply():
    return render_template("apply.html")
    # python section for upload functionality

@app.route('/display')
def apply():
    return render_template("display.html")
    # python section for text extraction and submission button

if __name__ == '__main__':
    app.run(debug=True)
