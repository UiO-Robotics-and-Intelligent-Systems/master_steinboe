import json

data = {}
data['people'] = []
data['people'].append({
    'name': 'Travis',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
data['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
data['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})

data['cat']=[]
data['cat'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})
print(data)
with open('data.jason', 'w') as outfile:
    json.dump(data, outfile, indent=2)