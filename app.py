from flask import Flask, request
import random
from pymessenger.bot import Bot
import os
from pymongo import MongoClient

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

bot = Bot(ACCESS_TOKEN)


@app.route('/', methods=['GET', 'POST'])

def receive_message():
    if request.method == 'GET':
        # Before allowing people to message your bot, Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook. 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message # back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):

                    #query mongodb data
                    mongo_url = "mongodb+srv://drahciR:redflyingcow@dynamicdata.ykrft.mongodb.net/?retryWrites=true&w=majority"
                    cluster = MongoClient(mongo_url)
                    db = cluster["Data"]
                    collection = db["levelone"]
                    data = collection.find().pretty()

                    # response_sent_text = get_message()
                    send_message(recipient_id, data)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    mongo_url = "mongodb+srv://drahciR:redflyingcow@dynamicdata.ykrft.mongodb.net/?retryWrites=true&w=majority"
                    cluster = MongoClient(mongo_url)
                    db = cluster["Data"]
                    collection = db["levelone"]
                    data = collection.find().pretty()

                    # response_sent_nontext = get_message()
                    send_message(recipient_id, data)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#chooses a random message to send to the user
def get_message():
    sample_responses = ["wassuh cuh", "ain", "yo", "Sup brah"]
    # return selected item to the user
    return random.choice(sample_responses)

def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"



if __name__ == '__main__':
    app.debug = True
    app.run()
    

