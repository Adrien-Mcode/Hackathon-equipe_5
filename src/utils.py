# YAML
from typing import Union
import logging
import os
import pandas as pd
from pandas.errors import EmptyDataError
import dynamic_yaml
import joblib
import yaml
from dynamic_yaml.yaml_wrappers import YamlDict
import datetime as dt

logger = logging.getLogger(__name__)


# YAML
def read_yaml(filename: str):
    with open(filename, encoding='utf8') as f:
        d = dynamic_yaml.load(f)
    return d


def write_yaml(d: dict, filename: str):
    with open(filename, 'w', encoding='utf8') as yaml_file:
        yaml.dump(d, yaml_file, default_flow_style=False)


def override_yaml(d: dict, override_d: dict):
    """
    Update the loaded 'd' yaml with the keys of "filename". Will recurse if old_dict[key] is still a dict.

    Parameters
    ----------
    d : dict
        loaded yaml
    override_d : dict
        loaded yaml with the label that should override

    Returns
    -------
    d : dict
        d updated with the keys of override_d
    """

    def override_aux(old_dict, new_dict):
        for key in old_dict.keys():
            if key in new_dict.keys():
                if isinstance(old_dict[key], dict):
                    old_dict[key] = override_aux(old_dict[key], new_dict[key])
                else:
                    old_dict[key] = new_dict[key]
        return old_dict

    return override_aux(d, override_d)


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


# FILES
def remove_if_exists(filename):
    if os.path.isfile(filename):
        logger.debug('Removed : ' + filename)
        os.remove(filename)
    else:
        logger.warning('No file to remove : ' + filename)


def make_dir(where, name):
    """ to create root_folder/new_folder/
    :param where: ex "root_folder/"
    :param name: ex "new_folder/"
    :return:
    """
    if name[-1] == '/':
        name = name[:-1]
    if name not in os.listdir(where):
        os.mkdir(where + name)


def safe_create_dir(path):
    if path:
        try:
            os.makedirs(path)
        except OSError:  # if the directory already exists
            pass


def save_mlflow_run_id(run_name, run_id, dict_path):
    def aux_read_yaml(filename: str):
        with open(filename, encoding='utf8') as f:
            d = yaml.load(f)
        return d
    if os.path.isfile(dict_path):
        id_dict = aux_read_yaml(dict_path)
        id_dict[run_name] = run_id
        write_yaml(id_dict, dict_path)
    else:
        id_dict = {run_name: run_id}
        write_yaml(id_dict, dict_path)


def load_mlflow_run_id(run_name, dict_path):
    return read_yaml(dict_path)[run_name]


def load_from_csv(file: str, alogger, **kwargs):  # parse_dates=["DPT_DATE"]
    alogger.debug(f"loading {file}")
    if os.path.isfile(file):
        try:
            raw = pd.read_csv(file, sep=';', decimal=',', **kwargs)
            return raw
        except EmptyDataError:
            return pd.DataFrame()
    else:
        return pd.DataFrame()


def save_to_csv(file, data, alogger):
    alogger.debug(f"saving {file}")
    data.to_csv(file, sep=";", index=False, decimal=',')
    logger.info(f"{file} saved")


def exists(file):
    return os.path.isfile(file)


def save_model(model, path_to_model):
    """
    Save the model as a pickle file at the given path
    :param model: sklearn model
    :param path_to_model: standard path to the model
    :return: None
    """
    try:
        os.makedirs(os.path.abspath(os.path.join(path_to_model, os.pardir)))
    except OSError:  # if the directory already exists
        pass
    joblib.dump(model, path_to_model)


def load_model(path_to_model):
    """
    Load the model from pickle file at the given path
    :param path_to_cell: standard path to the model
    :return: skearn model
    """
    return joblib.load(path_to_model)


def date_to_datetime(date):
    """datetime.date(2001,01,01) -> datetime.datetime(2001,01,01,00,00,00,000)"""
    return dt.datetime.combine(date, dt.datetime.min.time())

