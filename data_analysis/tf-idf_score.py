import json



my_dict={'d': {}, 'h':{}, 'i':{}, 'm': {}, 'o': {}, 't':{}, 'v':{}}

with open("most_common_words.json") as f:
    with open("tf-idf.json") as f2:
        data=json.load(f)
        tf_idf_data=json.load(f2)
        for topic in data:
            for i in range(len(data[topic])):
                if data[topic][i] in tf_idf_data[topic]:
                    my_dict[topic][data[topic][i]]=round(tf_idf_data[topic][data[topic][i]],4)
                else:
                    pass
f.close()
with open('tf_idf_score.json', 'w') as file:
    json.dump(my_dict, file, indent=4, sort_keys=True)
