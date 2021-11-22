from json import encoder
import requests
import os
import json
import csv

os.environ['TOKEN'] ='AAAAAAAAAAAAAAAAAAAAAOcUWAEAAAAAxoQu1ivWOCFtTA8dk7HagxhLZEs%3Dy4WsIq7n4mvmUmJfyD78trIxc3I0s1TCddApQXPJdtmYHcmJqb'
bearer_token = os.getenv('TOKEN')

search_url = 'https://api.twitter.com/2/tweets/search/recent'

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
# query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}

query_params = {'query': '(COVID OR vaccination OR pfizer OR moderna OR astrazeneca) (lang:en) (-is:retweet)',
                'max_results': 14, 'start_time': '2021-11-{day}T{start_hour}:00:00Z',
                'end_time': '2021-11-{day}T{end_hour}:59:59Z'}


def bearer_oauth(r):
    r.headers['Authorization'] = f'Bearer {bearer_token}'
    r.headers['User-Agent'] = 'v2RecentSearchPython'
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def extract_to_tsv(json_file):
    with open('data.tsv', 'w', encoding='utf-8') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['Annotation', 'Sentiment', 'Day', 'Text'])

        with open(json_file, 'r') as f:
            data = json.load(f)
            for day, entries_per_day in data.items():
                for entry in entries_per_day:
                    for tweet in entry['data']:
                        tsv_writer.writerow(['', '', day, tweet['text']])


def get_from_last_three_days(params):
    json_response = {'18': [], '19': [], '20': []}
    day = 18

    # loop through every hour of the last 3 days
    while day < 21:
        hour = 0
        while hour < 24:
            params['start_time'] = params['start_time'].format(day=str(day), start_hour=str(hour).zfill(2))
            params['end_time'] = params['end_time'].format(day=str(day), end_hour=str(hour+1).zfill(2))

            json_response[str(day)].append(connect_to_endpoint(search_url, params))
            hour += 1
        day += 1

    return json_response


def main():
    json_response = get_from_last_three_days(query_params)

    with open('data.json','w') as f:
       json.dump(json_response,f,indent=4)

    extract_to_tsv('data.json')


if __name__ == '__main__':
    main()