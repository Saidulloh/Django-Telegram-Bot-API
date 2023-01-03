from application.management.commands.core import bot
from application.models import User, Post
from application.management.commands.texts import about_user_text, about_post_text
from application.management.commands.keyboards import show_menu, edit_profile_keyboard, \
    show_posts


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id  # get chat id
    from_user = message.from_user
    bot.send_message(chat_id=chat_id, text=f'Hi, u can create own posts, and show the other users!')  # greeting
    lst = [i.user_id for i in User.objects.all()]  # lst for users ids
    if from_user.id not in lst:
        User.objects.create(user_id=from_user.id, first_name=from_user.first_name, last_name=from_user.last_name,
                            username=from_user.username)
        bot.send_message(chat_id=chat_id, text=f'Your data successfully added in database!')
    user = User.objects.get(user_id=from_user.id)  # get request user
    bot.send_message(chat_id=chat_id, text=about_user_text.format(user.username, user.first_name, user.last_name),
                     reply_markup=show_menu())


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    chat_id = call.message.chat.id  # get chat id
    if call.data == 'edit_profile':
        msg = bot.send_message(chat_id=chat_id, text='Enter new username, first name, last name. '
                                                     '\nSeparated by commas(,)!')
        bot.register_next_step_handler(msg, callback=edit_profile)
    if call.data == 'show_posts':
        page_count = len(Post.objects.all())
        for post_id in Post.objects.all():
            print(post_id.id)
            post = Post.objects.get(id=post_id.id)
            image = open(f'media/{post.image}', 'rb')
            bot.send_photo(chat_id, image, caption=about_post_text.format(post.id, post.title, post.description,
                                                                          post.owner), reply_markup=show_posts())
    if call.data == 'create_post':
        title = get_title(call.message)
        description = get_description(call.message)
        image = get_image(call.message)
        create_post(message=call.message, title=title, description=description, image=image)


@bot.message_handler()
def create_post(message, title, description, image):
    chat_id = message.chat.id  # get chat id
    try:
        Post.objects.create(title=title, description=description, owner=message.from_user, image=image)
        bot.send_message(chat_id=chat_id, text='New post successfully created!', reply_markup=show_menu())
    except Exception as ex:
        return ex


@bot.message_handler()
def edit_profile(message):
    chat_id = message.chat.id  # get chat id
    lst = edit_profile_keyboard(message)  # get username, first name and last name
    user = User.objects.get(user_id=message.from_user.id)  # get request user
    try:
        user.username = lst[0]  # reset username
        user.first_name = lst[1]  # reset first name
        user.last_name = lst[2]  # reset last name
        user.save()  # save
        bot.send_message(chat_id=chat_id, text=about_user_text.format(user.username, user.first_name, user.last_name),
                         reply_markup=show_menu())
    except Exception as ex:
        print(ex)


def get_title(message):
    title = bot.send_message(message.chat.id, "Enter title of post:")
    # title = bot.send_message(chat_id=message.chat.id).text
    result = bot.register_next_step_handler(title, callback=create_post)
    return result


def get_image(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"media/post_images/{file_id}.png") as new_file:
            image = new_file.write(downloaded_file)
    except Exception as ex:
        bot.send_message(message.chat.id, f"Error: {ex}, try again!")
    image = bot.register_next_step_handler(image, callback=create_post)
    return image


def get_description(message):
    bot.send_message(message.chat.id, "Enter description of post:")
    description = bot.wait_for_message(chat_id=message.chat.id).text
    result = bot.register_next_step_handler(description, callback=create_post)
    return result


bot.polling(none_stop=True)
