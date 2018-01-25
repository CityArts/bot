import json, requests
import configparser
import subprocess
import time
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


config = configparser.ConfigParser()
config.read('bot.conf')

updater = Updater(token=config['KEYS']['bot_api'])
dispatcher = updater.dispatcher

def start(bot, update):
    update.message.reply_text("안녕하세요! 여러분의 친구, CityArts Official Bot 입니다.\n"
                              "명령어를 보시려면 /help 를 입력해주시면 감사하겠습니다!\n"
                              "\n"
                              "Hello, It's you're friend, CityArts Official Bot.\n"
                              "If you want see commands, please send /help thanks!")

def stop(bot, update):
    update.message.reply_text("CityArts Official Bot 을 정지합니다.\n"
                              "다시 시작하시려면 /start 를 입력해주시면 감사하겠습니다.\n"
                              "\n"
                              "Stopping CityArts Official Bot.\n"
                              "If you want restart, please enter /start.")

def help(bot, update):
    update.message.reply_text("CityArts Official Bot 은 다음과 같이 사용할 수 있습니다.\n"
                              "/start - CityArts Official Bot 을 시작합니다.\n"
                              "/stop - CityArts Official Bot 를 중지합니다.\n"
                              "/help - CityArts Official Bot 의 도움말을 표시합니다.\n"
                              "/map - CityArts 서버의 지도를 표시합니다.\n"
                              "/trains - CityArts 서버의 철도 노선도를 표시합니다.\n"
                              "/report [문자] - IPA 에 서버의 문제점을 제보합니다.\n"
                              "/status - CityArts 서버의 상태를 표시합니다.\n"
                              "\n"
                              "The CityArts Official Bot can be used as follows.\n"
                              "/start - Start CityArts Official Bot.\n"
                              "/stop - Stop CityArts Official Bot.\n"
                              "/help - Displays help for CityArts Official Bot.\n"
                              "/map - Displays a map of CityArts.\n"
                              "/trains - Displays a railway route map of CityArts.\n"
                              "/report [Text] - Report complaints to IPA.\n"
                              "/status - Displays the status of CityArts.")

def map(bot, update):
    update.message.reply_photo(open("resources/map.jpg", 'rb'), 
                              "다음은 CityArts 의 지도입니다.\n"
                              "실시간 지도 확인은 live.cityarts.ga 에서 하실 수 있습니다.\n"
                              "Here is a map of CityArts.\n"
                              "Real-time map confirmation is available at live.cityarts.ga.")

def trains(bot, update):
    update.message.reply_photo(open("resources/trains_map.jpg", 'rb'), 
                              "다음은 CityArts 의 철도 노선도 입니다.\n"
                              "Here is a railroad map of CityArts.")

def status(bot, update):
    url = 'https://mcapi.us/server/status'

    params = dict(
        ip='cityarts.ga'
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    text = ("서버 주소 : cityarts.ga\n"
           "서버 상태 : {}\n"
           "플레이어 : {} / {}\n"
           "서버 버전 : {}\n"
           "\n"
           "Server Address : cityarts.ga\n"
           "Server Status : {}\n"
           "Players : {} / {}\n"
           "Server Version : {}".format(server_status(data["online"]), data["players"]["max"], data["players"]["now"], data["server"]["name"], server_status(data["online"]), data["players"]["max"], data["players"]["now"], data["server"]["name"]))

    update.message.reply_text(text)

def server_status(status):
    if status:
        return "ON ✅"

    return "OFF ❎"

def report(bot, update):
    text = ' '.join(update.message.text.split()[1:])

    if text:
        update.message.reply_text("IPA 로 해당 내용이 전송되었습니다.\n"
                                  "제보해주셔서 감사드립니다.\n"
                                  "\n"
                                  "Your content has been sent to IPA.\n"
                                  "Thank you for reporting.")
        bot.send_message(os.environ['IPA_GROUP_ID'], "여러분께 알립니다.\n"
                         "다음과 같은 제보가 들어왔습니다.\n"
                         "\n"
                         "사용자 이름 : " + update.message.from_user.first_name + " ( @" + update.message.from_user.username + " )\n"
                         "내용 : " + text + "\n"
                         "참고 부탁드리겠습니다 감사합니다.")
    else:
        update.message.reply_text("위 커맨드는 IPA에 제보하기 위한 명령어입니다.\n"
                                  "사용법 : /report [내용]\n"
                                  "\n"
                                  "The above command is a command to report to IPA.\n"
                                  "Usage : /report [Text]")

def welcome(bot, update):
    update.message.reply_text("안녕하세요! 여러분의 친구, CityArts Official Bot 입니다.\n"
                              "CityArts 의 서버원이 되신걸 진심으로 환영합니다!\n"
                              "\n"
                              "Hello, It's you're friend, CityArts Official Bot.\n"
                              "Welcome to CityArts!")
    
def wiki(bot, update):
    text = ' '.join(update.message.text.split()[1:])
    
    if text:
        url = 'https://wiki.cityarts.ga/search/' + text

        resp = requests.get(url)
        
        if resp.text.find("문서가 없습니다.") == -1:
            update.message.reply_text("wiki.cityarts.ga/w/{} 에서 해당 문서를 보실 수 있습니다.\n"
                                      "You can find this document in wiki.cityarts.ga/w/{}.".format(text, text))
        else:
            update.message.reply_text("죄송합니다. {} 문서를 찾을 수 없습니다."
                                      "Sorry. {} Document not found".format(text, text))
    else:
        update.message.reply_text("위 커맨드는 문서를 검색하기 위한 명령어입니다.\n"
                                  "사용법 : /wiki [내용]\n"
                                  "\n"
                                  "The above command is for searching documents.\n"
                                  "Usage : /wiki [Text]")

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('stop', stop))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('map', map))
dispatcher.add_handler(CommandHandler('trains', trains))
dispatcher.add_handler(CommandHandler('status', status))
dispatcher.add_handler(CommandHandler('report', report))
dispatcher.add_handler(CommandHandler('wiki', wiki))
dispatcher.add_handler(MessageHandler([Filters.status_update.new_chat_members], welcome))

updater.start_polling()
updater.idle()
