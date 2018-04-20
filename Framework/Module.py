from collections import namedtuple
from Framework import util

ModuleBuilder = namedtuple('ModuleBuilder', 'name class_name default_config resources permissions')


def load_module_builder(json_module, directory):  # creates a ModuleBuilder
    lib_name = "{}.{}".format(directory,
                              json_module['name'],
                              json_module['lib'])
    lib_path = "{}/{}/{}.py".format(directory,
                                    json_module['name'],
                                    json_module['lib'])
    lib = util.import_lib(lib_name, lib_path)

    module_class = lib.Main

    return ModuleBuilder(json_module['name'],
                         module_class,
                         json_module['default_config'],
                         json_module['resources'],
                         json_module['permissions'])


def make_module_builder_list(module_directory):
    json_modules = util.load_json_file(module_directory + '/modules.json')

    module_builders = []
    for module_name in json_modules:
        json_file = module_directory + '/' + module_name + '/' + module_name + '.json'
        module_builders.append(load_module_builder(util.load_json_file(json_file), module_directory))

    return module_builders


def new_instance(module_builder: ModuleBuilder, bot):
    return module_builder.class_name(bot)
