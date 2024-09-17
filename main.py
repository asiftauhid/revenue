import requests
from bs4 import BeautifulSoup

# URL of the website
url = "https://www.pvrcinemas.lk/"

def scrape_movie_data(url):
    try:
        response = requests.get(url)
        
        # Checking for error
        if response.status_code != 200:
            print("Failed to scrape the webpage!")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        # Adjusting according to the web structure to get the targeted data 
        movies_list = soup.findAll('div', class_="m-content")

        # Storing movie data in a list of dictionaries
        movie_data = []

        for movie in movies_list:
            # Getting the movie names
            movie_names = movie.find('h4', class_="m-title").text.strip()

            # Getting the movie genre
            movie_genres = [genre.text.strip() for genre in movie.findAll('div', class_="m-features")]

            # Adding data to the list (inside the loop)
            movie_data.append({
                "Movie Name": movie_names,
                "Movie Genre": movie_genres
            })

        return movie_data

    except Exception as e:
        print(f"An error has occurred: {e}")
        return []

def main():
    movie_data = scrape_movie_data(url)
    if movie_data:
        for movie in movie_data:
            print(f"Movie Name: {movie['Movie Name']}")
            print(f"Genres: {', '.join(movie['Movie Genre'])}")
            print('-' * 40)
    else:
        print("No movie data found.")

if __name__ == "__main__":
    main()
