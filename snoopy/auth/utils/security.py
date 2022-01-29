from passlib.hash import pbkdf2_sha256


def check_password(secret, hash_password):
    return pbkdf2_sha256.verify(secret, hash_password)


def make_password(secret):
    return pbkdf2_sha256.hash(secret)

