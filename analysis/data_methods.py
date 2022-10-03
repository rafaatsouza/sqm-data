import os
import pandas as pd


def get_dataframes():
    return {
        p: {
            'classes': pd.read_csv('../data/{}/class.csv'.format(p)),
            'fields': pd.read_csv('../data/{}/field.csv'.format(p)),
            'methods': pd.read_csv('../data/{}/method.csv'.format(p)),
            'variables': pd.read_csv('../data/{}/variable.csv'.format(p)),
        }
        for p in os.listdir('../data/')
    }

