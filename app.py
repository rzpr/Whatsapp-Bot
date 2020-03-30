from flask import Flask, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
from googletrans import Translator

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    #print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    
    if 'start' in incoming_msg:
        text = f'Hallo🙋🏽‍♂ \nBot Ini Dibuat Oleh _Rezza Priatna_ Semoga Bisa Membantu Kamu :)\n\nBerikut Inilah Yang Bisa Saya Lakukan 👇 \n\n *FB* <url>. Untuk Mendownlad video *Facebook*.\n\n *IG* <url>. Untuk Mendownlad Video *Instagram*. \n\n *YT* <urL>. Untuk Mendownlad Video *Youtube*.\n\n *S*  <url>. Untuk Menggunakan *Search Engine* \n\n */FB* <pesan> Untuk Menggunakan *Translate eng_idn*'
        msg.body(text)
        responded = True
    else:
        responded = False
 
    if '/FB' in incoming_msg:
        import requests as r
        import re
        par = incoming_msg[3:]
        html = r.get(par)
        video_url = re.search('sd_src:"(.+?)"', html.text).group(1)
        msg.media(video_url)
        responded = True

    if '/YT' in incoming_msg:
        text = f'Coming Soon'
        msg.body(text)
        responded = True
    
    if '/IG' in incoming_msg:
        text = f'Coming Soon'
        msg.body(text)
        responded = True

    if '/TR' in incoming_msg:
        par = incoming_msg[3:]
        translator = Translator()
        result = translator.translate(par, src='id', dest='en')
        msg.body(result.text)
        responded = True

    if responded == False:
        msg.body('Maaf Saya Hanya Bot Tidak Mengenal Perintah Itu :), Silahkan Kirim start Untuk Menunjukan Menu')

    return str(resp)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
