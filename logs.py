import pandas as pd
import warnings
import os
import keras


class Logger(object):
    def __init__(
        self,
        model: keras.models.Model,
        model_name=None,
        errors="raise",
    ):

        self.model = model
        self.model_name = model_name
        self.errors = errors

        self.logs: pd.DataFrame = pd.read_csv("models/general_log.csv")
        self.model_no = len(self.logs)

        if self.model_name == None:
            self.model_name = f"model_{self.model_no}"

    def log(
        self,
        batch_size,
        epochs,
        seed,
        details="",
        **kwargs,
    ):

        if self.model_name in self.logs["model_name"].values:
            if self.errors == "raise":
                raise ValueError("Model with this name already exists")
            elif self.errors == "warn":
                warnings.warn(
                    f"Model with this name already exists. Changing name to model_{self.model_no}"
                )
                self.model_name = f"model_{self.model_no}"

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            self.logs.loc[self.model_no] = {
                "model_name": self.model_name,
                "start_time": pd.Timestamp.now(),
                "end_time": None,
                "batch_size": batch_size,
                "epochs": epochs,
                "seed": seed,
                "details": details,
                **kwargs,
            }

        os.mkdir(f"models/{self.model_name}")
        self.logs.to_csv("models/general_log.csv", index=False)

    def get_csv_logger(self):
        return keras.callbacks.CSVLogger(
            f"models/{self.model_name}/log.csv", append=True
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.model.save(f"models/{self.model_name}/{self.model_name}.keras")
        self.logs = pd.read_csv("models/general_log.csv")

        # for some reason keras.callbacks.CSVLogger creates additional newlines, loading the file and saving it again removes them
        pd.read_csv(f"models/{self.model_name}/log.csv").to_csv(
            f"models/{self.model_name}/log.csv", index=False
        )

        self.logs.loc[self.model_no, "end_time"] = pd.Timestamp.now()
        self.logs.to_csv("models/general_log.csv", index=False)
        return None
