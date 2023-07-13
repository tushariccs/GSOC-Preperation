#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df = pd.read_csv('netflix-rotten-tomatoes-metacritic-imdb.csv')


# In[3]:


df.head()


# In[4]:


df.info()


# In[5]:


df.describe()


# In[6]:


df.isnull().sum()


# In[7]:


df = df.drop(columns = [ 'Metacritic Score', 'Boxoffice', 'Production House', 'Netflix Link', 'IMDb Link',
        'Poster', 'TMDb Trailer', 'Trailer Site'], axis = 1)


# In[8]:


print(df.columns)


# In[9]:


print(df.columns[df.isnull().any()])


# Exploratory data analysis
# 1)What type of content is available? and with what frequency?

# In[10]:


type_counts = df['Series or Movie']
type_counts = type_counts.value_counts()
plt.bar(type_counts.index, type_counts.values,color=['blue','pink'])

# Add labels and title
plt.xlabel('Content Type')
plt.ylabel('Count')
plt.title('Series vs Movies')

# Show the plot
plt.show()


# In[11]:


#All the different tags used in series

series_shows = df[df['Series or Movie'] == 'Series']
series_shows['Tags'].unique()
np.reshape(series_shows['Tags'].unique(),(-1, 1))


# In[12]:


#List of all the different tags used for series

series_tags_array = np.array(series_shows['Tags'].unique())
series_tags_list = series_tags_array.flatten().tolist()
split_series_tags_list = [string.split(',') if isinstance(string, str) else [] for string in series_tags_list]
flattened_series_tags_list = [element for sublist in split_series_tags_list for element in sublist]
print(flattened_series_tags_list)


# In[13]:


#Top 10 tags used for series

series_tags_dict = {}

for item in flattened_series_tags_list:
    if item in series_tags_dict:
        series_tags_dict[item] += 1
    else:
        series_tags_dict[item] = 1
#print(series_tags_dict)

series_tags_df = pd.DataFrame(series_tags_dict.items(), columns=['Tags', 'Count'])
series_tags_df = series_tags_df.sort_values('Count', ascending=False)
top_10_df = series_tags_df.head(10)

colors = ['steelblue', 'mediumseagreen', 'coral', 'purple', 'gold', 'turquoise', 'salmon', 'lime', 'royalblue', 'orange']
top_10_df.plot(kind='bar', x='Tags', y='Count',color = colors, figsize=(10, 6))
plt.xlabel('Tags')
plt.ylabel('Count')
plt.title('Series Tag Frequencies')
plt.show()


# In[14]:


#All the different tags used in movies

movies_shows = df[df['Series or Movie'] == 'Movie']
movies_shows['Tags'].unique()
np.reshape(movies_shows['Tags'].unique(),(-1, 1))


# In[15]:


#List of all the different tags used for movies

movies_tags_array = np.array(movies_shows['Tags'].unique())
movies_tags_list = movies_tags_array.flatten().tolist()
split_movies_tags_list = [string.split(',') if isinstance(string, str) else [] for string in movies_tags_list]
flattened_movies_tags_list = [element for sublist in split_movies_tags_list for element in sublist]
print(flattened_movies_tags_list)


# In[16]:


#Top 10 tags used for movies

movies_tags_dict = {}

for item in flattened_movies_tags_list:
    if item in movies_tags_dict:
        movies_tags_dict[item] += 1
    else:
        movies_tags_dict[item] = 1

movies_tags_df = pd.DataFrame(movies_tags_dict.items(), columns=['Tags', 'Count'])
movies_tags_df = movies_tags_df.sort_values('Count', ascending=False)
top_10_df = movies_tags_df.head(10)

colors = ['steelblue', 'mediumseagreen', 'coral', 'purple', 'gold', 'turquoise', 'salmon', 'lime', 'royalblue', 'orange']
top_10_df.plot(kind='bar', x='Tags', y='Count',color = colors, figsize=(10, 6))
plt.xlabel('Tags')
plt.ylabel('Count')
plt.title('Movie Tag Frequencies')
plt.show()


# The top 10 famous languages on Netflix

# In[17]:


#List of languages

Lang_list = df['Languages'].unique()
lang_df_list = Lang_list.flatten().tolist()

unique_lang_list = []
for item in lang_df_list:
    if isinstance(item, str):
        if ',' in item:
            unique_lang_list.extend(item.split(','))
        else:
            unique_lang_list.append(item)

print(unique_lang_list)


# In[18]:


#Top 10 most popular languages

lang_dict = {}

for item in unique_lang_list:
    if item in lang_dict:
        lang_dict[item] += 1
    else:
        lang_dict[item] = 1

lang_df = pd.DataFrame(lang_dict.items(), columns=['Languages', 'Count'])
lang_df = lang_df.sort_values('Count', ascending=False)
top_10_lang_df = lang_df.head(10)

colors = ['steelblue', 'mediumseagreen', 'coral', 'purple', 'gold', 'turquoise', 'salmon', 'lime', 'royalblue', 'orange']
top_10_lang_df.plot(kind='bar', x='Languages', y='Count',color = colors, figsize=(10, 6))
plt.xlabel('Languages')
plt.ylabel('Count')
plt.title('Languages Frequencies')
plt.show()


# In[19]:


#Graph of number of shows released in the past couple of years

year = df['Netflix Release Date'].str[:4]
year_count = year.value_counts()
year_counts = year_count.sort_index()

plt.figure(figsize=(10, 6))
plt.plot(year_counts.index, year_counts.values,'o-')
plt.xlabel('Year')
plt.ylabel('No. of shows')
plt.title('No. of shows released each year')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


# In[20]:


#Top 10 shows released in 2021

release_date = df[df['Netflix Release Date'].str.contains('2021')]
sorted_titles = release_date.sort_values('IMDb Votes', ascending=False)
top_10_titles = sorted_titles['Title'].head(10).tolist()
for item in top_10_titles:
    print(item)


# In[21]:


# % of different genres


from collections import Counter
Genres = df['Genre']
Genres = Genres.value_counts().index.tolist()
split_Genres_list = [string.split(',') if isinstance(string, str) else [] for string in Genres]
flattened_Genres_list = [element for sublist in split_Genres_list for element in sublist]

item_frequency = dict(Counter(flattened_Genres_list))
sorted_items = dict(sorted(item_frequency.items(), key=lambda x: x[1], reverse=True))
print(sorted_items)

threshold = 30

# Get the items with frequencies above the threshold
main_items = {item: count for item, count in sorted_items.items() if count >= threshold}

# Calculate the frequency sum for the small frequencies
other_frequency = sum(count for item, count in sorted_items.items() if count < threshold)

# Create the "other" item in the dictionary
main_items['other'] = other_frequency

labels = list(main_items.keys())
counts = list(main_items.values())

plt.figure(figsize=(10, 10))
plt.pie(counts, labels=labels, autopct='%1.1f%%')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.title('Genre Frequency')
plt.subplots_adjust(top=1)
plt.show()

