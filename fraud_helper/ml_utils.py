# file: ml_utils.py
# utility libs
import os
import sys
from pathlib import Path
import pickle
from datetime import datetime
# DS and DV libs
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
# ML libs
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_predict
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report, accuracy_score

# set up work env
CURRENT_DIR = Path.cwd()
# please consider to change the value to find your root dir
ROOT_DIR = CURRENT_DIR.parents[0]
sys.path.insert(0, str(ROOT_DIR))
# import utils.dataviz_utils as custom_viz

SEED = 42
MODELS_NAME_NEEDING_SCALING = ["LogisticRegression", "SGDClassifier"]

def plot_consumption_distribution(consumption_df, consumpt_cols, title):
    
    fig, axes = plt.subplots(1, 3)
    fig.suptitle(f"Consumption Level 1 ({title}): Missing vs Not Missing")

    axes = axes.flatten()
    for idx, col_name in enumerate(consumpt_cols):
        sns.boxplot(
        data=consumption_df,
        x="missing_std_1",
        y=col_name,
        ax=axes[idx]
        )

    plt.title(f"{title} - Consumption Means\nMissing vs not Missing std")
    plt.tight_layout()
    plt.show()

# scaling data (only if needed)
def scale_features(X_train, X_test, apply_scaling=False):
    """Apply scale on data only if requested"""
    if not apply_scaling:
        return X_train.values, X_test.values, None
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, scaler

# train a single model
def train_model(model_name, config, X_train, y_train, X_test, scoring="roc_auc", scale=False):
    """Train a single model with or without scaling"""
    print(f"\n{'':10} {model_name} (scaled: {scale})...")

    X_tr, X_te, _ = scale_features(X_train, X_test, scale)
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=SEED)

    grid_search = GridSearchCV(
        config["model"],
        config["params"],
        cv=cv,
        scoring=scoring,
        n_jobs=-1,
        verbose=2
    )
    grid_search.fit(X_tr, y_train)
    
    return grid_search, X_tr, X_te

# evaluate the model and store the summary
def evaluate_and_store(grid_search, X_train, y_train, X_test, model_name, scale):
    """predict and store metric prediction"""
    # train
    y_tr_pred = grid_search.predict(X_train)
    train_acc = accuracy_score(y_train, y_tr_pred)
    train_roc = None
    if hasattr(grid_search.best_estimator_, "predict_proba"):
        train_roc = roc_auc_score(y_train, grid_search.predict_proba(X_train)[:, 1])
        # check overfitting gap
        overfit_gap = train_roc - grid_search.best_score_
        if overfit_gap > 0.1:
            print(f"{'':15}Overfitting! Gap: {overfit_gap:.3f}")

    # test
    y_test_pred = grid_search.predict(X_test)
    y_test_pred_proba = None
    if hasattr(grid_search.best_estimator_, "predict_proba"):
        y_test_pred_proba = grid_search.predict_proba(X_test)[:, 1]

    # put evaluation summary in a dict
    eval_summary = {
        "model": model_name,
        "scaled": scale,
        "train_acc": train_acc,
        "train_roc": train_roc,
        "val_roc": grid_search.best_score_,
        "y_pred": y_test_pred,
        "y_pred_proba": y_test_pred_proba,
        "best_model": grid_search.best_estimator_,
        "best_params": grid_search.best_params_,
        "overfitting_gap": overfit_gap
    }
    return eval_summary

# run training
def run_training(features_sets_dict, models_dict, X_train, y_train, X_test):
    """Run training in all models with all thegiven sets and return a dataframe to analyse the results"""
    results = []

    for feature_name, features in features_sets_dict.items():
        print(f"\n{'='*50}\nFEATURE SET: {feature_name}\n{'='*50}")

        X_train_subset = X_train[features]
        X_test_subset = X_test[features]

        for model_name, config in models_dict.items():
            # train without scaling
            grid_search_not_scaled, X_train_not_scaled, X_test_not_scaled = train_model(
                model_name, config, X_train_subset, y_train,
                X_test_subset, scale=False
            )
            # add the result to the list
            result = evaluate_and_store(
                grid_search_not_scaled, X_train_not_scaled, y_train,
                X_test_not_scaled, model_name, False
            )
            results.append(result)

            # if scaling
            if model_name in MODELS_NAME_NEEDING_SCALING:
                grid_search_scaled, X_train_scaled, X_test_scaled = train_model(
                    model_name, config, X_train_subset, y_train,
                    X_test_subset, scale=True
                )
                result = evaluate_and_store(
                grid_search_scaled, X_train_scaled, y_train,
                X_test_scaled, model_name, True
            )
    # convert the result to a dataframe
    summary_df = pd.DataFrame(results)
    return summary_df

# get confusion matrix
def plot_conf_mat_from_cv(model_name, config, X, y, custom_viz, scale=False):
    X_scaled, _, _ = scale_features(X, X, scale)
    # return prediction
    y_cv_pred = cross_val_predict(config["model"], X_scaled, y, cv=3)
    cm = confusion_matrix(y, y_cv_pred)

    print(f"\n{'':25} Confusion Matrix (from cross val)")
    print(f"\n{'':25} Model Name: {model_name})")
    print(f"[[TN: {cm[0, 0]}, FP: {cm[0, 1]}]]")
    print(f"[[FN: {cm[1, 0]}, TP: {cm[1, 1]}]]")

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(
        data=cm, annot=True,
        fmt="d", cmap=custom_viz.CMAP_PALETTE_02,
        xticklabels=["No Fraud", "Fraud"],
        yticklabels=["No Fraud", "Fraud"],
        ax=ax
    )
    ax.set_title(f"{model_name} Confusion Matrix")
    plt.show()

    return cm

# report
def plot_classification_report_cv(model_name, config, X, y, scale=False):
    "Plot classification report"
    X_scaled, _, _ = scale_features(X, X, scale)
    y_cv_pred = cross_val_predict(config["model"], X_scaled, y, cv=3)

    report = classification_report(y, y_cv_pred, output_dict=True)
    report_df = pd.DataFrame(report)
    print(f"\nReport (before transpose):\n{report_df}")
    report_df = report_df.transpose()
    print(f"\nReport (after transpose):\n{report_df}")
    # plot
    fig, ax = plt.subplots(figsize=(8, 3))
    sns.heatmap(
        report_df[["precision", "recall", "f1-score"]],
        annot=True, fmt=".3f", cmap="RdYlGn", ax=ax
    )
    ax.set_title(f"Classification Report: {model_name}")
    plt.show()

    return report_df

# plot summary
def plot_models_summary(summary_df, custom_viz):
    # display best model
    best_model = summary_df.loc[summary_df["val_roc"].idxmax()]

    print(f"\n    BEST MODEL: {best_model['model']} (scaled: {best_model['scaled']})")
    print(f"{'':10}Val ROC-AUC: {best_model['val_roc']:.3f}")
    print(f"{'':10}Train ROC-AUC: {best_model['train_roc']:.3f}")
    x = np.arange(len(summary_df))
    plt.bar(x, summary_df["val_roc"], color=custom_viz.PALETTE_BLUE[3])
    plt.xticks(
        x, 
        [f"{m}\n({'Scaled' if s else 'Not Scaled'})" for m, s in zip(summary_df["model"], summary_df["scaled"])],
        rotation=45, ha="right"
    )
    plt.title("Cross Val score ROC")
    plt.tight_layout()
    plt.show()

# plot overfitting gap
def plot_overfitting_detection(summary_df, custom_viz):
    sns.barplot(
        data=summary_df,
        x="val_roc",
        y="model",
        hue="scaled",
        palette=custom_viz.MIXED_PALETTE[:2]
    )
    plt.title("Validation ROC AUC")
    plt.xlabel("ROC-AUC")
    plt.tight_layout()
    plt.show()

    # overfitting heatmap
    pivot_df = summary_df.pivot_table(
        values="overfitting_gap",
        index="model", columns="scaled"
    )
    sns.heatmap(
        data=pivot_df, annot=True, cmap="RdYlGn_r",
        center=0.05
    )
    plt.title("Overfitting gap (Train - Val)")
    # plt.tight_layout()
    plt.show()

def analyze_energy_type_fraud(original_train_df, custom_viz):
    """Analyze fraud by energy type (ELEC vs GAZ) - needs original dataframe"""
    # Check if columns exist
    if 'has_elec_sum' not in original_train_df.columns:
        print("ERROR: Need original train_data_df with has_elec_sum column!")
        print(f"Available columns: {original_train_df.columns.tolist()}")
        return None
    
    # Clients with single counter type only
    single_type = original_train_df[original_train_df['counter_type_nunique'] == 1].copy()
    
    # Determine energy type
    single_type['energy_type'] = np.where(single_type['has_elec_sum'] > 0, 'ELEC', 'GAZ')
    
    # Calculate fraud rates
    energy_rate = single_type.groupby('energy_type')['target'].agg(['count', 'mean']).round(3)
    energy_rate.columns = ['Client_Count', 'Fraud_Rate']
    
    print("\nFRAUD RATE BY ENERGY TYPE (Single Counter):")
    print(energy_rate)
    
    # Plot
    plt.figure(figsize=(6, 4))
    sns.barplot(data=energy_rate.reset_index(), x='energy_type', y='Fraud_Rate', 
                palette={'ELEC': custom_viz.MIXED_PALETTE[1], 'GAZ': custom_viz.MIXED_PALETTE[0]})
    plt.title('Fraud Rate by Energy Type (Single Counter)')
    plt.ylabel('Fraud Rate')
    plt.show()
    
    return energy_rate

def analyze_counter_type_fraud(train_data_df, custom_viz):
    """Analyze fraud by number of counter types"""
    # Fraud rate by number of counter types
    rate_by_type = train_data_df.groupby('counter_type_nunique')['target'].agg(['count', 'mean']).round(3)
    rate_by_type.columns = ['Client_Count', 'Fraud_Rate']
    
    print("\nFRAUD RATE BY COUNTER TYPE COUNT:")
    print(rate_by_type)
    
    # Plot
    plt.figure(figsize=(8, 4))
    sns.barplot(data=rate_by_type.reset_index(), x='counter_type_nunique', y='Fraud_Rate', palette=custom_viz.MIXED_PALETTE[:2])
    plt.title('Fraud Rate by Number of Counter Types')
    plt.xlabel('Number of Counter Types')
    plt.ylabel('Fraud Rate')
    plt.ylim(0, rate_by_type['Fraud_Rate'].max() * 1.2)
    plt.show()
    
    return rate_by_type

# Real vs predicted fraud distribution
def plot_fraud_distribution(X_train, y_train, training_summary, main_feature_cols, final_cols):
    best_row = training_summary.loc[training_summary["val_roc"].idxmax()]
    best_model = best_row["best_model"]
    
    features_set_used = best_row.get("features_set", "all_features")
    if features_set_used == "main_features":
        features_used = main_feature_cols
    else:
        features_used = final_cols[: -1]
    # Predict on train data
    X_features = X_train[features_used]
    y_pred_train = best_model.predict(X_features.values)
    
    # Plot
    plt.figure(figsize=(8, 5))
    plt.bar(
        ["Real No Fraud", "Real Fraud", "Pred No Fraud", "Pred Fraud"],
        [
            (y_train == 0).sum(), (y_train == 1).sum(),
            (y_pred_train == 0).sum(), (y_pred_train == 1).sum()
        ],
        color=['#4CAF50', '#F44336', '#4CAF50', '#F44336'],
        alpha=0.7
    )
    plt.title(f'Fraud Distribution: Real vs Predicted ({features_set_used})', fontweight='bold')
    plt.ylabel('Client Count')
    plt.xlabel('')
    plt.legend(title='Fraud')
    plt.tight_layout()
    plt.legend()
    plt.show()
    # Print stats
    print(f"Model: {best_row['model']}")
    print(f"Feature set: {features_set_used} ({len(features_used)} features)")
    print(f"Real fraud: {(y_train == 1).sum()} ({(y_train == 1).mean():.1%})")
    print(f"Pred fraud: {(y_pred_train == 1).sum()} ({(y_pred_train == 1).mean():.1%})")

def fraud_rate_catg_features(train_df, features=["client_catg", "region", "disrict"]):
    for feature in features:
        print(f"\n{'='*50}")
        print(f"FRAUD BY RATE - {feature.upper()}")
        print(f"{'='*50}")

        rate = train_df.groupby(feature)["target"].agg(["count", "mean"]).round(3)
        rate.columns = ["Count", "Fraud_Rate"]
        rate = rate.sort_values("Fraud_Rate", ascending=False)
        print(rate.head(5))
        # plot
        sns.barplot(
            data=rate.head(5).reset_index(),
            x="Fraud_Rate", y=feature
        )
        plt.title(f"Top 5 {feature} by Fraud Rate")
        plt.xlabel("Fraud Rate")
        plt.show()

        # show highest
        print(f"\nHighest fraud rate: {rate.iloc[0]['Fraud_Rate']:.1%} (Category: {rate.index[0]})")
    
def interpret_model_summary(training_summary, df):
    best = training_summary.loc[training_summary["val_roc"].idxmax()]
    print(f"\nBEST: {best['model']} | ROC-AUC: {best['val_roc']:.3f}")
    
    # Check if multi-counter = more fraud
    if 'counter_type_nunique' in df.columns:
        multi = df[df['counter_type_nunique'] > 1]['target'].mean()
        single = df[df['counter_type_nunique'] == 1]['target'].mean()
        print(f"Multi-counter fraud: {multi:.1%} | Single: {single:.1%}")
        print(f"Ratio: {multi/single:.1f}x more fraud" if single > 0 else "N/A")
    
    # Performance interpretation
    if best['val_roc'] > 0.75:
        print("  EXCELLENT fraud detection")
    elif best['val_roc'] > 0.65:
        print("  GOOD performance")
    else:
        print("  NEEDS IMPROVEMENT")

def save_best_model(training_summary, train_samples, features_sets, output_path, author_name="Rackkoun"):
    best_row = training_summary.iloc[training_summary["val_roc"].idxmax()]

    # get actual features
    if "features_set" in best_row:
        features_set_name = best_row["features_set"]
        features_set_used = features_sets[features_set_name]
    else:
        # figure out from model
        model = best_row["best_model"]
        if model.n_features_in_ == len(features_sets["main_features"]):
            features_set_used = features_sets["main_features"]
            features_set_name = "main_features"
        else:
            features_set_used = features_sets["all_features"]
            features_set_name = "all_features"
    print(f"Saving model trained with: {features_set_name} ({len(features_set_used)})")
    model_package = {
        "model": best_row["best_model"],
        "metadata": {
            "author": author_name,
            "model_name": best_row["model"],
            "val_roc_auc": best_row["val_roc"],
            "overfitting_gap": best_row["overfitting_gap"],
            "best_params": best_row.get("best_params", {}),
            "saved_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "features_set": features_set_name,
            "features_used": features_set_used,#main_feature_cols,
            "n_features": len(features_set_used),
            "n_samples": len(train_samples)#len(X_train)
        }
    }
    # create models dir if not exist
    # MODEL_PATH = os.path.join(MODELS_DIR, MODEL_FILE_NAME)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # save to file
    with open(output_path, "wb") as model_file:
        pickle.dump(model_package, model_file)
    print(f"Model saved to: {output_path}")
    print(f"Author: {author_name}")
    print(f"ROC-AUC: {best_row['val_roc']:.3f}")
    return model_package

def load_model(model_path):
    """Load model package from disk"""
    with open(model_path, "rb") as model_file:
        model_pkg = pickle.load(model_file)
    
    model = model_pkg["model"]
    metadata = model_pkg["metadata"]

    print(f"Model loaded from: {model_path}")
    print(f"{''*10}Author: {metadata['author']}")
    print(f"{''*10}ROC-AUC: {metadata['val_roc_auc']}")
    print(f"{''*10}Features: {metadata['features_used']}")

    return model, metadata