import argparse
import logging
import sys
from src.config import CommonConfig
from src.train import do_training
from src.test import do_test

logger = logging.getLogger(__name__)


def parse_command_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, nargs='+',
                        help='execution mode: train, test',
                        default=['train'])
    parser.add_argument('-s', '--step', type=str, nargs='+',
                        help='execution step: all, raw, preprocess, training, predict, eval',
                        default='all')
    parser.add_argument('--config', default='config.yaml')
    return parser.parse_args()


def main():
    arg = parse_command_args()
    logger.debug("running with debug level logs")
    logger.info('[%s] Started ' % ' '.join(sys.argv[:]))
    modes = [x for x in arg.mode]
    logger.info(f"will run modes : {modes}")
    for mode in modes:
        config = CommonConfig(default_configs=[], custom_configs=[arg.config], args=arg)
        if mode == 'train':
            do_training(config)
        if mode == 'test':
            do_test(config)
        logger.info(f"{mode} is DONE")
    logger.info('[%s] Finished ' % ' '.join(sys.argv[:]))


if __name__ == "__main__":
    main()
