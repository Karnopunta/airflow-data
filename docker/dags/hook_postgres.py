# Import library
import pandas as pd
from flatten_json import flatten

# Sample JSON data
json_data = [
    {
        "input": {"first_name": "sandra", "country": "US"},
        "details": {
            "credits_used": 1,
            "duration": "13ms",
            "samples": 9273,
            "country": "US",
            "first_name_sanitized": "sandra",
        },
        "result_found": True,
        "first_name": "Sandra",
        "probability": 0.98,
        "gender": "female"
    }
]

# Flatten JSON data
def flatten_json(json_obj):
    flat_dict = flatten(json_obj, ".")
    return flat_dict

# Create flattened DataFrame
flattened_data = [flatten_json(item) for item in json_data]
df = pd.DataFrame(flattened_data)

# Print DataFrame
print(df)

# Save DataFrame to CSV
csv_path = 'C:/Karno/airflow-data1/docker/dags/df.csv'
df.to_csv(csv_path, index=False)
print(f'Data saved to {csv_path}')
