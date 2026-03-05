import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    # call TMDB API for movie details using the numeric movie_id
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=686cf2e02de2ee92761210e1099462d9&language=en-US"
    response = requests.get(url)
    data = response.json()
    # size can be w500, w300, etc. using w500 here
    return f"https://image.tmdb.org/t/p/w500{data.get('poster_path','')}"

     #ek movie doge tou return  m apko 5 recommended movies k title dega 
def recommend(movie_name):
    # movie_name is a string selected by the user
    # use the movies_df DataFrame to look up the index
    movie_index = movies_df[movies_df['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    # get top 5 similar movies (skip self at index 0)
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters=[]

    # each element of similar_movies is a tuple (movie_index, similarity_score)
    for movie_index, _ in similar_movies:
        # lookup the real TMDB ID from the dataframe
        movie_id = movies_df.iloc[movie_index].movie_id
        recommended_movies.append(movies_df.iloc[movie_index].title)
        # fetch poster using the TMDB ID
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_posters

# load movies DataFrame and keep titles separately
movies_df = pickle.load(open('movies.pkl','rb'))
titles = movies_df['title'].values

similarity = pickle.load(open('similarity.pkl','rb'))

title=st.title('Movies Recommender System')

selected_movie_name = st.selectbox('Select a movie', titles)

if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    
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


