import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

def fetch_posters(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c1c2d61ea0637dc204db761ca30e7370&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend_movies(movie):
    movie_index=movies[movies['title']==movie].index[0]
    similar_movies=sorted(list(enumerate(similarity[movie_index])),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in similar_movies:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movies.iloc[i[0]].movie_id))
    return recommended_movies,recommended_movies_posters

st.title('Movies Recommendation System')
selected_movie_name=st.selectbox('Which movie would you like to select??',movies['title'].values)
similarity=pickle.load(open('similarity.pkl','rb'))
if st.button('Recommend'):
   names,posters=recommend_movies(selected_movie_name)
   col=st.columns(5)
   for i in range(0,5):
       with col[i]:
           st.text(names[i])
           st.image(posters[i])