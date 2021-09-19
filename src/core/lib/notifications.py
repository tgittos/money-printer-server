from pathlib import Path

from core.apis.mailgun import *


class ProfileCreatedNotification(object):
    profile=None
    temp_password=None

    def __init__(self, profile, password):
        self.profile = profile
        self.temp_password = password


class PasswordResetNotification(object):
    profile=None
    token=None

    def __init__(self, profile, token):
        self.profile = profile
        self.token = token


def notify_profile_created(config, notification):
    text = Path("core/templates/notifications/profile_created.html").read_text()
    text = text.replace("{name}", "{0} {1}".format(notification.profile.first_name, notification.profile.last_name))
    text = text.replace("{username}", notification.profile.email)
    text = text.replace("{password}", notification.temp_password)

    mg = MailGun(config)
    result = mg.send(MailGunMessage(
        to=[MailGunRecipient(name="{0} {1}".format(notification.profile.first_name, notification.profile.last_name),
                             email=notification.profile.email)],
        subject="New account created on Money Printer",
        html=text
    ))
    return result


def notify_password_reset(config, notification):
    text = Path("core/templates/notifications/password_reset.html").read_text()
    text = text.replace("{name}", "{0} {1}".format(notification.profile.first_name, notification.profile.last_name))
    text = text.replace("{username}", notification.profile.email)
    text = text.replace("{token}", notification.token)

    mg = MailGun(config)
    result = mg.send(MailGunMessage(
        to=[MailGunRecipient(name="{0} {1}".format(notification.profile.first_name, notification.profile.last_name),
                             email=notification.profile.email)],
        subject="Money Printer account password reset",
        html=text
    ))
    return result

