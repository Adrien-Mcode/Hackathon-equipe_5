import copy
import os
from munch import munchify
from ...utils.ioutils import safe_create_dir, override_yaml_list
import logging
from .globalstate import GlobalState
from .dataprovider import DataProvider
import re

logger = logging.getLogger(__name__)


class CommonConfig:
    ###############
    # CORE CONFIG #
    ###############
    from .utils import get_grain_perimeter, set_dates_from_grain_atom, initialize_smart_dates, get_csv_filename

    def __init__(self, default_configs=(), custom_configs=(), args=None,
                 dataprovider=DataProvider) -> None:  # TODO : voir si args est pas plus intéressant
        """
        1) read all configs, and set all attributes
        2) apply standard methods
            (compute dates, initialize DataProvider, create paths, get grain_list)
        3) apply custom methods
        """
        # Override selon l'ordre ?
        list_config = list(default_configs) + list(custom_configs)
        self.dict_attr = override_yaml_list(list_config)
        self.path_to_create = self.dict_attr["path"]
        self._from_dict()
        self.args = args
        self._from_args()
        self._create_dirs()
        self.state = GlobalState()
        self.dataprovider = dataprovider(config=self)
        self.model_grain_list = self.get_grain_perimeter()
        self.initialize_smart_dates()

    def _from_args(self):
        for k, v in vars(self.args).items():
            setattr(self, k, v)

    def _from_dict(self):
        obj = munchify(self.dict_attr)  # Automatically construct the config object
        for elem in list(self.dict_attr.keys()):
            setattr(self, elem, getattr(obj, elem))

    # noinspection PyAttributeOutsideInit
    def _create_dirs(self):
        for elem in self.flattened_dict_values(self.path_to_create):
            if not ("." in elem):  # not a file name
                os.makedirs(elem, exist_ok=True)
            else:
                try:
                    os.makedirs(os.path.dirname(elem), exist_ok=True)
                except Exception as e:
                    logger.info(f"can't create folders for the following path : {elem}")

    def copy(self):
        return copy.copy(self)

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

    #######################
    # REQUIRED PARAMETERS #
    #######################

    # Utile ?
    def set_current_grain(self, grain_atom):
        self.current_grain_atom = grain_atom
        self.set_dates_from_grain_atom()
        self.generate_filename()

    def generate_filename(self):
        self.model_filename = os.path.join(self.path.model, re.sub(r'\W+', '_', self.model_name) + ".pkl")

    get_csv_filename = staticmethod(get_csv_filename)
    #################
    # COMMON CONFIG #
    #################


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
