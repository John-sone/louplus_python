import json

list_ = [{
    'user_id': 1000,
    'name': 'Shiyan',
    'pass': 10,
    'study_time': 50,
}, {
    'user_id': 2000,
    'name': 'Lou',
    'pass': 15,
    'study_time': 171,
}]

with open('jsontest.json', 'w') as f:
    f.write(json.dumps(list_))