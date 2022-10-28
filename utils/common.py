import re

def extract_username (var):
    return "".join(re.findall(r'\w+', var)).replace("_", "").lower()

def is_not_empty (var):
    if (isinstance(var, bool)):
        return var
    elif (isinstance(var, int)):
        return not var == 0
    empty_chars = ["", "null", "nil", "false", "none"]
    return var is not None and not any(c == "{}".format(var).lower() for c in empty_chars)

def is_true (var):
    false_char = ["false", "ko", "no", "off"]
    return is_empty(var) or not any(c == "{}".format(var).lower() for c in false_char)

def is_false (var):
    return not is_true(var)

def is_empty (var):
    return not is_not_empty(var)

def is_disabled (var):
    return is_empty(var) or "changeit" == var
