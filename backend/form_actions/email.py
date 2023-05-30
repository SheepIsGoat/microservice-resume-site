import os
from typing import List, Optional
from logging import Logger

from flask import Flask, render_template, request, url_for, redirect
from flask.app import BaseResponse
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

from data_classes.formdata import SendgridAdmin


class Sendgrid():
    """
    Manage sending emails from the web form.
    """
    def __init__(
            self,
            logger: Optional[Logger]=None,
            api_key: str=None,
            sender_email: str=None,
            replyto_email: str=None,
            template_id: str=None
    ) -> None:
        
        self.logger = logger if logger is not None else Logger()

        self.api_key = (
            api_key or
            os.environ.get(
                'SENDGRID_API_KEY', 
                None,
            )
        )

        self.sender_email = (
            sender_email or
            os.environ.get(
                "SENDER_EMAIL", 
                "funk.ml.engineering+automail@gmail.com",
            )
        )

        self.replyto_email = (
            replyto_email or
            os.environ.get(
                "REPLYTO_EMAIL", 
                "funk.ml.engineering+personal_site@gmail.com",
            )
        )

        self.template_id = (
            template_id or
            os.environ.get(
                "SENDGRID_TEMPLATE_ID",
                "d-3838ba39f31c40098c8b137104844cd8"
            )
        )


    def send_contact_email(
            self
    ) -> BaseResponse:
        """
        Handle a sendemail request from the flask server.
        Sends an email to the sendgrid admin and to the person that viewed your page.
        """

        if request.method == "POST":
            name = request.form['name']
            subject = request.form['Subject']
            email = request.form['_replyto']
            message = request.form['message']

            new_friend_email_res = self.send_templated_email([email])
            to_me = self.send_plain_email(
                from_email=self.sender_email,
                to_emails=[self.replyto_email],
                subject=subject,
                message=message,
                name=name
            )
            self.logger.info(f"Status: {new_friend_email_res} {to_me}")

        return redirect('/')

    def send_plain_email(
            self,
            from_email: str,
            to_emails: List[str],
            subject: str,
            message: str,
            name: str,
    ) -> str:
        """
        Send a plain email
        """

        body = f"<p>{message}</p>" + \
            f"<p>Sender Name: {name}</p>" + \
            f"<p>Sender Email: {from_email}</p>"
        message = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            html_content=body
        )
        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            code, body, headers = response.status_code, response.body, response.headers
            self.logger.info(f"Response Code: {code} ")
            self.logger.info(f"Response Body: {body} ")
            self.logger.info(f"Response Headers: {headers} ")
            self.logger.info("Message Sent!")
            return str(response.status_code)
        except Exception as e:
            self.logger.info("Error: {0}".format(e))
        return "500"


    def send_templated_email(
            self,
            to_emails: List[str],
            from_email=None,
    ) -> str:
        """ 
        Send a dynamic email to a list of email addresses

        :returns API response code
        """
        if from_email is None:
            from_email = self.sender_email

        # create Mail object and populate
        message = Mail(
            from_email=from_email,
            to_emails=to_emails
        )
        message.bcc=self.replyto_email
        message.reply_to=self.replyto_email
        message.template_id = self.template_id
        # create our sendgrid client object, pass it our key, then send and return our response objects
        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            code, body, headers = response.status_code, response.body, response.headers
            self.logger.info(f"Response code: {code}")
            self.logger.info(f"Response headers: {headers}")
            self.logger.info(f"Response body: {body}")
            self.logger.info("Dynamic Messages Sent!")
            return str(response.status_code)
        except Exception as e:
            self.logger.info("Error: {0}".format(e))
        return "500"