import os
import sys



if __name__ == '__main__':
    # echo the environment we're passing in
    env_string = os.environ['MONEY_PRINTER_ENV']
    print(" * setting env to {0}".format(env_string))

    # sometimes we run with whacky paths, so lets set the python runtime
    # pwd to something sane
    pwd = os.path.abspath(os.path.dirname(__file__) + "/../../")

    print(" * changing pwd to {0}".format(pwd))
    os.chdir(pwd)

    # also add the core dir to the path so we can include from it
    print(" * augmenting path with core")
    sys.path.append(pwd)
    print(" * path: {0}".format(sys.path))

    # fetch the environment we need to be loading
    from server import load_config
    from server.config import config as server_config
    app_config = load_config()

    from core.apis.mailgun import MailGunConfig
    from core.repositories.profile_repository import ProfileRepository, ProfileRepositoryConfig, RegisterProfileRequest

    repo = ProfileRepository(ProfileRepositoryConfig(
        mailgun_config=MailGunConfig(api_key=server_config['mailgun']['api_key'],
                                     domain=server_config['mailgun']['domain']),
        mysql_config=app_config['db']
    ))

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


