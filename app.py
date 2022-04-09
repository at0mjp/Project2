from flask import Flask, render_template, request, redirect, url_for
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
        user['name'] = text[5] + text[6] + text[7] + text[8]
        user['address'] = text[10] + " " + text[12]
        user['phone'] = ''.join(text[14:17])
        user['email'] = text[18]
        user['qual_summary'] = ''.join(text[23:35])
        user['education'] = ''.join(text[40:53])
        user['accomplishments'] = ''.join(text[58:105])
        user['work_history'] = ''.join(text[110:131])
        user['affiliation'] = ''.join(text[136:138])
        user['computer_skills'] = ''.join(text[146:150])
        counter = 0

        for item in user:
            user[item] = str(user[item]).replace(" ", " ")

        for i in range(len(text)):
            # Printing the line
            # Lines are seprated using "\n"
            print(counter, "\t", text[i], end="\n")
            # For Seprating the Pages
            counter = counter + 1
        print(user['name'])
        print(user['address'])
        print(user['email'])

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

            return redirect(url_for('display'))     # redirects user to the review and submit page

    return render_template("apply.html")


@app.route('/display')
def display():
    return render_template("display.html", user=user)
    # python section for text extraction and submission button


if __name__ == '__main__':
    app.run(debug=True)
