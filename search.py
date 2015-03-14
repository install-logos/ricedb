import json
from pprint import pprint

def search(json_file,target_val,field):
    target_id = 10
    json_data = open(json_file)

    data = json.load(json_data)
    json_data.close()
    found = False

    for obj in data:
        if obj[field] == target_val:
            return obj

    return 'Not Found'
