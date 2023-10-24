#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import streamlit as st
import pickle
from pickle import load
from pickle import dump
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings as war
war.filterwarnings('ignore')
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine, correlation

st.title("BOOK RECOMMENDATION SYSTEM")

final_ratings=pickle.load(open("final_ratings.pkl","rb"))
pivot_table=pickle.load(open("pivot_table.pkl","rb"))
user_sim_df=pickle.load(open("usd.pkl","rb"))
user_id_list=user_sim_df.index.values
book_list=pivot_table.columns.values

def get_top_n_similar_users(userid, topn=10):
   # Sort the user IDs by similarity score in descending order
    similar_ids = user_sim_df[userid].sort_values(ascending=False).index.tolist()
    # Remove the user's own ID from the list
    similar_ids.remove(userid)
    # Return the top N similar user IDs
    return similar_ids[:topn]

def recommend_books_to_user(userid,topn=10):
    #Get the most similar users
    similar_users = get_top_n_similar_users(userid,topn=10)
    
    recommended_books = []
    
    for sim_user in similar_users:
        # Filter books rated by the similar user
        sim_user_ratings = final_ratings[final_ratings['userid'] == sim_user]
        
        # Find the top-rated book by the similar user
        top_rated_book = sim_user_ratings.sort_values(by='bookrating', ascending=False).head(1)
        
        top_rated_book_title = top_rated_book['booktitle'].values[0]
        
        # Check if the user has not already rated the book
        if top_rated_book_title not in final_ratings[final_ratings['userid'] == userid]['booktitle'].values:
            recommended_books.append(top_rated_book_title)
    
    return recommended_books                        







#final_ratings=pickle.load(open("final_ratings.pkl","rb"))
#pivot_table=pickle.load(open("pivot_table.pkl","rb"))
#user_sim_df=pickle.load(open("usd.pkl","rb"))
#user_id_list=pivot_table.index.values
#book_list=pivot_table.columns.values

userid = st.selectbox("Select a User ID", user_id_list)

# Button for generating recommendations
if st.button("Generate Recommendations"):
    try:
        userid = int(userid)
        recommended_books = recommend_books_to_user(userid, topn=10)
        st.write(f"Recommended Books for User {userid}:")
        for book_title in recommended_books:
            st.write(f"- Book : {book_title}")
    except ValueError:
        st.error("Please select a valid User ID.")



            
           



                        