import requests


class MailGunConfig(object):
    api_key=None
    domain=None

    def __init__(self, api_key=None, domain=None):
        self.api_key = api_key
        self.domain = domain


class MailGunRecipient(object):
    name=None
    email=None

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return "{0} <{1}>".format(self.name, self.email)


class MailGunMessage(object):
    to_addresses = None
    from_address=MailGunRecipient(name="Money Printer", email="no-reply@moneyprintergobrr.io")
    subject=None
    html=None

    def __init__(self, to, subject, html, from_address=None):
        self.to_addresses = to
        if from_address is not None:
            self.from_address = from_address
        self.subject = subject
        self.html = html


class MailGun:

    def __init__(self, config):
        self.api_url = "https://api.mailgun.net/v3/{0}/messages".format(config.domain)
        self.api_key = config.api_key

    def send(self, msg):
        response = requests.post(
            self.api_url,
            auth=("api", self.api_key),
            data={
                "from": msg.from_address,
                "to": msg.to_addresses,
                "subject": msg.subject,
                "html": msg.html
            }
        )
        return response
