import json
import importlib.util


def load_json_file(filename):
    with open(filename, "r") as f:
        content = json.load(f)
    return content


def load_file(filename):
    with open(filename, "r") as f:
        content = f.read()
    return content


def import_lib(lib: str, path):
    spec = importlib.util.spec_from_file_location(lib, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
