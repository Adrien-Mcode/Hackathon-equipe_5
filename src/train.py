from .raw import get_train
from .preprocess import preprocess
import mlflow
from .utils import save_mlflow_run_id
from .plot import log_stat_desc

def do_training(config):
    run_name = config.model_name + str(config.nrows_train)
    with mlflow.start_run(run_name=run_name) as run:
        run_id = run.info.run_id
        save_mlflow_run_id(run_name, run_id, "save_mlflow_dict.yml")
        train_df = get_train(config)
        log_stat_desc(train_df)
        train_df = preprocess(train_df, config)
        train(train_df, config)



def train(train_df, config):
    pass