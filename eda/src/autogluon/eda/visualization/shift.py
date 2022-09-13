
from .base import AbstractVisualization
from .jupyter import JupyterMixin
from .. import AnalysisState

class XShiftSummary(AbstractVisualization, JupyterMixin):

    def __init__(self, headers: bool = False, namespace: str = None, **kwargs) -> None:
        super().__init__(namespace, **kwargs)
        self.headers = headers

    def summary(self,
                results: dict) -> str:
        """Output the results of C2ST in a human readable format

        Parameters
        ----------
        results: dict
            Results of xshiftdetector

        Returns
        -------
        str of summary
        """
        if results['detection_status'] == 'not_detected':
            ret_md = (
                f"# Detecting distribution shift\n"
                f"We did not detect a substantial difference between the training and test X distributions."
            )
            return ret_md
        else:
            ret_md = (
                f"# Detecting distribution shift\n"
                f"We detected a substantial difference between the training and test X distributions,\n"
                f"a type of distribution shift.\n"
                f"\n"
                f"## Test results\n"
                f"We can predict whether a sample is in the test vs. training set with a {results['eval_metric']} of\n"
                f"{results['test_statistic']} with a p-value of {results['pvalue']}"
                f"(larger than the threshold of {results['pvalue_threshold']}).\n"
                f"\n"
            )
        if 'feature_importance' in results:
            fi_md = (
                f"## Feature importances\n"
                f"The variables that are the most responsible for this shift are those with high feature importance:\n"
                f"{results['feature_importance'].to_markdown()}"
            )
            return ret_md + fi_md
        return ret_md


    def can_handle(self, state: AnalysisState) -> bool:
        return self._at_least_one_key_must_be_present(state, ['xshift_results'])

    def _render(self, state: AnalysisState) -> None:
        res_md = self.summary(state.xshift_results)
        self.render_markdown(res_md)
        #self.display_obj(state.xshift_results['pvalue'])

