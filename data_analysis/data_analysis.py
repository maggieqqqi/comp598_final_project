import json
import pandas as pd
import math
from collections import Counter

categories_json = {
        'i': {},
        'v': {},
        'm': {},
        'd': {},
        't': {},
        'h': {},
        'o': {},
    }

def compute_tf_idfs(word_counts_json):
    tf_idf_output = categories_json

    for (annotation,text) in word_counts_json.items():
        for (word, count) in text.items():
            tf = count
            idf = compute_idf(word_counts_json,word)
            tf_idf_output[annotation][word] = tf*idf

    with open('./tf-idf.json', 'w') as file:
        json.dump(tf_idf_output, file, indent=4, sort_keys=True)

    output_tf_idf = {}
    common_words_array = []
    for (annotation, words) in tf_idf_output.items():
        most_common_words = Counter(words).most_common(10)
        for common_word in most_common_words:
            common_words_array.append(common_word[0])
        output_tf_idf[annotation] = common_words_array
        common_words_array = []

    with open('./most_common_words.json', 'w') as file:
        json.dump(output_tf_idf, file, indent=4, sort_keys=True)
    return output_tf_idf

def compute_idf(word_counts_json,word):
    total_number_of_annotations = len(word_counts_json.keys())
    number_of_annotations_that_use_word = 0

    for (annotation,words) in word_counts_json.items():
        if word in words:
            number_of_annotations_that_use_word += 1
            continue
    
    if number_of_annotations_that_use_word == 0:
        return 0
    return math.log(float(total_number_of_annotations / number_of_annotations_that_use_word))


def compute_word_counts(data):
    stopwords_file = open('stopwords.txt', 'r')
    stopwords = stopwords_file.read().splitlines()
    stopwords_file.close()

    data_df = preprocess_data(data)
    output = categories_json

    for i in range(len(data_df['Annotation'])):
        annotation = str(data_df.iloc[i,0])

        for word in data_df.iloc[i,1].split():
            if word not in stopwords and word.isalpha():
                if word not in output[annotation]:
                    output[annotation][word] = 1
                else:
                    output[annotation][word] += 1

    # remove elements with less than 5 words
    for (name,words) in output.copy().items():
        for (word,count) in words.copy().items():
            if count < 2:
                del output[name][word]

    with open('./word_count.json', 'w') as file:
        json.dump(output, file, indent=4, sort_keys=True)
    return output

def preprocess_data(data):
    df = data[['Annotation','Text']]
    
    # remove punctuation
    df['Text'] = df['Text'].str.replace('https(.*)',' ',regex=True).replace('#', ' ', regex=True).replace('[()\[\],-.?!;:#&]', ' ', regex=True).replace('@\w+','',regex=True)
    df.dropna(how='any', inplace=True)

    # make all words lower case
    for i in range(len(df['Text'])):
      df.iloc[i, 0] = df.iloc[i, 0].lower()
      df.iloc[i, 1] = df.iloc[i, 1].lower()

    df.to_csv('pre_processed_data.csv',sep='\t')
    return df

def main():
    tsv_file = open('data.tsv')
    data = pd.read_csv(tsv_file,delimiter='\t')

    word_counts = compute_word_counts(data)
    compute_tf_idfs(word_counts)

if __name__ == '__main__':
    main()