import re

import os

def remove_accents(var):
    rtn = var.lower()
    rtn = re.sub(r'[àáâãäå]', 'a', rtn)
    rtn = re.sub(r'[èéêë]', 'e', rtn)
    rtn = re.sub(r'[ìíîï]', 'i', rtn)
    rtn = re.sub(r'[òóôõö]', 'o', rtn)
    rtn = re.sub(r'[ùúûü]', 'u', rtn)
    return rtn

def extract_alphanum (var):
    return remove_accents("".join(re.findall(r'\w+', var)).replace("_", "").lower())

def is_empty_array(array):
    return array is None or len(array) <= 0 or not any(is_not_empty(elem) for elem in array)

def is_not_empty_array(array):
    return not is_empty_array(array)

def is_not_empty (var):
    if (isinstance(var, bool)):
        return var
    elif (isinstance(var, int)):
        return not var == 0
    empty_chars = ["", "null", "nil", "false", "none"]
    return var is not None and not any(c == "{}".format(var).lower() for c in empty_chars)

def is_true (var):
    false_char = ["false", "ko", "no", "off"]
    return is_not_empty(var) and not any(c == "{}".format(var).lower() for c in false_char)

def is_false (var):
    return not is_true(var)

def is_empty (var):
    return not is_not_empty(var)

def sn_message(username, message):
    return re.sub("^At", "From {} at".format(username), message)

def is_disabled (var):
    return is_empty(var) or "changeit" == var

def is_enabled(var):
    return not is_disabled(var)

def is_not_null_env(env_key):
    return is_enabled(os.getenv(env_key))

def is_null_env(env_key):
    return not is_not_null_env(env_key)

def is_from_another_account(msg):
    return re.match("^From.* at", msg)

