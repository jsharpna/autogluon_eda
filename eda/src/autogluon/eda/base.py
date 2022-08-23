from __future__ import annotations

import inspect
import logging
from abc import ABC, abstractmethod
from typing import List, Union, Type

from pandas import DataFrame

from autogluon.eda.backend.base import RenderingBackend, EstimatorsBackend

logger = logging.getLogger(__name__)


class AbstractAnalysis(ABC):

    def __init__(self,
                 train_data: Union[str, DataFrame] = None,
                 test_data: Union[str, DataFrame] = None,
                 tuning_data: Union[str, DataFrame] = None,
                 fitted_predictor=None,
                 problem_type: str = None,
                 label: str = None,
                 eval_metric=None,
                 sample = None,
                 rendering_backend: Union[RenderingBackend, Type[RenderingBackend]] = None,
                 estimators_backend: Type[EstimatorsBackend] = None,
                 children: List[AbstractAnalysis] = [],
                 **kwargs) -> None:
        self.sample = sample
        self.estimators_backend = estimators_backend
        self.tuning_data = tuning_data
        self.test_data = test_data
        self.train_data = train_data
        self.eval_metric = eval_metric
        self.label = label
        self.problem_type = problem_type
        self.fitted_predictor = fitted_predictor
        self.children: List[AbstractAnalysis] = children

        if inspect.isclass(rendering_backend):
            rendering_backend = rendering_backend()
        self.rendering_backend = rendering_backend

        self.model = None
        self._kwargs = kwargs

    @abstractmethod
    def fit(self, **kwargs):
        """
        Fit composing EDA primitives.
        """
        raise NotImplemented

    def render(self, **kwargs):
        """
        Fit composing EDA primitives.
        """
        if self.model is None:
            raise ValueError('Analysis is not fit yet, please use fit() before rendering.')
        if self.rendering_backend is None:
            logger.warning(f'Component {self.__class__} has no rendering_backend')
        else:
            self.rendering_backend.render(self.model)

    def _datasets_as_map(self):
        return {
            'train_data': self.train_data,
            'test_data': self.test_data,
            'tuning_data': self.tuning_data
        }

    def _get_datasets(self):
        return self.model['datasets']

    def _sample_and_set_model_datasets(self):
        self.model['datasets'] = {}
        for t, ds in self._datasets_as_map().items():
            if ds is not None:
                if self.sample is not None:
                    if len(ds) > self.sample:
                        ds = ds.sample(self.sample)
                self.model['datasets'][t] = ds