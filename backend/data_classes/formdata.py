import os

class FormFiller():
    """
    Wrapper for the details of person that filled out your ContactMe form.
    """
    def __init__(
            self,
            name,
            subject,
            replyto,
            message
    ) -> None:
        self.name = name
        self.subject=subject
        self.replyto=replyto
        self.message=message

class SendgridAdmin():
    """
    Wrapper for variables needed to send emails via sendgrid
    """
    def __init__(
            self,
            api_key: str=None,
            sender_email: str=None,
            replyto_email: str=None
    ) -> None:
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