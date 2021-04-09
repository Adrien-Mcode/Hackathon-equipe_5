import argparse
import logging
import sys

logger = logging.getLogger(__name__)


def parse_command_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, nargs='+',
                        help='execution mode: train, test',
                        default=['train'])
    parser.add_argument('-s', '--step', type=str, nargs='+',
                        help='execution step: all, raw, preprocess, training, predict, eval',
                        default='all')
    parser.add_argument('--config', default='src/conf_run.yml')
    return parser.parse_args()


def main():
    arg = parse_command_args()
    logger.debug("running with debug level logs")
    logger.info('[%s] Started ' % ' '.join(sys.argv[:]))
    modes = [x for x in arg.mode]
    logger.info(f"will run modes : {modes}")
    for mode in modes:
        config = (YamlConfig()
                  .from_args(arg)
                  .from_model_args(arg)
                  .from_db_args(arg)
                  .get_grain_perimeter()
                  .get_mode_dates(mode))
        state = GlobalState(config)
        if mode == 'train':
            do_training(state, config)
        if mode == 'test':
            do_test(state, config)
        if mode == 'predict':
            do_predict(state, config)
        logger.info(f"{mode} is DONE")
    logger.info('[%s] Finished ' % ' '.join(sys.argv[:]))


if __name__ == "__main__":
    main()





if __name__ == '__main__':
