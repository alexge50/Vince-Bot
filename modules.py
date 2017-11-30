import json


def build_modules_list(bot_instance, file):
    with open(file, "r") as f:
        config = json.load(f)

    modules_list = {}

    for module_name in config["active_modules"]:
        modules_list[module_name] = build_module(bot_instance, config[module_name])

    return modules_list


def build_module(bot_instance, module_config):
    if module_config["config_file"] is not "":
        with open(module_config["config_file"], "r") as f:
            module_config_file = json.load(f)
    else:
        module_config_file = None

    exec("import {}".format(module_config["lib"]))

    return eval("{}.{}(bot_instance, module_config_file)".format(module_config["lib"], module_config["class"]))
