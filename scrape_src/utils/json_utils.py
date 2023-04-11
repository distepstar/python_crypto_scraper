import json


def pretty_print(json_file, indent):
    print(json.dumps(json_file, indent=indent))


def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True
