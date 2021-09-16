if __name__ == "__main__":

    from script_base import *

    from server.config import config as server_config

    from core.apis.mailgun import MailGunConfig
    from core.repositories.profile_repository import get_repository as get_profile_repository, RegisterProfileRequest

    repo = get_profile_repository(
        mysql_config=app_config['db'],
        mailgun_config=MailGunConfig(api_key=server_config['mailgun']['api_key'],
                                     domain=server_config['mailgun']['domain']))

    email = input("Email to invite: ")
    first_name = input("First name: ")
    last_name = input("Last name: ")

    result = repo.register(RegisterProfileRequest(
        email=email, first_name=first_name, last_name=last_name
    ))

    if result.success:
        print("Your invite was sent to {0}, please check your email".format(email))
    else:
        print("Something went wrong, try again: {0}".format(result.message))
