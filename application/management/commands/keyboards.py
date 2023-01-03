from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def show_menu():
    """
    Get all posts
    :return:
    """
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text='Edit profile', callback_data='edit_profile'),
        InlineKeyboardButton(text='Show posts', callback_data='show_posts'),
        InlineKeyboardButton(text='Create post', callback_data='create_post'),
    )
    return keyboard


def edit_profile_keyboard(message):
    """
    Function for editing profile
    :return:
    """
    lst = message.text.split(',')
    return lst  # return list for username, first name and last name



def show_posts():
    """
    Function for showing all posts
    :return:
    """
    keyboard = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='next', callback_data='next'),
    )
    return keyboard
