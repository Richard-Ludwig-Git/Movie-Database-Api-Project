"""programm to manage a Movie-Database with different funktions"""
import statistics
import random
import json
import requests
import movie_storage_sql as movie_storage

API_KEY = '4bd3a055'

def show_main_menu():
    """funktion to print the main menu of the programm"""
    print()
    print("\33[33mMenu:\33[0m")
    print("\33[90m0. Exit\33[0m")
    print("\33[33m1. List movies\33[0m")
    print("\33[33m2. Add movie\33[0m")
    print("\33[33m3. Delete movie\33[0m")
    print("\33[33m4. Update movie\33[0m")
    print("\33[33m5. Stats\33[0m")
    print("\33[33m6. Random movie\33[0m")
    print("\33[33m7. Search movie\33[0m")
    print("\33[33m8. Movies sorted by rating/year\33[0m")
    print("\33[33m9. Generate website\33[0m")
    print()
    return int(input("Enter choice (0-9)"))


def navigate_menu(user_choice):
    """funktion to track the users choice in the menu"""
    if 0 <= user_choice < 10:
        if user_choice == 0:
            print("\33[43m-- till next time --\33[0m")
            exit()
        if user_choice == 1:
            menu_one()
        if user_choice == 2:
            menu_two()
        if user_choice == 3:
            menu_three()
        if user_choice == 4:
            menu_four()
        if user_choice == 5:
            menu_five()
        if user_choice == 6:
            menu_six()
        if user_choice == 7:
            menu_seven()
        if user_choice == 8:
            menu_eight()
        if user_choice == 9:
            menu_nine()
    else:
        print("InMenu")
        print("\33[41mInvalid choice\33[0m")

def menu_one():
    """funktion to list all movies in the Database"""
    movies = movie_storage.list_movies()
    print(f"{len(movies)} movies in total")
    for movie in movies:
        print(f"{movie}: {movies[movie]['rating']} - {movies[movie]['year']}")
    print()
    input("\33[2mPress Enter to continue:\33[0m")


def menu_two():
    """funktion to add a movie in the Database"""
    while True:
        try:
            movie_to_add = input("Enter new movie name:")
            url = f'https://www.omdbapi.com/?i=tt3896198&apikey={API_KEY}&t={movie_to_add}'
            movie_to_add_res = requests.get(url)
            movie_data = json.loads(movie_to_add_res.text)
            if movie_to_add == "":
                raise ValueError
            try:
              movie_rating = movie_data["imdbRating"]
              movie_year = movie_data["Year"]
              movie_poster = movie_data["Poster"]
              movie_storage.add_movie(movie_to_add, movie_year, movie_rating, movie_poster)
            except KeyError:
              print("Movie not found! ")
            print()
            input("\33[2mPress Enter to continue:\33[0m")
            break
        except ConnectionError:
            print("No Connection to API, try again later")
        except ValueError:
            print("\33[41mInvalid entry, try again\33[0m")
            pass
        

def menu_three():
    """funktion to delete a movie in the Database"""
    while True:
        movie_to_delete = input("Enter movie name to delete:")
        if movie_to_delete == "":
            print("\33[41mInvalid entry, try again\33[0m")
            pass
        else:
            break
    movie_storage.delete_movie(movie_to_delete)
    print()
    input("\33[2mPress Enter to continue:\33[0m")

def menu_four():
    """funktion to update a movie in the Database"""
    while True:
        try:
            movie_to_update = input("Enter movie name:")
            if movie_to_update == "":
                raise ValueError
            new_movie_rating = float(input("Enter new movie rating (0-10):"))
            break
        except ValueError:
            print("\33[41mInvalid entry, try again\33[0m")
            pass
    movie_storage.update_movie(movie_to_update, new_movie_rating)
    print()
    input("\33[2mPress Enter to continue:\33[0m")

def menu_five():
    """funktion to display verious stats of the movies in the Database"""
    movies = movie_storage.get_movies()
    rating_sum = 0
    rating_list = []
    movie_and_rating = {}
    for movie in movies:
        rating_sum += movie[2]
        rating_list.append(movie[2])
        movie_and_rating[movie[0]] = movie[2]
    median_ratings = statistics.median(rating_list)
    average_rating = rating_sum/len(movies)
    sorted_movies_by_rating = sorted(movie_and_rating, key=lambda mov_name: movie_and_rating[mov_name], reverse=True)
    print(f"Average rating: {round(average_rating, 1)}")
    print(f"Median rating: {round(median_ratings, 1)}")
    print(f"Best movie: {sorted_movies_by_rating[0]}, \33[32m{movie_and_rating[sorted_movies_by_rating[0]]}\33[0m")
    print(f"Worst movie: {sorted_movies_by_rating[-1]}, \33[32m{movie_and_rating[sorted_movies_by_rating[-1]]}\33[0m")
    print()
    input("\33[2mPress Enter to continue:\33[0m")

def menu_six():
    """funktion to show a random movie in the Database"""
    movies = movie_storage.get_movies()
    random_movie = random.randrange(len(movies)-1)
    print(f"Your movie for tonight: {movies[random_movie][0]}, its rated {movies[random_movie][2]}")
    print()
    input("\33[2mPress Enter to continue:\33[0m")

def menu_seven():
    """funktion to search a movie in the json file"""
    movies = movie_storage.get_movies()
    user_search = input("Enter part of movie name:")
    for movie in movies:
        if user_search.lower() in movie[0].lower():
            print(f"{movie[0]}, {movie[2]}")
    print()
    input("\33[2mPress Enter to continue:\33[0m")

def menu_eight():
    """funktion to list all movies in the json file, sorted by year or rating"""
    movies = movie_storage.get_movies()
    movie_and_rating = {}
    movie_and_year = {}
    for movie in movies:
        movie_and_rating[movie[0]] = movie[2]
        movie_and_year[movie[0]] = movie[1]
    sorted_movies_by_rating = sorted(movie_and_rating, key=lambda mov_name: movie_and_rating[mov_name], reverse=True)
    user_sort_choice = ""
    while user_sort_choice != "rating" or user_sort_choice != "year":
        user_sort_choice = input("Movies sorted by rating or year (Type your choice): ")
        if user_sort_choice == "rating":
            for movie in sorted_movies_by_rating:
                print(f"{movie}: {movie_and_rating[movie]}")
            break
        if user_sort_choice == "year":
            user_order_choice = ""
            while user_order_choice != "o" or user_order_choice != "n":
                try:
                    user_order_choice = input("Do you want to see the oldest or the newest first?(Enter o/n) ")
                    if user_order_choice == "o":
                        sorted_movies_by_year = sorted(movie_and_year, key=lambda mov_name: movie_and_year[mov_name], reverse=False)
                    elif user_order_choice == "n":
                        sorted_movies_by_year = sorted(movie_and_year, key=lambda mov_name: movie_and_year[mov_name], reverse=True)
                    for movie in sorted_movies_by_year:
                        print(f"{movie}: {movie_and_year[movie]}")
                    break
                except UnboundLocalError:
                    print("\33[41mInvalid entry, try again\33[0m")
                    pass
            break
        print("\33[41mInvalid entry, try again\33[0m")
    print()
    input("\33[2mPress Enter to continue:\33[0m")


def menu_nine():
    """ Loads a HTML Tamplate """
    with open('_static/index_template.html', encoding="UTF-8", errors="ignore") as gettemp:
      template_site = gettemp.read()
      template_site_with_name = template_site.replace("__TEMPLATE_TITLE__", "********** RMDB **********")
      movies = movie_storage.get_movies()
      output = ""
      for movie in movies:
        output += f'<li>\n<div class="movie">\n<img class="movie-poster"\n src={movie[3]}/>\n<div class="movie-title">{movie[0]}</div>\n<div class="movie-year">{movie[1]}</div>\n</div>\n</li>\n'
      temp_with_data = template_site_with_name.replace("__TEMPLATE_MOVIE_GRID__", output)
      with open("_static/index.html", "w") as makepage:
        makepage.write(temp_with_data) 
    print("Website was generated successfully.")
    print()
    input("\33[2mPress Enter to continue:\33[0m")


def main():
    """main funktion with a while loop to bring the main menu back, over and over again"""
    print("\33[43m********** RMDB **********\33[0m")
    while True:
        try:
            user_choice = show_main_menu()
            navigate_menu(user_choice)
        except ValueError:
            print("InMain")
            print("\33[41mInvalid choice\33[0m")

if __name__ == "__main__":
    main()
