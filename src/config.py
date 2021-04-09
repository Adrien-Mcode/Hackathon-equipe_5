import copy
import os
from munch import munchify
import dynamic_yaml
from dynamic_yaml.yaml_wrappers import YamlDict
import logging
import re

logger = logging.getLogger(__name__)


def override_yaml_list(filename_list):

    def rec_update(dico, update_dico):
        is_dict_keys = [key for key in dico.keys() if isinstance(dico[key], YamlDict)]
        dico.update({key: update_dico[key] for key in update_dico.keys() if key not in is_dict_keys})
        for key in is_dict_keys:
            if key in update_dico.keys():
                if isinstance(update_dico[key], YamlDict):
                    dico[key] = rec_update(dico[key], update_dico[key])
                else:
                    dico[key] = update_dico[key]
        return dico
    config_dict = {}
    for filename in filename_list:
        with open(filename, encoding='utf8') as f:
            d = dynamic_yaml.load(f)
        config_dict = rec_update(config_dict, d)
    return config_dict


def safe_create_dir(path):
    if path:
        try:
            os.makedirs(path)
        except OSError:  # if the directory already exists
            pass


class CommonConfig:
    ###############
    # CORE CONFIG #
    ###############

    def __init__(self, default_configs=(), custom_configs=(), args=None) -> None:  # TODO : voir si args est pas plus intéressant
        """
        1) read all configs, and set all attributes
        2) apply standard methods
            (compute dates, initialize DataProvider, create paths, get grain_list)
        3) apply custom methods
        """
        # Override selon l'ordre ?
        list_config = list(default_configs) + list(custom_configs)
        self.dict_attr = override_yaml_list(list_config)
        self._from_dict()
        self.args = args
        self._from_args()
        self.model_filename = "model/" + self.model_name + "_" + self.sample_name + ".pkl"
        self.figure_folder = "figure/" + self.model_name + "_" + self.sample_name

    def _from_args(self):
        for k, v in vars(self.args).items():
            setattr(self, k, v)

    def _from_dict(self):
        obj = munchify(self.dict_attr)  # Automatically construct the config object
        for elem in list(self.dict_attr.keys()):
            setattr(self, elem, getattr(obj, elem))

    @staticmethod
    def flattened_dict_values(d):
        import collections

        def flatten(d, parent_key='', sep='_'):
            items = []
            for k, v in d.items():
                new_key = parent_key + sep + k if parent_key else k
                if isinstance(v, collections.MutableMapping):
                    items.extend(flatten(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            return dict(items)

        return flatten(d).values()



