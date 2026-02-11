from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

try:
    from xgboost import XGBClassifier
except Exception:  # pragma: no cover
    XGBClassifier = None  # type: ignore[assignment]


@dataclass
class SklearnClassifierWrapper:
    estimator: BaseEstimator | None = None
    model: BaseEstimator = field(init=False)

    def __post_init__(self) -> None:
        self.model = self.estimator or Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
            ]
        )

    def fit(self, features: np.ndarray, labels: np.ndarray) -> "SklearnClassifierWrapper":
        self.model.fit(features, labels)
        return self

    def predict(self, features: np.ndarray) -> np.ndarray:
        return self.model.predict(features)

    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(features)
        raise AttributeError("Current estimator does not support predict_proba().")


class XGBoostClassifierWrapper:
    def __init__(self, **kwargs: int | float | str) -> None:
        if XGBClassifier is None:
            raise RuntimeError("xgboost is not installed in this environment.")
        params = {
            "n_estimators": 400,
            "max_depth": 6,
            "learning_rate": 0.05,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "objective": "binary:logistic",
            "eval_metric": "logloss",
            "random_state": 42,
        }
        params.update(kwargs)
        self.model = XGBClassifier(**params)

    def fit(self, features: np.ndarray, labels: np.ndarray) -> "XGBoostClassifierWrapper":
        self.model.fit(features, labels)
        return self

    def predict(self, features: np.ndarray) -> np.ndarray:
        return self.model.predict(features)

    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(features)
