import pandas as pd
import json


def fetch_rows_as_json(df, conditions):
    combined_condition = None
    for condition in conditions:
        if combined_condition is None:
            combined_condition = condition
        else:
            combined_condition |= condition
    filtered_df = df.loc[combined_condition]
    return filtered_df.to_json(orient='records')

def fetch_data_from_mapping(json_file, google_sheet_csv):
    with open(json_file) as f:
        input_data = json.load(f)
    
    mapping_table = pd.read_csv(google_sheet_csv)
    
    emp_id = int(input_data['emp_id'])
    domicile = str(input_data['domicile'])
    limit = int(input_data['limit'])

    df = pd.DataFrame(mapping_table)

    message = []

    if emp_id not in df['emp_id'].values:
        message.append(f'Input emp_id: "{emp_id}" is missing from the data')
    if domicile not in df['domicile'].values:
        message.append(f'Input domicile: "{domicile}" is missing from the data')
    if limit not in df['limit'].values:
        message.append(f'Input limit: "{limit}" is missing from the data')
    
    conditions = [
        df['emp_id'] == emp_id,
        df['domicile'] == domicile,
        df['limit'] == limit
    ]
    
    json_data = fetch_rows_as_json(df, conditions)
    data = []
    for json_object in json.loads(json_data):
        data.append(json_object)
    result = {
        "data" : data,
        "message": message
    }
    return result
