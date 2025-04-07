import hashlib

def check_letter(letter):
    return (1072 <= ord(letter) <= 1103) or (1040 <= ord(letter) <= 1071) or (ord(letter) == 1025) or \
            (ord(letter) == 1105) or letter == " "

def check_nic_letter(letter):
    return (1072 <= ord(letter) <= 1103) or (1040 <= ord(letter) <= 1071) or (ord(letter) == 1025) or \
            (ord(letter) == 1105)

def validation_password(passwd):
    if len(passwd) < 6:
        return (False, "Пароль слишком короткий!")
    if any(check_letter(letter) for letter in passwd):
        return (False, "Используются недопустимые символы в пароле!")
    if len(passwd) > 20:
        return (False, "Пароль слишком длинный!")
    if "'" in passwd:
        return (False, "Гений решил потыкать кавычки?))")
    return (True, "Все в порядке")

def validation_username(username):
    if len(username) < 3:
        return (False, "Имя слишком короткое!")
    if any(check_nic_letter(letter) for letter in username):
        return (False, "Используются недопустимые символы в имени!")
    if len(username) > 20:
        return (False, "Имя слишком длинное!")
    if "'" in username:
        return (False, "Гений решил потыкать кавычки?))")
    return (True, "Все в порядке")

def encrypt(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def compare(text, hash):
    return encrypt(text) == hash