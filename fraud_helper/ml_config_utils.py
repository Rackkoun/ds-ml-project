# file: ml_config.py
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
# ML libs
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier

MAX_ITER = 5000
SEED = 42

# features configs
# maping_dict
# - client catg(3): [11, 12, 51], 
# - disrict(4): [60 69 62 63]
# take the agg content as a dict to automatate the process
invoice_agg_dict = {
    "consommation_level_1": ["count", "sum", "mean", "min", "max", "std"],
    "consommation_level_2": ["count", "sum", "mean", "min", "max", "std"],
    "consommation_level_3": ["count", "sum", "mean", "min", "max", "std"],
    "consommation_level_4": ["count", "sum", "mean", "min", "max", "std"]
}

missing_data_std_1 = [
        "consommation_level_1_count",
        "consommation_level_1_mean",
        "consommation_level_1_std"
]
# close to the final df
final_cols = [
    "disrict", "client_catg", "region", "counter_type_nunique",
    "consommation_level_1_min", "consommation_level_1_mean", "consommation_level_1_max", 
    "consommation_level_2_min", "consommation_level_2_mean", "consommation_level_2_max", 
    "consommation_level_3_min", "consommation_level_3_mean", "consommation_level_3_max", 
    "consommation_level_4_min", "consommation_level_4_mean", "consommation_level_4_max", 
    "target"
]
# define main features
main_feature_cols = [
    "disrict", "client_catg", "region", "counter_type_nunique",
    "consommation_level_1_mean", 
    "consommation_level_2_mean",
    "consommation_level_3_mean",
    "consommation_level_4_mean"
]
# all feats
features_sets = {
    "main_features": main_feature_cols,
    "all_features": final_cols[: -1]
}

# model pipeline
models = {
    "RandomForestClassifier": {
        "model": RandomForestClassifier(class_weight="balanced", random_state=SEED, n_jobs=-1),
        "params": {
            "criterion": ["gini", "entropy", "log_loss"],
            "n_estimators": [50, 100, 200],
            "max_depth": [None,  10]
        }
    },
    "LogisticRegression": {
        "model": LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
        "params": {
            "solver": ["lbfgs", "liblinear", "saga"],
            "C": [0.001, 0.01, 0.1, 1, 10]
        }
    },
    "SGDClassifier":{
        "model": SGDClassifier(max_iter=MAX_ITER, n_jobs=-1, random_state=SEED),
        "params": {
            "loss": ["log_loss"],
            "penalty": ["l1", "l2"],
            "alpha": [0.001, 0.01, 0.1],
            "learning_rate": ["optimal"]
        }
    },
    "DecisionTreeClassifier":{
        "model": DecisionTreeClassifier(random_state=SEED),
        "params": {
            "criterion": ["gini", "entropy", "log_loss"],
            "splitter": ["best", "random"],
            "max_depth": [5, 10]
        }
    }
}