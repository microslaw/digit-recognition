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

        self.logs: pd.DataFrame = pd.read_csv("models/log.csv")
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

        self.logs.loc[self.model_no] = {
            "model_name": self.model_name,
            "start_time": pd.Timestamp.now(),
            "end_time": None,
            "batch_size": batch_size,
            "epochs": epochs,
            "test_accuracy": None,
            "test_loss": None,
            "train_accuracy": None,
            "train_loss": None,
            "seed": seed,
            "details": details,
            **kwargs,
        }

        if self.model_name in self.logs["model_name"].values:
            if self.errors == "raise":
                raise ValueError("Model with this name already exists")
            elif self.errors == "warn":
                warnings.warn("Model with this name already exists")

        os.mkdir(f"models/{self.model_name}")
        self.model.save(f"models/{self.model_name}/{self.model_name}.keras")
        self.logs.to_csv("models/log.csv", index=False)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.logs = pd.read_csv("models/log.csv")
        self.logs.loc[-2, "end_time"] = pd.Timestamp.now()
        # add update parameters
        self.logs.to_csv("models/log.csv", index=False)
        return None
