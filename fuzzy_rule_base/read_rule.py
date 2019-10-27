import pandas as pd
import xlrd
from pathlib import Path

def get_workbook():
    data_folder = Path("../rule")
    file_to_open = data_folder / 'fuzzy_rule.xlsx' # '../rule/fuzzy_rule.xlsx'
    return file_to_open

def read_light_rule():
    light_rule = []
    
    with xlrd.open_workbook(get_workbook()) as book:
        sheet = book.sheet_by_index(1)

        distance = [x for x in sheet.col_values(1)]
        light_status = [y for y in sheet.col_values(2)]
        angle = [z for z in sheet.col_values(3)]
        speed = [t for t in sheet.col_values(4)]

        for i in range(1, len(distance)):
            light_rule.append((distance[i].strip(), light_status[i].strip(), angle[i].strip(), speed[i].strip()))

    return light_rule


def read_impediment_rule():
    impediment_rule = []
    with xlrd.open_workbook(get_workbook()) as book:
        sheet = book.sheet_by_index(0)

        distance = [x for x in sheet.col_values(1)]
        angle = [y for y in sheet.col_values(2)]
        speed = [z for z in sheet.col_values(3)]

        for i in range(1, len(distance)):
            impediment_rule.append((distance[i].strip(), angle[i].strip(), speed[i].strip()))

    return impediment_rule

def read_fuzzy_initial_values():
    df = pd.read_excel(get_workbook(), sheet_name='fuzzy_values_initalize')
    return df

def read_fuzzy_values():
    df = pd.read_excel(get_workbook(), sheet_name='fuzzy_values')
    return df

def query_fuzzy_individual_values(df_base, query, required_cols = 4):
    df = df_base[(df_base.rule == query)]
    if(required_cols==3):
        return df['a'].iloc[0], df['b'].iloc[0], df['c'].iloc[0]
    else:
        return df['a'].iloc[0], df['b'].iloc[0], df['c'].iloc[0], df['d'].iloc[0]

def query_fuzzy_values(df_base, query):
    df = df_base[(df_base.rule == query)]
    return df['start'].iloc[0], df['stop'].iloc[0], df['step'].iloc[0]
