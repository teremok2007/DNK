import json

data={}
with open('R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper_tmp/data.json', 'r') as f:
    data=json.load(f)
print(data)