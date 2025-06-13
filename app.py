import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# URLs to your Google Drive files (must be set to 'Anyone with the link can view')
SIMILARITY_URL = 'https://drive.google.com/uc?id=1bVy5FeHmf2WdzqXla6-J9GDoplCRN_nI'
MOVIE_DICT_URL = 'https://drive.google.com/uc?id=1-L4yfLil56gXgVk2iCUQTln-lxrJvGjh'

# Download files if not already present
if not os.path.exists("similarity.pkl"):
    gdown.download(SIMILARITY_URL, "similarity.pkl", quiet=False)

if not os.path.exists("movie_dict.pk1"):
    gdown.download(MOVIE_DICT_URL, "movie_dict.pk1", quiet=False)



def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0d59572307968f58a7534f996d3e7176&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        #fetchposterfromAPI
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0d59572307968f58a7534f996d3e7176&language=en-US'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


movies_dict = pickle.load(open("movie_dict.pk1", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")


Selected_movie_name = st.selectbox(
    "how would you like to contacted",
    movies["title"].values)

if st.button("Recommend"):

    names, posters = recommend(Selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
