import re
import pandas as pd
import numpy as np


def get_dataframes_dict_by_identifier(identifier):
    return {
        'classes': pd.read_csv('../data/{}/class.csv'.format(identifier)),
        'fields': pd.read_csv('../data/{}/field.csv'.format(identifier)),
        'methods': pd.read_csv('../data/{}/method.csv'.format(identifier)),
        'variables': pd.read_csv('../data/{}/variable.csv'.format(identifier)),
    }


def get_dataframes():
    return {
        i: get_dataframes_dict_by_identifier(i)
        for i in ['2019-01', '2020-01', '2020-02', '2022-01', '2022-02']
    }


def get_refacts_dataframes():
    keys_and_identifiers = [
        ('01-refact', '01-command'),
        ('02-refact', '02-questions'),
        ('03-refact', '03-template'),
        ('04-refact', '04-adjusted'),
        ('05-refact', '05-fix'),
        ('06-refact', '06-fix'),
        ('07-refact', '07-fix'),
        ('08-refact', '08-fix'),
        ('09-refact', '09-code-test'),
        ('10-refact', '10-code-test'),
        ('11-refact', '11-code-test'),
        ('current', '2022-02')
    ]
    return {
        t[0]: get_dataframes_dict_by_identifier(t[1])
        for t in keys_and_identifiers
    }


def get_metrics_analysis(df, metrics_by_class, metrics_by_method):
    def _get_data_without_tests(df):
        reg = re.compile(r'.*test.*', re.IGNORECASE)    
        return df[~df['file'].str.match(reg, na=False)]

    analysis = {}
    samples = [
        { 
            'key': 'class', 
            'dfs': {
                'default': df['classes'],
                'not-test': _get_data_without_tests(df['classes']),
            }, 
            'metrics': metrics_by_class,
            'get_metric_content': lambda record, metric: { 
                'class': record['class'], 
                'metric': record[metric],
            }
        },
        { 
            'key': 'method', 
            'dfs': {
                'default': df['methods'],
                'not-test': _get_data_without_tests(df['methods']),
            }, 
            'metrics': metrics_by_method,
            'get_metric_content': lambda record, metric: { 
                'class': record['class'], 
                'method': record['method'], 
                'metric': record[metric],
            }
        },
    ]

    for s in samples:
        key = s['key']
        for df_name, df in s['dfs'].items():
            for metric in s['metrics']:
                avg_metric_classes = np.average(np.array(df[metric].values))
                std_metric_classes = np.std(np.array(df[metric].values))
                top_metric_classes = df[df[metric] > (avg_metric_classes + std_metric_classes)]
                records = [ 
                    s['get_metric_content'](r[1], metric) 
                    for r in top_metric_classes.sort_values(metric, ascending=False).iterrows() 
                ]

                if metric not in analysis:
                    analysis[metric] = {}
                if key not in analysis[metric]:
                    analysis[metric][key] = {}

                analysis[metric][key][df_name] = {
                    'avg': avg_metric_classes,
                    'std': std_metric_classes,
                    'records': records
                }

    return analysis


def get_data_for_top_by_metric(analysis, target, top=10):
    def __get_tuple_by_target(r, target):
        if target == 'method':
            return (r['class'], r['method'][:r['method'].find('/')] if r['method'].find('/') >= 0 else r['method'], r['metric'])
        return (r['class'], r['metric'])

    result = {}
    if target not in ['class', 'method']:
        return result

    for metric, metric_content in analysis.items():
        if target in metric_content:
            result[metric] = {'avg': metric_content[target]['default']['avg'], 'stdev': metric_content[target]['default']['std']}

            not_test_records = [__get_tuple_by_target(r, target) for r in metric_content[target]['default']['records']]
            not_test_records = sorted(not_test_records, key=lambda x: x[len(x)-1], reverse=True)

            if len(not_test_records) > top:
                not_test_records = not_test_records[:top]

            result[metric]["records"] = not_test_records

    return result
