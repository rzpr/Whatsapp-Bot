from flask import Flask, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
from googletrans import Translator

app = Flask(__name__)

@app.route("/")
def hello():
    return "Status Online"

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    #print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    
    if 'start' in incoming_msg:
        text = f'🤖 *Hallo, Selamat Datang Saya Adalah Recsec Bot Dibuat Oleh _Rezza Priatna_ Jika Butuh Bantuan/Ingin Requests Contack Dibawah :\n\n☎️ 085885105039\n📲 fb.me/rezzapriatna12\n\n📄*Berikut Command Yang Bisa Saya Lakukan* : \n\n🛡️ */FB* <url> ( Facebook Downloader )\n\n🛡️ */IG* <url> ( Instagram Downloader ) \n\n🛡️ */SG* <username> ( Stalk Profil Instagram )\n\n🛡️ */GL* <query> ( Google Search )\n\n🛡️ */TR-id-en* <text> ( Translate IDN>ENG )\n\n🛡️ */TR-eng-id* <text> ( Translate ENG>ID )\n\n🛡️ */TR-id-kor* <text> ( Translate ID>KOR )\n\n🛡️ */TR-kor-id* <text> ( Translate KOR>ID )\n\n🛡️ *help* Info Cara Menggunakan Tools'
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
        for i in search(query, tld="com", num=10, stop=10, pause=2):
            text = f'==========Results==========\n\n *Reff* : '+i
            msg.body(text)
            responded = True
            
    if '/TR-en-id' in incoming_msg:
        par = incoming_msg[9:]
        translator = Translator()
        result = translator.translate(par, src='en', dest='id')
        msg.body(result.text)
        responded = True

    if '/TR-id-en' in incoming_msg:
        par = incoming_msg[9:]
        translator = Translator()
        result = translator.translate(par, src='id', dest='en')
        msg.body(result.text)
        responded = True

    if '/TR-id-kor' in incoming_msg:
        par = incoming_msg[10:]
        translator = Translator()
        result = translator.translate(par, src='id', dest='ko')
        msg.body(result.text)
        responded = True

    if '/TR-kor-id' in incoming_msg:
        par = incoming_msg[10:]
        translator = Translator()
        result = translator.translate(par, src='ko', dest='id')
        msg.body(result.text)
        responded = True


 
    if '/TTS' in incoming_msg:
        par = incoming_msg[5:]
        msg.media('https://api.farzain.com/tts.php?id='+par+'&apikey=JsaChFteVJakyjBa0M5syf64z&')
        responded = True

    if '/SG' in incoming_msg:
        import requests 
        import json
        par = incoming_msg[4:]
        p = requests.get('http://api.farzain.com/ig_profile.php?id='+par+'&apikey=JsaChFteVJakyjBa0M5syf64z')
        js = p.json()['info']
        ms = (js['profile_pict'])
        jp = p.json()['count']
        text = f'Nama : *{js["full_name"]}* \nUsername : {js["username"]} \nBio : *{js["bio"]}* \nSitus Web : *{js["url_bio"]}* \nPengikut : *{jp["followers"]}* \nMengikuti : *{jp["following"]}* \nTotal Postingan : *{jp["post"]}* '
        msg.body(text)
        msg.media(ms)
        responded = True

    if 'help' in incoming_msg:
       text = f'💻 *Help For Instagram*\n\n/IG <Link Video> Contoh : \n/IG https://www.instagram.com/p/BWhyIhRDBCw/\n\n\n*Note* : Link Harus Seperti Di Contoh Kalo link Akhirannya Ada ?utm_source=ig_web_copy_link hapus bagian itu\n\n 💻 *Help For Facebook*\n\n/FB _link video_ Contoh :\n\n/FB https://www.facebook.com/100010246050928/posts/1143182719366586/?app=fbl \n\n💻 *Help For Translate*\n\n/TR Text Yang Ingin Di Translate, Contoh :\n\n/TR Selamat Malam  \n\n💻 *Help For Google Search* \n\n /GL <Query> Contoh :  \n\n/GL rezzaapr \n\n💻 *Help For Instagram Stalking \n\n/SG <username> Contoh : \n\n/SG rzapr \n\n💻 *Help For Translate* \n\nTR-id-eng Translate indonesia Ke inggris\n\n/TR-eng-id Translate Inggris Ke Indonesia\n\n/TR-id-kor Translate Indonesia Ke Korea \n\n/TR-kor-id Translate Korea Ke Indonesia \n\n💻 *Help For Text To Speech* \n\n/TTS WhatsappBotRezzaapr\n\nJika Ingin Menggunakan Spasi Ganti Dengan %20\n\nContoh : /TTS Whatsapp%20Bot%Rezzaapr'
       msg.body(text)
       responded = True

    if responded == False:
        msg.body('Maaf Saya Hanya Bot Tidak Mengenal Perintah Itu :), Silahkan Kirim start Untuk Menunju Ke Menu')

    return str(resp)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
