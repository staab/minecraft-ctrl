import re
from itertools import tee, chain


def parse_data(s):
    result, i = parse_generic(c for c in s)

    return result


def parse_generic(i):
    for c in i:
        if c == '"':
            return parse_string(i)

        if c == '{':
            return parse_dict(i)

        if c == '[':
            return parse_list(i)

        # UUIDs are a list of [I; n, n, n], just treat them as a list
        if c == 'I':
            next(i)
            continue

        if c != ' ':
            return parse_literal(chain([c], i))


def parse_literal(i):
    b = ''
    is_uuid = False
    for c in i:
        if c in ']},':
            i = chain([c], i)
            break

        b += c

    float_match = re.match(r'^(-?[\d\.]+)[sbdf]?$', b)

    if not float_match:
        raise ValueError(f"Unable to parse {b}")

    return float(float_match.group(1)), i



def parse_dict(i):
    key = ''
    data = {}

    while True:
        c = next(i)

        if c == '}':
            return data, i

        if c == ':':
            # Parse the value
            data[key], i = parse_generic(i)

            # Reset the key
            key = ''

            # Keep going
            continue

        if not key and c in ', ':
            continue

        key += c


def parse_list(i):
    data = []

    while True:
        c = next(i)

        if c not in '], ':
            i = chain([c], i)

        if c == ']':
            return data, i

        item, i = parse_generic(i)

        if item:
            data.append(item)


def parse_string(i):
    data = ''
    for c in i:
        if c == '"':
            return data, i

        data += c


