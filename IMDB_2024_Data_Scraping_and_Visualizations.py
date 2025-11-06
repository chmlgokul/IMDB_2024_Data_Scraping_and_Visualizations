from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://www.imdb.com/search/title/?year=2024&title_type=feature"
driver.get(url)
time.sleep(3)

# Locate all movie cards
movies = driver.find_elements(By.XPATH, "//li[@class='ipc-metadata-list-summary-item']")

movie_names = []
movie_ratings = []
movie_genres = []
movie_runtimes = []

for movie in movies:
    # Movie name
    try:
        name = movie.find_element(By.XPATH, ".//h3[contains(@class, 'ipc-title__text')]").text
        if '. ' in name:
            name = name.split('. ', 1)[1]
    except:
        name = "N/A"

    # Rating
    try:
        rating = movie.find_element(By.XPATH, ".//span[contains(@class,'ipc-rating-star--imdb')]").text.split('\n')[0]
    except:
        rating = "N/A"

    # Runtime (usually in <li> containing 'h' or 'm')
    try:
        runtime = movie.find_element(By.XPATH, ".//ul[contains(@class,'metadata-list')]/li[contains(text(),'h') or contains(text(),'m')]").text
    except:
        runtime = "N/A"

    # Genre (usually after runtime)
    try:
        genre_list = movie.find_elements(By.XPATH, ".//span[@class='ipc-chip__text']")
        if genre_list:
            genre = ", ".join([g.text for g in genre_list])
        else:
            genre = "N/A"
    except:
        genre = "N/A"

    movie_names.append(name)
    movie_ratings.append(rating)
    movie_genres.append(genre)
    movie_runtimes.append(runtime)

driver.quit()


# Create DataFrame
data = pd.DataFrame({
    "Movie Name": movie_names,
    "Genre": movie_genres,
    "Runtime": movie_runtimes,
    "Rating": movie_ratings
})
data.index = range(1, len(data) + 1)

print("Scraped successfully!")
print(data.head())

data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce')
data.to_csv("imdb_2024_movies.csv", index=False)
print("Data saved as imdb_2024_movies.csv")

print(data.info())
print(data.describe())
print(data['Genre'].value_counts().head(10))



# Load data
data = pd.read_csv("imdb_2024_movies.csv")

st.title("IMDB 2024 Movie Data Dashboard")

# Sidebar filter
selected_genre = st.sidebar.selectbox("Choose a Genre", options=["All"] + list(data['Genre'].unique()))
if selected_genre != "All":
    data = data[data['Genre'] == selected_genre]

# Show data
st.subheader("Movie List")
st.dataframe(data)

# Rating distribution
st.subheader("Rating Distribution")
fig, ax = plt.subplots()
ax.hist(data['Rating'].dropna(), bins=10)
ax.set_xlabel("Rating")
ax.set_ylabel("Number of Movies")
st.pyplot(fig)