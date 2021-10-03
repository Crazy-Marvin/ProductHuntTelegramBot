import telebot
import gspread
import requests
import threading
import time
import schedule
import datetime
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from telebot import custom_filters
from oauth2client.service_account import ServiceAccountCredentials

dotenv.load_dotenv()

# your Token from @Botfather
API_KEY = os.getenv("API_KEY")
my_id = os.getenv("my_id")  # your personal chat ID
analyst_id = os.getenv("analyst_id")  # your analyst chat ID
ph_auth = os.getenv("ph_auth")  # your token for accessing the Product Hunt API
# the place where your creds.json from Google is stored
creds_location = os.getenv("creds_location")
forms_url = os.getenv("forms_url")  # your URL to the Google Forms for feedback
# your URL to the Google Spreadsheet for analytics
spreadsheet_url = os.getenv("spreadsheet_url")

pod_img = "AgACAgUAAxkBAAMsYUtpwf4IweE0MYMGR9Vbpe1xOiEAAuStMRu77WBWjmCIZUpTv9oBAAMCAAN5AAMhBA"
pom_img = "AgACAgUAAxkBAAIB9WFO1TnJhBFbYkS0O-VdaYA9UA3SAAJkrDEbzKd4Vq56YH6fcfZFAQADAgADeQADIQQ"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(creds_location, scope)
client = gspread.authorize(creds)

analytics_PRODUCT_HUNT_BOT = client.open(
    "ANALYTICS").worksheet("PRODUCT-HUNT_BOT")
database = client.open("PRODUCT HUNT BOT DATABASE").worksheet("DATABASE")

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def start(message):

    col = database.col_values(1)

    if str(message.chat.id) not in col:
        database.append_row([message.chat.id, 'daily/monthly'])
        analytics_PRODUCT_HUNT_BOT.update_acell('F10', str(
            len(database.col_values(1))-1).replace("'", " "))

    msg = '''
Welcome to the [Product Hunt](https://www.producthunt.com/) Telegram bot\! 👶

I can send you daily or monthly updates regarding posts on [Product Hunt](https://www.producthunt.com/)\. An opt\-out is possible if you would like to trigger me manually\.

Send /help for more information\.

Enjoy\! 🎉
'''
    bot.send_message(message.chat.id, msg,
                     parse_mode="MarkdownV2", disable_web_page_preview=True)

    start_count = analytics_PRODUCT_HUNT_BOT.acell('F3').value
    analytics_PRODUCT_HUNT_BOT.update_acell(
        'F3', str(int(start_count)+1).replace("'", " "))


@bot.message_handler(commands=["daily"])
def pod(message):

    url = "https://api.producthunt.com/v1/posts"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ph_auth}",
        "Host": "api.producthunt.com"
    }

    posts, MSG = requests.get(url=url, headers=headers).json()['posts'], ""

    bot.send_photo(message.chat.id, pod_img)

    for count, post in enumerate(posts):

        if(count+1) == len(posts):
            bot.send_message(message.chat.id, MSG, parse_mode="HTML",
                             disable_web_page_preview=True, disable_notification=True)

        elif (count + 1) % 10 == 0:
            bot.send_message(message.chat.id, MSG, parse_mode="HTML",
                             disable_web_page_preview=True, disable_notification=True)
            MSG = ""

        MSG += f'➤ <b><a href="{post["redirect_url"]}">{post["name"]}: </a></b>'
        MSG += f'<a href="{post["discussion_url"]}">{post["tagline"]}</a>\n\n'

    END = "<i>For more such amazing products, please visit our \
<b><a href='https://www.producthunt.com/'>website.</a></b></i>"

    bot.send_message(message.chat.id, END, parse_mode="HTML",
                     disable_web_page_preview=True)
    ph_count = analytics_PRODUCT_HUNT_BOT.acell('F4').value
    analytics_PRODUCT_HUNT_BOT.update_acell(
        'F4', str(int(ph_count)+1).replace("'", " "))


@bot.message_handler(commands=["monthly"])
def pom(message):

    month = datetime.datetime.today().month  # TODO: Fix for Jan 1, 2022
    year = datetime.datetime.today().year

    url = f"https://api.producthunt.com/v1/posts/all?sort_by=votes_count&order=desc&search[featured_month]={month}&search[featured_year]={year}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ph_auth}",
        "Host": "api.producthunt.com"
    }

    posts, MSG = requests.get(url=url, headers=headers).json()['posts'], ""

    bot.send_photo(message.chat.id, pom_img)

    for count, post in enumerate(posts):

        if(count+1) == len(posts):
            bot.send_message(message.chat.id, MSG, parse_mode="HTML",
                             disable_web_page_preview=True, disable_notification=True)

        elif (count + 1) % 10 == 0:
            bot.send_message(message.chat.id, MSG, parse_mode="HTML",
                             disable_web_page_preview=True, disable_notification=True)
            MSG = ""

        MSG += f'➤ <b><a href="{post["redirect_url"]}">{post["name"]}: </a></b>'
        MSG += f'<a href="{post["discussion_url"]}">{post["tagline"]}</a>\n\n'

    END = "<i>For more such amazing products, please visit our \
<b><a href='https://www.producthunt.com/'>website.</a></b></i>"

    bot.send_message(message.chat.id, END, parse_mode="HTML",
                     disable_web_page_preview=True)
    ph_count = analytics_PRODUCT_HUNT_BOT.acell('F5').value
    analytics_PRODUCT_HUNT_BOT.update_acell(
        'F5', str(int(ph_count)+1).replace("'", " "))


@bot.message_handler(commands=["schedule"])
def sch(message):

    mark_up = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    B1 = KeyboardButton(text='DAILY UPDATES')
    B2 = KeyboardButton(text='MONTHLY UPDATES')
    B3 = KeyboardButton(text='DAILY & MONTHLY')
    B4 = KeyboardButton(text='MANUAL UPDATES')

    mark_up.row(B1, B2)
    mark_up.row(B3, B4)

    bot.send_message(
        message.chat.id, "How often would you like to recieve updates?", reply_markup=mark_up)
    sch_count = analytics_PRODUCT_HUNT_BOT.acell('F6').value
    analytics_PRODUCT_HUNT_BOT.update_acell(
        'F6', str(int(sch_count)+1).replace("'", " "))


@bot.message_handler(text=['DAILY UPDATES'])
def text_filter(message):

    cell = database.find(str(message.chat.id))
    r, c = cell.row, cell.col+1
    database.update_cell(r, c, 'daily')
    bot.send_message(message.chat.id, "PREFERENCE: DAILY UPDATES")


@bot.message_handler(text=['MONTHLY UPDATES'])
def text_filter(message):

    cell = database.find(str(message.chat.id))
    r, c = cell.row, cell.col+1
    database.update_cell(r, c, 'monthly')
    bot.send_message(message.chat.id, "PREFERENCE: MONTHLY UPDATES")


@bot.message_handler(text=['DAILY & MONTHLY'])
def text_filter(message):

    cell = database.find(str(message.chat.id))
    r, c = cell.row, cell.col+1
    database.update_cell(r, c, 'daily/monthly')
    bot.send_message(message.chat.id, "PREFERENCE: DAILY & MONTHLY UPDATES")


@bot.message_handler(text=['MANUAL UPDATES'])
def text_filter(message):

    cell = database.find(str(message.chat.id))
    r, c = cell.row, cell.col+1
    database.update_cell(r, c, 'none')
    bot.send_message(message.chat.id, "PREFERENCE: MANUAL UPDATES")


@bot.message_handler(commands=['contact'])
def contact(message):
    contact_info = '''
*CONTACT :*\n
Telegram: https://t\.me/Marvin\_Marvin\n
Mail: marvin@poopjournal\.rocks\n
Issue: https://github\.com/Crazy\-Marvin/ProductHuntTelegramBot/issues\n
Source: https://github\.com/Crazy\-Marvin/ProductHuntTelegramBot
'''
    bot.send_message(message.chat.id, contact_info,
                     parse_mode='MarkdownV2', disable_web_page_preview=True)
    contact_count = analytics_PRODUCT_HUNT_BOT.acell('F8').value
    analytics_PRODUCT_HUNT_BOT.update_acell(
        'F8', str(int(contact_count)+1).replace("'", " "))


@bot.message_handler(commands=['feedback'])
def feedback(message):

    bot.send_message(message.chat.id, "Want to give us a feedback?\n\n\
{forms_url} \n\nPlease fill out this Google Form☝🏻", disable_web_page_preview=True)

    feedback_count = analytics_PRODUCT_HUNT_BOT.acell('F7').value
    analytics_PRODUCT_HUNT_BOT.update_acell(
        'F7', str(int(feedback_count)+1).replace("'", " "))


@bot.message_handler(commands=['help'])
def help(message):
    msg = '''
Thanks for using the Product Hunt Telegram bot. 

After starting the bot with /start you will receive all Product Hunt posts daily. It is possible to opt-out or change the schedule with the /schedule command.

Sending /ph will send you all posts from today again.

If you would like to contact me send /contact. 
Feedback is very appreaciated by filling out a Google form which the bot will send you after sending him /feedback. 

Have fun!  🥳'''

    bot.send_message(message.chat.id, msg)
    help_count = analytics_PRODUCT_HUNT_BOT.acell('F9').value
    analytics_PRODUCT_HUNT_BOT.update_acell(
        'F9', str(int(help_count)+1).replace("'", " "))


@bot.message_handler(commands=['logs'])
def logs(message):

    if message.chat.id == my_id or message.chat.id == analyst_id:

        bot.send_message(message.chat.id, f"Check out the *[ANALYTICS]{spreadsheet_url})* for the month\.",
                         parse_mode="MarkdownV2", disable_web_page_preview=True)


bot.add_custom_filter(custom_filters.TextMatchFilter())


def monthly():

    if datetime.date.today() != 1:
        return

    month = datetime.datetime.today().month - 1  # TODO: Fix for Jan 1, 2022
    year = datetime.datetime.today().year

    url = f"https://api.producthunt.com/v1/posts/all?sort_by=votes_count&order=desc&search[featured_month]={month}&search[featured_year]={year}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ph_auth}",
        "Host": "api.producthunt.com"
    }

    posts, MSG = requests.get(url=url, headers=headers).json()['posts'], ""
    users = database.get_all_records()

    for user in users:

        if user["Updates"] == "monthly" or user["Updates"] == "daily/monthly":

            chat_id = user["Chat Id"]

            bot.send_photo(chat_id, pom_img)

            for count, post in enumerate(posts):

                if(count+1) == len(posts):
                    bot.send_message(chat_id, MSG, parse_mode="HTML",
                                     disable_web_page_preview=True, disable_notification=True)

                elif (count + 1) % 10 == 0:
                    bot.send_message(chat_id, MSG, parse_mode="HTML",
                                     disable_web_page_preview=True, disable_notification=True)
                    MSG = ""

                MSG += f'➤ <b><a href="{post["redirect_url"]}">{post["name"]}: </a></b>'
                MSG += f'<a href="{post["discussion_url"]}">{post["tagline"]}</a>\n\n'

            END = "<i>For more such amazing products, please visit our <b><a href='https://www.producthunt.com/'>website.</a></b></i>"

            bot.send_message(chat_id, END, parse_mode="HTML",
                             disable_web_page_preview=True)


def daily():

    url = "https://api.producthunt.com/v1/posts/"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ph_auth}",
        "Host": "api.producthunt.com"
    }

    posts, MSG = requests.get(url=url, headers=headers).json()['posts'], ""
    users = database.get_all_records()

    for user in users:

        if user["Updates"] == "daily" or user["Updates"] == "daily/monthly":

            chat_id = user["Chat Id"]

            bot.send_photo(chat_id, pod_img)

            for count, post in enumerate(posts):

                if(count+1) == len(posts):
                    bot.send_message(chat_id, MSG, parse_mode="HTML",
                                     disable_web_page_preview=True, disable_notification=True)

                elif (count + 1) % 10 == 0:
                    bot.send_message(chat_id, MSG, parse_mode="HTML",
                                     disable_web_page_preview=True, disable_notification=True)
                    MSG = ""

                MSG += f'➤ <b><a href="{post["redirect_url"]}">{post["name"]}: </a></b>'
                MSG += f'<a href="{post["discussion_url"]}">{post["tagline"]}</a>\n\n'

            END = "<i>For more such amazing products, please visit our <b><a href='https://www.producthunt.com/'>website.</a></b></i>"

            bot.send_message(chat_id, END, parse_mode="HTML",
                             disable_web_page_preview=True)


schedule.every().day.at("00:00").do(daily)
schedule.every().day.at("12:00").do(monthly)

# TODO: Create a separate script and host it as a main thread on server for better performance 🤔


def thrd():
    while True:
        schedule.run_pending()
        time.sleep(5)


t = threading.Thread(target=thrd)

t.start()
bot.polling()
