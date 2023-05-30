from typing import List

from flask import Flask, render_template, request, url_for, redirect
from form_actions.email import Sendgrid


app = Flask(__name__)
sendgrid = Sendgrid(logger=app.logger)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/sendemail/", methods=['POST'])
def send_contact_me_email():
    return sendgrid.send_contact_email()

if __name__ == '__main__':
    app.run()
