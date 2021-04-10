import argparse
import logging
import sys
import os
from src.config import CommonConfig
from src.train import do_training
import random
logger = logging.getLogger(__name__)


def parse_command_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.yaml')
    return parser.parse_args()


def truc():

    print(os.getcwd())
    arg = parse_command_args()
    config = CommonConfig(default_configs=[], custom_configs=["config_grid.yml"], args=arg)
    do_training(config)


if __name__ == '__main__':
    truc()




