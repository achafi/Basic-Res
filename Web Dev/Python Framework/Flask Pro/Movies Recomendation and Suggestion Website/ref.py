import pandas as pd
from math import sqrt
import numpy as np
import substring
import json
import requests
from isodate import parse_duration


with open("info.json", "r") as c:
    parameters = json.load(c)["parameters"]

search_url = 'https://www.googleapis.com/youtube/v3/search'
video_url = 'https://www.googleapis.com/youtube/v3/videos'

movies_df = pd.read_csv('./dataset/movies_df.csv')
ratings_df = pd.read_csv('./dataset/ratings.csv')  
moviesWithGenres_df = pd.read_csv('./dataset/moviesWithGenres.csv')


def predict(userInput, q):
    inputMovies = pd.DataFrame(userInput)
    inputId = movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]

    inputMovies = pd.merge(inputId, inputMovies)
    inputMovies = inputMovies.drop('genres', 1).drop('year', 1)

    userMovies = moviesWithGenres_df[moviesWithGenres_df['movieId'].isin(inputMovies['movieId'].tolist())]
    userMovies = userMovies.reset_index(drop=True)

    userGenreTable = userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)

    userProfile = userGenreTable.transpose().dot(inputMovies['rating'])

    genreTable = moviesWithGenres_df.set_index(moviesWithGenres_df['movieId'])
    genreTable = genreTable.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)

    recommendationTable_df = ((genreTable*userProfile).sum(axis=1))/(userProfile.sum())
    recommendationTable_df = recommendationTable_df.sort_values(ascending=False)

    x = movies_df.loc[movies_df['movieId'].isin(recommendationTable_df.head(int(q)).keys())]
    x = x['title']

    a = []
    for i in x:
        a.append(i)
    return a


def view(r):
    x = movies_df
    x = x.head(r)
    title = x['title']
    a = []
    for i in title:
        b = []
        q= i[0]
        z = substring.substringByChar(i, startChar=q, endChar="(")
        z = z[:len(z)-1]
        s = substring.substringByChar(i, startChar="(", endChar=")")
        b.append(z)
        b.append(s)
        a.append(b)
    return a


def youvideoauth(x):
    videos = []

    for i in x:
        search_params = {
            'key' : parameters['key'],
            'q' : i,
            'part' : 'snippet',
            'maxResults' : 1,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []

        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
                'key' : parameters['key'],
                'id' : ','.join(video_ids),
                'part' : 'snippet,contentDetails',
                'maxResults' : 1
            }
        
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']

        for result in results:
            video_data = {
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'title' : result['snippet']['title'],
                }
            videos.append(video_data)
    return videos


def searchds(k):
    x = movies_df
    title = x['title']
    for j in title:
        if k == j:
            return ("Found")

    return "Not found"
    

def youvideo():
    a = [{'id': 'jo505ZyaCbA', 'url': 'https://www.youtube.com/watch?v=jo505ZyaCbA', 'thumbnail': 'https://i.ytimg.com/vi/jo505ZyaCbA/hqdefault.jpg', 'duration': 2, 'title': 'The Beatles - Yesterday'}, {'id': 'k4V3Mo61fJM', 'url': 'https://www.youtube.com/watch?v=k4V3Mo61fJM', 'thumbnail': 'https://i.ytimg.com/vi/k4V3Mo61fJM/hqdefault.jpg', 'duration': 4, 'title': 'Coldplay - Fix You (Official Video)'}, {'id': 'IXdNnw99-Ic', 'url': 'https://www.youtube.com/watch?v=IXdNnw99-Ic', 'thumbnail': 'https://i.ytimg.com/vi/IXdNnw99-Ic/hqdefault.jpg', 'duration': 4, 'title': 'Pink Floyd - Wish You Were Here'}]
    return a
