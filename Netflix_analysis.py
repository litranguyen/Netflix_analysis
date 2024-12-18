#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 20:52:22 2024

@author: viviancenguyen
"""

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go


#read the csv file
df = pd.read_csv('netflix_dataset.csv', index_col=0)
print(df.shape)
df.head(100)

#Task1: explore the data
#count number of types that Netflix provides
type_count =df['type'].value_counts()
print(type_count)

#count number of countries. Countries should be unique data
unique_countries = df['country'].nunique()
country_count = df['country'].value_counts()
print(f'Number of unique countries: {unique_countries}')
print(country_count.head())

#count number of genres. Genres should be unique data
unique_genres = df['listed_in'].nunique()
print (f'Number of unique genres:{unique_genres}')

genres_count = df['listed_in'].str.split(', ',expand = True).stack().value_counts()
print (genres_count.head())

#Task 2: visualize a word cloud for the movies
#combine all descriptions into a single string
text = " ".join(descriptions for descriptions in df.description.dropna())

#generate the word cloud
wordcloud = WordCloud(width=800, height = 400, background_color='white').generate(text)

#display the word cloud
plt.Figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

#Task 3: analyze to see if Netflix has invested in new genres in recent years and what age group
#Extract the year from the date_added column
df['date_added']=pd.to_datetime(df['date_added'], errors ='coerce')
df['year_added']=df['date_added'].dt.year

#Analyze Genres
#split the listed_in column into multiple rows
genres_df = df.dropna(subset=['listed_in']).copy()
genres_df = genres_df.set_index(['year_added'])['listed_in'].str.split(', ',expand=True).stack().reset_index(name='genre')

#count the number of shows added per genre per year
genre_trends= genres_df.groupby(['year_added','genre']).size().unstack(fill_value=0)

#analyze Avg groups
#count the number of shows added per rating per year
rating_trends = df.groupby(['year_added', 'rating']).size().unstack(fill_value=0)

# Visualize the Trends
fig = make_subplots(rows=2, cols=1, subplot_titles=("Genre Trends Over the Years", "Rating Trends Over the Years"))

# Add genre trends to the plot
for genre in genre_trends.columns:
    fig.add_trace(go.Scatter(x=genre_trends.index, y=genre_trends[genre], mode='lines', name=genre), row=1, col=1)

# Add rating trends to the plot
for rating in rating_trends.columns:
    fig.add_trace(go.Scatter(x=rating_trends.index, y=rating_trends[rating], mode='lines', name=rating), row=2, col=1)

# Update layout
fig.update_layout(height=800, width=1000, title_text="Netflix Investment Trends in Genres and Age Groups")

# Show the plot
fig.show()


