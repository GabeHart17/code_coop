import re
def verify(s):
    match = re.match(r'\[([0-9](, )?)*\]|[0-9]*', s)
    return bool(match)
