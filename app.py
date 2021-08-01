import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import requests

load_dotenv()

#initializing the variables from environment.
connection_string = os.getenv('CONNECTION_STRING')
api_key = os.getenv('API_KEY')

def get_database_connection(connection_string):
    return MongoClient(connection_string)

def odds_in_play(api_key, sport_key='upcoming'):

    odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
        'api_key': api_key,
        'sport': sport_key,
        'region': 'uk', 
        'mkt': 'h2h' 
    })
    return odds_response

def get_all_sports(api_key):
    sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
        'api_key': api_key
    })
    return sports_response

sports_response = get_all_sports(api_key)
sports_json = json.loads(sports_response.text)
sports = sports_json['data']


odds_response = odds_in_play(api_key)
odds_json = json.loads(odds_response.text)
odds = odds_json['data']

#Get the database connection from the string
connection = get_database_connection(connection_string)

#Run the below code lines just once
# Creates the database and the sports and odds collections. 
db = connection.betme
all_sports_collection = db.all_sports
odds_collection = db.odds

#inserts the data from the api call onto the database
sports_insert = all_sports_collection.insert_many(sports)
odds_insert = odds_collection.insert_many(odds)


#Querying the database and projecting only the required values.
my_query = {'sport_key':'soccer_russia_premier_league'}
project = {'sites': 1}
a = odds_collection.find(my_query,project)
for item in a:
    print(item)

