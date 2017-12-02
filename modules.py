import json


def build_modules_list(bot_instance, file):
    with open(file, "r") as f:
        config = json.load(f)

    modules_list = {}

    for module_name in config["active_modules"]:
        modules_list[module_name] = build_module(bot_instance, config[module_name])

    return modules_list


def build_module(bot_instance, module_config):
    exec("import {}".format(module_config["lib"]))

    return eval("{}.{}(bot_instance)".format(module_config["lib"], module_config["class"]))


def build_module_instance_list(modules_config):
    module_instance_list = {}

    for module_name in modules_config["active_modules"]:
        module_instance_list[module_name] = build_module_instance(modules_config[module_name])

    return module_instance_list


def build_module_instance(module_config):
    if module_config["config_file"] is not "":
        with open(module_config["config_file"], "r") as f:
            default_module_configuration = json.load(f)
    else:
        default_module_configuration = None

    module_class = None

    exec("import {}".format(module_config["lib"]))
    module_class = eval("{}.{}".format(module_config["lib"], module_config["instance_class"]))

    return {"default_config": default_module_configuration, "class": module_class}
    # it returns the "settings" to build a module_instance of this kind
