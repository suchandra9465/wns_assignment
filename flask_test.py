from flask import Flask, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

# Define fetch_rows_as_json function
def fetch_rows_as_json(df, conditions):
    combined_condition = None
    for condition in conditions:
        if combined_condition is None:
            combined_condition = condition
        else:
            combined_condition |= condition
    filtered_df = df.loc[combined_condition]
    return filtered_df.to_json(orient='records')

# Define fetch_data_from_mapping function
def fetch_data_from_mapping(json_file, google_sheet_csv):
    # Load data from JSON file
    with open(json_file) as f:
        input_data = json.load(f)
    
    # Read mapping table from Google Sheet CSV
    mapping_table = pd.read_csv(google_sheet_csv)
    
    # Extract input values
    emp_id = int(input_data['emp_id'])
    domicile = str(input_data['domicile'])
    limit = int(input_data['limit'])

    # Convert mapping table to DataFrame
    df = pd.DataFrame(mapping_table)

    message = []
    # Check if input values exist in DataFrame
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

@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    data = request.get_json()
    json_file_path = data.get('json_file')
    google_sheet_csv_path = data.get('google_sheet_csv')
    
    result = fetch_data_from_mapping(json_file_path, google_sheet_csv_path)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
