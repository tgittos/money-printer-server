from pathlib import Path

from core.apis.mailgun import *

class ProfileCreatedNotification(object):
    profile=None
    temp_password=None

    def __init__(self, profile, password):
        self.profile = profile
        self.temp_password = password


def notify_profile_created(config, notification):
    notification = Path("core/templates/notifications/profile_created.html").read_text()
    notification = notification.replace("{name}",
                                        "{0} {1}".format(notification.profile.first_name, notification.profile.last_name))
    notification = notification.replace("{username}", notification.profile.email)
    notification = notification.replace("{password", notification.temp_password)

    mg = MailGun(config)
    result = mg.send(MailGunMessage(
        to=[MailGunRecipient(name="{0} {1}".format(notification.profile.first_name, notification.profile.last_name),
                             email=notification.profile.email)],
        subject="New account created on Money Printer",
        html=notification
    ))
    return result
