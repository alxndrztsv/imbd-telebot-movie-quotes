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
    # create a dictionary with chosen movies
    chosen_movies = {}
    # user's input
    users_title = message.text
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
            choose += '{}. for \"{}\"\n'.format(str(count + 1), movie_title)
            count += 1
        text = 'Please select:\n' + choose.strip()
        # check if there are a lot of movies
        if count > 100:
            long_text = 'Message is too long, please narrow your search.'
            bot.send_message(message.chat.id, long_text)
            chosen_movies.clear()
        else:
            # send a message to make user select a movie
            bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(message, lambda x: choose_movie(x, chosen_movies))
    # if there is only one movie in the new dictionary
    else:
        # get all quotes from the movie
        quotes = get_quotes(list(chosen_movies.keys())[0])
        # create a list with quotes of a particular movie
        movie_quotes = quotes.copy()
        bot.send_message(message.chat.id, random.choice(quotes))
        ask_repeat(message, movie_quotes)


# method receives the user's choice (1... 2...)
# and sends quotes from the chosen movie
def choose_movie(message, chosen_movies):
    users_number = message.text
    if users_number == '/start':
        send_welcome(message)
    try:
        # choose a proper movie from the dict with chosen movies
        movie_id = list(chosen_movies.keys())[int(users_number) - 1]
        quotes = get_quotes(movie_id)
        # a list with particular quotes
        movie_quotes = quotes.copy()
        bot.send_message(message.chat.id, random.choice(quotes))
        ask_repeat(message, movie_quotes)
        chosen_movies.clear()
    except:
        wrong_input_text = 'There are no quotes for such input.\n' \
                           'Try again.'
        bot.send_message(message.chat.id, wrong_input_text)
        bot.register_next_step_handler(message, lambda x: choose_movie(x, chosen_movies))


def send_another_quote(message, movie_quotes):
    if message.text.lower() == 'more':
        bot.send_message(message.chat.id, random.choice(movie_quotes))
        ask_repeat(message, movie_quotes)
    else:
        # clear all data to add new next time
        movie_quotes.clear()
        send_welcome(message)


# method sends another random quote from the movie
def ask_repeat(message, movie_quotes):
    repeat_text = '\'More\' for another quote.'
    bot.send_message(message.chat.id, repeat_text)
    bot.register_next_step_handler(message, lambda x: send_another_quote(x, movie_quotes))


bot.polling(none_stop=True, interval=0, timeout=20)
