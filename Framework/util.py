import json


def load_json_file(filename):
    with open(filename, "r") as f:
        content = json.load(f)
    return content


def load_file(filename):
    with open(filename, "r") as f:
        content = f.read()
    return content


def import_lib(lib: str):
    exec("import {}".format(lib))
