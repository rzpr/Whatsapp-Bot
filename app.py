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
        text = f'🤖 *Hallo, Selamat Datang Saya Adalah Recsec Bot Dibuat Oleh _Rezza Priatna_ Jika Butuh Bantuan Lihat Command Dibawah\n\n📄*Berikut Command Yang Bisa Saya Lakukan* : \n\n🛡️ */FB* <url>. Untuk Mendownlad video *Facebook*.\n\n🛡️ */IG* <url>. Untuk Mendownlad Video *Instagram*. \n\n🛡️ */SG* <username>. Untuk Stalking Profile *instagram*.\n\n🛡️ */GL* <query>. Untuk Menggunakan *Search Engine* \n\n🛡️ */TR* <pesan> Untuk Menggunakan *Translate eng_idn*\n\n🛡️ *help* Info Cara Menggunakan Tools'
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
            
    if '/TR' in incoming_msg:
        par = incoming_msg[3:]
        translator = Translator()
        result = translator.translate(par, src='id', dest='en')
        msg.body(result.text)
        responded = True
           
    if 'ZZ' in incoming_msg:
        msg.media('https://r5---sn-nh5gu-jb3l.googlevideo.com/videoplayback?expire=1585788895&ei=f-OEXpe1LJGwoAPa5K7ABQ&ip=115.178.203.34&id=o-ADlatN8F5e-q6Y0BcMNW_niN3ldHPZgmuAHZHrOdoQn9&itag=137&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=Tx&mm=31%2C26&mn=sn-nh5gu-jb3l%2Csn-i3beln7s&ms=au%2Conr&mv=m&mvi=4&pl=24&pcm2=yes&initcwndbps=150000&vprv=1&mime=video%2Fmp4&gir=yes&clen=191507551&dur=360.193&lmt=1531558813632691&mt=1585767226&fvip=5&keepalive=yes&c=WEB&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cpcm2%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=ALrAebAwRgIhANayLqNXOeN6S425tqgQqbz1exS_BAaauJFQKv5S6ya4AiEAwz6v4hsBgebSZR5XiFXNHMA4W4KXOX4Cdd23jVi8b5Y%3D&sig=AJpPlLswRQIhANzDDpH6hO58caFusMudU1NI341vm-Lmpf1Bvg5sYzw2AiBrv7Yz6OtH5MsyK_re4mCg64Yn3GdXW0MDz0lMpzvLzg==&ratebypass=yes')        
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
       text = f'💻 *Help For Instagram*\n\n/IG <Link Video> Contoh : \n/IG https://www.instagram.com/p/BWhyIhRDBCw/\n\n\n*Note* : Link Harus Seperti Di Contoh Kalo link Akhirannya Ada ?utm_source=ig_web_copy_link hapus bagian itu\n\n 💻 *Help For Facebook*\n\n/FB _link video_ Contoh :\n\n/FB https://www.facebook.com/100010246050928/posts/1143182719366586/?app=fbl \n\n💻 *Help For Translate*\n\n/TR Text Yang Ingin Di Translate, Contoh :\n\n/TR Selamat Malam  \n\n💻 *Help For Google Search* \n\n /GL <Query> Contoh :  \n\n/GL rezzaapr \n\n💻 *Help For Instagram Stalking \n\n/SG <username> Contoh : \n\n/SG rzapr'
       msg.body(text)
       responded = True

    if responded == False:
        msg.body('Maaf Saya Hanya Bot Tidak Mengenal Perintah Itu :), Silahkan Kirim start Untuk Menunjukan Menu')

    return str(resp)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
