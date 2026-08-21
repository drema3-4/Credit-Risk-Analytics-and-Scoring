from sklearn.metrics import roc_auc_score, average_precision_score, roc_curve
import numpy as np


def evaluate_ranking(model, X, y) -> dict[str, float]:
    y_score = model.predict_proba(X)[:, 1]

    roc_auc = roc_auc_score(y, y_score)
    pr_auc = average_precision_score(y, y_score)

    fpr, tpr, _ = roc_curve(y, y_score)
    ks = np.max(tpr - fpr)

    return {
        "roc_auc": roc_auc,
        "gini": 2 * roc_auc - 1,
        "ks": ks,
        "pr_auc": pr_auc,
    }