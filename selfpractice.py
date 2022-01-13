from __future__ import unicode_literals
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import json
import configparser
import os
from urllib import parse
app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
my_line_id = config.get('line-bot', 'my_line_id')
end_point = config.get('line-bot', 'end_point')
client_id = config.get('line-bot', 'client_id')
client_secret = config.get('line-bot', 'client_secret')
HEADER = {
    'Content-type': 'application/json',
    'Authorization': F'Bearer {config.get("line-bot", "channel_access_token")}'
}


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return 'ok'
    body = request.json
    events = body["events"]
    print(body)
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
        if events[0]["type"] == "message":
            if events[0]["message"]["type"] == "text":
                text = events[0]["message"]["text"]


                if text == text:
                    payload["messages"] = [
                            {
                                "type": "template",
                                "altText": "this is a confirm template",
                                "template": {
                                    "type": "confirm",
                                    "text": "是否規劃XXX附近景點??",
                                    "actions": [
                                        {
                                            "type": "message",
                                            "label": "是",
                                            "text": "是"
                                        },
                                        {
                                            "type": "message",
                                            "label": "否",
                                            "text": "否"
                                        }
                                    ]
                                }
                                }
                    ]
                elif text == "我選台北孔廟":
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": getTaipeiConfuciusTempleMessage()
                            }
                        ]
                elif text == "我選士林夜市":
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": getShiLinNNightMarketMessage()
                            }
                        ]   
                # 附近景點圖
                elif text == "是":
                    payload["messages"] = [
                            {
                                "type": "template",
                                "altText": "this is a carousel template",
                                "template": {
                                    "type": "carousel",
                                    "columns": [
                                        {
                                            "thumbnailImageUrl": "https://reurl.cc/Mbk57K",
                                            "imageBackgroundColor": "#FFFFFF",
                                            "title": "台北孔廟",
                                            "text": "description",
                                            "defaultAction": {
                                                "type": "uri",
                                                "label": "View detail",
                                                "uri": "http://example.com/page/123"
                                            },
                                            "actions": [
                                                {
                                                    "type": "postback",
                                                    "label": "我選台北孔廟",
                                                    "text":"我選台北孔廟"
                                                }
                                            ]
                                        },
                                        {
                                            "thumbnailImageUrl": "https://reurl.cc/jkgZ7m",
                                            "imageBackgroundColor": "#000000",
                                            "title": "士林夜市",
                                            "text": "description",
                                            "defaultAction": {
                                                "type": "uri",
                                                "label": "View detail",
                                                "uri": "http://example.com/page/222"
                                            },
                                            "actions": [
                                                {
                                                    "type": "postback",
                                                    "label": "我選士林夜市",
                                                    "text":"我選士林夜市"
                                                }
                                            ]
                                        }
                                    ],
                                    "imageAspectRatio": "rectangle",
                                    "imageSize": "cover"
                                }
                                }
                    ]

                elif text == "否":
                    payload["messages"] = [dontRecommend()]

                    
                   
                        
                    
                else:
                    print("error")


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
        )





@app.route("/sendTextMessageToMe", methods=['POST'])
def sendTextMessageToMe():
    body = request.json
    payload = {
    }
    pushMessage(payload)
    return 'OK'

def dontRecommend():
    return "感謝您的使用!"

def getLocationConfirmMessage(title, latitude, longitude):
    message = dict()
    message["type"] = "template"
    message["altText"] = "this is a confirm template"
    data = {"title": title, "latitude": latitude, "longitude": longitude, "action": "get_near"}
    message["template"] = {

    }
    return message


def getTaipeiConfuciusTempleMessage():
    message = dict()
    message["type"] = "location"
    message["title"] = "台北孔廟"
    message["address"] = "No. 275, Dalong St, Datong District, Taipei City, 103"
    message["latitude"] = 25.07281794124952
    message["longitude"] = 121.51631688202026

    return message

def getShiLinNNightMarketMessage():
    message = dict()
    message["type"] = "location"
    message["title"] = "士林夜市"
    message["address"] = "No. 101, Jihe Rd, Shilin District, Taipei City, 111"
    message["latitude"] = 25.08841443198597
    message["longitude"] = 121.52420239992968

    return message





def getLocalMessage():
    response = requests.get('https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4001&limited=TWN')
    date = response.json()[0]["a04"]
    total_count = response.json()[0]["a05"]
    count = response.json()[0]["a06"]
    return F"日期：{date}, 人數：{count}, 確診總人數：{total_count}"

