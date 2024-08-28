import streamlit as st
import pickle
import pandas as pd
import requests
from pathlib import Path
import os

def fetch_poster(movie_id):
    """Fetches the movie poster from the TMDB API using the movie ID."""
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    return None

def recommend(movie):
    """Recommends 5 movies similar to the selected movie."""
    if movie not in movies['title'].values:
        st.write(f"The movie '{movie}' is not found in the dataset.")
        return [], []
    else:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        Recommended_Movies = []
        Recommended_Movies_posters = []

        for i in movie_list:
            movie_id = movies.iloc[i[0]]['id']
            Recommended_Movies.append(movies.iloc[i[0]]['title'])
            # fetch poster
            poster_url = fetch_poster(movie_id)
            if poster_url:
                Recommended_Movies_posters.append(poster_url)
            else:
                Recommended_Movies_posters.append('No Poster Available')

        return Recommended_Movies, Recommended_Movies_posters

# Define the paths using pathlib
similarity_path = Path("C:/Users/Hp/PycharmProjects/Recommendation_System/venv/similarity.pkl")
movies_list_path = Path("C:/Users/Hp/PycharmProjects/Recommendation_System/venv/Movie_list.pkl")

# Print current working directory (for debugging purposes)
st.write(f"Current working directory: {os.getcwd()}")

# Load the files with error handling
try:
    if not movies_list_path.exists():
        st.error(f"Error: The file {movies_list_path} was not found.")
    movies_list = pickle.load(movies_list_path.open('rb'))
except FileNotFoundError:
    st.error(f"Error: The file {movies_list_path} was not found.")
    movies_list = None

try:
    if not similarity_path.exists():
        st.error(f"Error: The file {similarity_path} was not found.")
    similarity = pickle.load(similarity_path.open('rb'))
except FileNotFoundError:
    st.error(f"Error: The file {similarity_path} was not found.")
    similarity = None

# Continue only if both files are loaded successfully
if movies_list is not None and similarity is not None:
    movies = pd.DataFrame(movies_list)

    st.title('Movie Recommender System (Ravi)')

    Selected_Movie_Name = st.selectbox(
        "Select a movie:",
        (movies['title'].values))

    if st.button('Recommend'):
        names, posters = recommend(Selected_Movie_Name)

        # Display recommendations horizontally
        st.write("Recommended Movies:")
        st.write("These are your 5 Suggested Movies List According to Ravi.")

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
