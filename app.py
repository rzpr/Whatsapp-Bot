from flask import Flask, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse

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
    
    if 'p' in incoming_msg or 'P' in incoming_msg or 'Menu' in incoming_msg or 'menu' in incoming_msg or 'start' in incoming_msg:
        text = f'Hallo🙋🏽‍♂ \nBot Ini Dibuat Oleh _Rezza Priatna_ Semoga Bisa Membantu Kamu :)\n\nBerikut Inilah Yang Bisa Saya Lakukan 👇 \n\n *fb* <url>. Untuk Mendownlad video *Facebook*.\n\n *Ig* <url>. Untuk Mendownlad Video *Instagram*. \n\n *Yt* <urL>. Untuk Mendownlad Video *Youtube*.\n\n *S* <url>. Untuk Menggunakan *Search Engine*'
        msg.body(text)
        responded = True

    if 'fb' in incoming_msg:
        import requests as r
        import re
        par = incoming_msg[3:]
        html = r.get(par)
        video_url = re.search('sd_src:"(.+?)"', html.text).group(1)
        msg.media(video_url)
        responded = True

    if 'Yt' in incoming_msg:
        text = f'Coming Soon'
        msg.body(text)
        responded = True
    
    if 'Ig' in incoming_msg:
        text = f'Coming Soon'
        msg.body(text)
        responded = True
    
    

    if responded == False:
        msg.body('Maaf Saya Hanya Bot Tidak Mengenal Perintah Itu :)')

    return str(resp)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
