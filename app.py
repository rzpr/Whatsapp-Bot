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
        text = f'🤖 *Hallo, Selamat Datang Saya Adalah Recsec Bot Dibuat Oleh _Rezza Priatna_ Jika Butuh Bantuan Lihat Command Dibawah\n\n📄*Berikut Command Yang Bisa Saya Lakukan* : \n\n🛡️ */FB* <url>. Untuk Mendownlad video *Facebook*.\n\n🛡️ */IG* <url>. Untuk Mendownlad Video *Instagram*. \n\n🛡️ */YT* <urL>. Untuk Mendownlad Video *Youtube*.\n\n🛡️ */GL* <query>. Untuk Menggunakan *Search Engine* \n\n🛡️ */TR* <pesan> Untuk Menggunakan *Translate eng_idn*\n\n🛡️ *help* Info Cara Menggunakan Tools'
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
        import requests as r
        par = incoming_msg[3:]
        a = r.get(par+'?__a=1')
        b = a.json()
        c = b['graphql']['shortcode_media']
        d = (c['video_url']) 
        msg.media(d)
        responded = True  
        
    if '/GL' in incoming_msg:
        from googlesearch import search
        query = incoming_msg[3:]
        for i in search(query, tld="com", num=10, stop=5, pause=2):
            text = f'==========Results==========\n\n *Reff* : '+i
            msg.body(text)
            responded = True
            
    if '/TR' in incoming_msg:
        par = incoming_msg[3:]
        translator = Translator()
        result = translator.translate(par, src='id', dest='en')
        msg.body(result.text)
        responded = True
        
    if '/SG' in incoming_msg:
        par = incoming_msg[3:]
        p = requests.get('https://www.instagram.com/'+par+'/?__a=1')
        q = requests.get('http://api.farzain.com/ig_profile.php?id='+par+'&apikey=JsaChFteVJakyjBa0M5syf64z')
        jp = q.json()['count']
        js = p.json()['graphql']['user']
        text = f'*Username* : {js["username"]} \n*Full Name* : {js["full_name"] \n*Bio* : {["biography"]} \n*Followers* : {jp["followers"]} \n*Following* : {jp["following"]}'
        p = (["profile_pic_url_hd"]) 
        msg.body(text)
        msg.media(p)
                                                                
    if 'help' in incoming_msg:
       text = f'💻 *Help For Instagram*\n\n/IG Link Video Contoh : \n/IG https://www.instagram.com/p/BWhyIhRDBCw/\n\n\n*Note* : Link Harus Seperti Di Contoh Kalo link Akhirannya Ada ?utm_source=ig_web_copy_link hapus bagian itu\n\n 💻 *Help For Facebook*\n\n/FB _link video_ Contoh :\n\n/FB https://www.facebook.com/100010246050928/posts/1143182719366586/?app=fbl \n\n💻 *Help For Translate*\n\n/TR Text Yang Ingin Di Translate, Contoh :\n\n/TR Selamat Malam '
       msg.body(text)
       responded = True

    if responded == False:
        msg.body('Maaf Saya Hanya Bot Tidak Mengenal Perintah Itu :), Silahkan Kirim start Untuk Menunjukan Menu')

    return str(resp)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
