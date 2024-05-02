from typing import Union, Iterable
from copy import deepcopy

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

from .diff import *


# TODO: Проставить типы
# TODO: is_fitted
# TODO: проверки на int и float


class TimeSeriesDiff(BaseEstimator, TransformerMixin):
    def __init__(
        self, diff_steps: Union[int, Iterable[int]], drop_first_values: bool = True
    ):
        if not hasattr(diff_steps, "__iter__"):
            self.diff_steps = [diff_steps]
        self.drop_first_values = drop_first_values
        self.diff_steps = diff_steps
        self.first_values_ = {s: None for s in self.diff_steps}

    def fit(self, x, y=None):
        if len(x) < max(self.diff_steps):
            raise ValueError(
                "Length of input data X is less than one of the diff_steps values."
            )
        return self

    def transform(self, x):
        transformed_x = deepcopy(x)
        for step in sorted(self.diff_steps):
            self.first_values_[step] = np.array(transformed_x[:step])
            transformed_x = diff(ts=transformed_x, step=step)
        return transformed_x

    def inverse_transform(
        self, x, first_values: Union[Iterable, None] = None
    ) -> np.array:
        if first_values is None:
            first_values = self.first_values_
        untransformed_ts = np.array([])
        for step in reversed(self.diff_steps):
            untransformed_ts = undiff(ts=x, first_values=first_values[step])
            x = untransformed_ts
        print(self.first_values_)
        if self.drop_first_values:
            return untransformed_ts[max(self.diff_steps) :]
        return untransformed_ts
