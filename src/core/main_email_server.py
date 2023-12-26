from src.utils.EmailSender import EmailSender


def main(args):
    if len(args) > 0:
        for recipient in args:
            EmailSender.send_email(recipient, None, None, None, None, None, None)
