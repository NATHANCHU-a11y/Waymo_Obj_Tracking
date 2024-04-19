import json

# Load JSON file
with open('testing/annotations/instances_val2020.json') as f:
    data = json.load(f)

# Print categories
for category in data['categories']:
    print(category['name'])