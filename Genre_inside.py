#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 22:06:56 2024

@author: viviancenguyen

Purpose of this query is to find what the most frequent movie duration in 2000s
"""

import pandas as pd
import matplotlib.pyplot as plt

#read the csv file
df = pd.read_csv('netflix_dataset.csv', index_col=0)
print(df.shape)

#sort out "Movie" genre
genre = df[df['type']=='Movie']
movies = genre[genre['release_year'] >= 1990]
subset_movies = movies[movies['release_year'] <2000]

#count the number of unique type
unique_type = subset_movies['listed_in'].nunique()

#split the type into seperate rows
genres_df = subset_movies.dropna(subset=['listed_in']).copy()
genres_df = genres_df['listed_in'].str.split(', ',expand=True).stack().reset_index(name='genre')
grouped = genres_df.groupby('genre')

for genre,group in grouped:
    plt.hist(group[''])

#create the graph
plt.hist(subset_movies, bins=3)
plt.title('Distribution of Movie Duration in the 1990s')
plt.xlabel('Duration (minute)')
plt.ylabel('Number of Movies')
plt.show()

