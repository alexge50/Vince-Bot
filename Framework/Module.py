from collections import namedtuple
from Framework import util

ModuleBuilder = namedtuple('ModuleBuilder', 'name class')


def load_module_builder(json_module, directory):  # creates a ModuleBuilder
    lib = "{}.{}.{}".format(directory,
                            json_module['name'],
                            json_module['lib'])
    util.import_lib(lib)

    module_class = eval("{}.{}".format(lib,
                                       json_module["class"]))

    return ModuleBuilder(json_module['name'], module_class)
