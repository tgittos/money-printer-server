from core.lib.jwt import hash_password, check_password

def check_password_works():
    candidate = "this is my password1!"
    hashed = hash_password(candidate)
    assert candidate != hashed
    assert check_password(hashed, candidate)