import json
import pandas as pd


my_dict={'d': {'count': 0, 'percentage': 0}, 'h':{'count': 0, 'percentage': 0}, 'i':{'count': 0, 'percentage': 0}, 'm': {'count': 0, 'percentage': 0}, 'o': {'count': 0, 'percentage': 0}, 't':{'count': 0, 'percentage': 0}, 'v':{'count': 0, 'percentage': 0}}
data = pd.read_csv("pre_processed_data.csv",delimiter='\t')
for topic in data['Annotation']:
    if topic in my_dict:
        my_dict[topic]['count']+=1
    else:
        pass

for topic in my_dict:
    my_dict[topic]['percentage']=round(my_dict[topic]['count']/964,5)

with open('topic_count.json', 'w') as file:
    json.dump(my_dict, file, indent=4, sort_keys=True)
file.close()