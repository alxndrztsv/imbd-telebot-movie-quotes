import telebot
from scraper import Scraper
from dictionary import Dictionary
import random

TOKEN = '**********************************************'
bot = telebot.TeleBot(TOKEN)

# useless but anyway
# create a dictionary object
dict = Dictionary()
# get all movies {code: title}
movies = dict.get_dict
# create an empty dictionary that will store similar movies {code: title}
chosen_movies = {}
# a variable will store particular movie
movie_quotes = []


# # method represents binary search
# def binary_search(array, x):
#     low = 0
#     high = len(array) - 1
#
#     while low <= high:
#         mid = (high + low) // 2
#         if array[mid][1] < x:
#             low = mid + 1
#         elif array[mid][1] > x:
#             high = mid - 1
#         else:
#             return array[mid]
#     # There is no such item
#     return -1


# method gets all quotes from the page
def get_quotes(code):
    url = 'https://www.imdb.com/title/' + code + '/quotes'
    scraper = Scraper(url)
    return scraper.quotes


# create start method
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = 'Hello, this is a movie quotes bot from IMBD.com\n' \
                   'Type words from the title of the movie you want.'
    bot.send_message(message.chat.id, welcome_text)


@bot.message_handler(content_types=['text'])
def send_message(message):
    # user's input
    users_title = message.text
    # tup = binary_search(movies, title)
    # iterate through all movies
    for movie_id, movie_title in movies.items():
        # if the movie title contains user's input
        # add to our dictionary with movies
        if users_title.lower() in movie_title.lower():
            chosen_movies[movie_id] = movie_title
    # if there is no movies
    if not chosen_movies:
        no_text = 'There is no such movie or ' \
                  'there are no quotes for this movie.'
        bot.send_message(message.chat.id, no_text)
    # check if there are several matches
    elif len(chosen_movies) > 1:
        choose = ''
        count = 0
        # iterate through a new dictionary
        # to give the user opportunity to chose
        for movie_id, movie_title in chosen_movies.items():
            choose += '{}) for \"{}\"\n'.format(str(count + 1), movie_title)
            count += 1
        text = 'Please select:\n' + choose.strip()
        # send a message to make user select a movie
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, choose_movie)
    # if there is only one movie in the new dictionary
    else:
        # get all quotes from the movie
        quotes = get_quotes(list(chosen_movies.keys())[0])
        # make the variable global to get it from other methods
        global movie_quotes
        movie_quotes = quotes.copy()
        bot.send_message(message.chat.id, random.choice(quotes))
        ask_repeat(message)


# method receives the user's choice (1... 2...)
# and sends quotes from the chosen movie
def choose_movie(message):      # slow
    users_number = message.text
    try:
        # choose a proper movie from the dict with chosen movies
        movie_id = list(chosen_movies.keys())[int(users_number) - 1]
        quotes = get_quotes(movie_id)
        global movie_quotes
        movie_quotes = quotes.copy()
        bot.send_message(message.chat.id, random.choice(quotes))
        ask_repeat(message)
    except:
        wrong_input_text = 'Wrong input. Try again.'
        bot.send_message(message.chat.id, wrong_input_text)
        bot.register_next_step_handler(message, choose_movie)


def send_another_quote(message):        # too slow
    if message.text.lower() == 'more':
        bot.send_message(message.chat.id, random.choice(movie_quotes))
        ask_repeat(message)
    else:
        # clear all data to add new next time
        chosen_movies.clear()
        movie_quotes.clear()
        send_welcome(message)


# method sends another random quote from the movie
def ask_repeat(message):
    repeat_text = '\'More\' for another quote.'
    bot.send_message(message.chat.id, repeat_text)
    bot.register_next_step_handler(message, send_another_quote)


bot.polling(none_stop=True, interval=20)
