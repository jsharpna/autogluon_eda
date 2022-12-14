import pandas as pd
import numpy as np
import autogluon.eda.analysis as eda
import autogluon.eda.auto as auto
import autogluon.eda.visualization as viz

s3_url = 'https://autogluon.s3.us-west-2.amazonaws.com/datasets/AdultIncomeBinaryClassification/'

def load_adult_data():
    train_data = s3_url + 'train_data.csv'
    test_data = s3_url + 'test_data.csv'
    train = pd.read_csv(train_data)
    test = pd.read_csv(test_data)
    data = (train, test)
    return data

def sim_cov_shift(train, test, p_nonmarr = .75, val=False):
    """Simulate covariate shift by biasing training set toward married
    """
    data = pd.concat((train, test))
    data.loc[:,'race'] = data['race'].str.strip()
    data.loc[:,'sex'] = data['sex'].str.strip()
    data.loc[:,'marital-status'] = data['marital-status'].str.strip()
    data.index = pd.Index(range(data.shape[0]))
    data_married = data['marital-status']=="Married-civ-spouse"
    p_married = (0.5 + data_married.mean() - p_nonmarr) / data_married.mean()
    train_p = data_married * p_married + (1 - data_married) * p_nonmarr
    train_ind = np.random.binomial(1,train_p) == 1
    train_cs = data[train_ind]
    test_cs = data[~train_ind]
    if val:
        train_cs, val_cs = model_selection.train_test_split(train_cs)
        return train_cs, val_cs, test_cs
    else:
        return train_cs, test_cs

def test_xsd_cs():
    # assert len(js) == 3
    # assert xsd.decision() == 'detected'
    pass

def test_shift_analysis():
    train, test = load_adult_data()
    analysis_args = dict(
        train_data=train,
        test_data=test,
        label='class',
        classifier_kwargs={'path': 'AutogluonModels'}
    )
    shft_ana = eda.shift.XShiftDetector(**analysis_args)
    shft_ana.fit()
    res = shft_ana.state.xshift_results
    assert all(res[k] is not None for k in ['detection_status', 'pvalue', 'pvalue_threshold', 'eval_metric',
                                  'feature_importance'])
    assert res['detection_status'] == 'not_detected'

def test_shift_auto():
    train, test = load_adult_data()
    analysis_args = dict(
        train_data=train,
        test_data=test,
        label='class',
    )
    shft_args = dict(
        classifier_kwargs={'path': 'AutogluonModels'},
    )
    viz_args = dict(headers=True)
    auto.analyze(**analysis_args, anlz_facets=[
        eda.shift.XShiftDetector(**shft_args)
    ],
    viz_facets=[
         viz.shift.XShiftSummary(**viz_args)
    ]
    )
    pass
