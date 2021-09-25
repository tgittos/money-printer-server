from server.services.api.application import ApiApplication

if __name__ == "__main__":
    email = input("Email to invite: ")
    first_name = input("First name: ")
    last_name = input("Last name: ")

    app = ApiApplication()
    result = app.init(
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    if result.success:
        print("Your invite was sent to {0}, please check your email".format(email))
    else:
        print("Something went wrong, try again: {0}".format(result.message))

