import json


def add_decimal_values(arguments):
    args = json.loads(arguments)
    value1 = args["value1"]
    value2 = args["value2"]
    result = value1 + value2
    return result


def add_hexadecimal_values(arguments):
    args = json.loads(arguments)
    value1 = args["value1"]
    value2 = args["value2"]
    decimal1 = int(value1, 16)
    decimal2 = int(value2, 16)
    result = hex(decimal1 + decimal2)[2:]
    return result
