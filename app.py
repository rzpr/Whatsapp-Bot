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
        text = f'🤖 _Halo Saya Adalah Recsec Bot, Ada Yang Bisa Saya Bantu?_\n\n*Admin :*\n\n📞 : 085885105039\n📱 : _fb.me/rezzapriatna12_ \n\n🚀 *Fitur* \n\n✅ _Youtube Downloader_ \n✅ _Facebook Downloader_ \n✅ _Instagram Downloader_ \n✅ _Google Search_ \n✅ _Text To Speech_ \n✅ _Stalking Profil Instagram_ \n✅ _Translate_ \n\n\n _Untuk Menampilkan Command Ketik_ *Menu*'
        msg.body(text)
        responded = True
    else:
        responded = False
    if 'Menu' in incoming_msg or 'menu' in incoming_msg:
        text = f'⌨️ *List Of Command :* \n\n🔥 */YT* _<url>_ : Youtube Downloader\n🔥 */FB* _<url>_ : Facebook Downloader\n🔥 */IG* _<url>_ : Instagram Downloader\n🔥 */FL* _<url>_ : Download Video Fb Ukuran BIG\n🔥 */GL* _<query>_ : Google Search\n🔥 */SG* _<usrname>_ : Get Info Instagram Profile\n🔥 */TTS* <Text> : Text To Speech\n🔥 */TR-id-en* _<text> : Translate ID > ENG\n🔥 */TR-en-id* _<text> : Translate ENG > ID\n🔥 */TR-id-kor* _<text>_ : Translate ID > Korea\n🔥 */TR-kor-id* _<text>_ : Translate Korea > ID\n🔥 *help* : Cara Menggunkan Command'
        msg.body(text)
        responded = True
        
    if '/FB' in incoming_msg:
        import requests as r
        import re
        par = incoming_msg[3:]
        html = r.get(par)
        video_url = re.search('sd_src:"(.+?)"', html.text).group(1)
        msg.media(video_url)
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

    if '/FL' in incoming_msg:
        import requests as r
        import re
        par = incoming_msg[3:]
        html = r.get(par)
        video_url = re.search('sd_src:"(.+?)"', html.text).group(1)
        reqq = r.get('http://tinyurl.com/api-create.php?url='+video_url)
        msg.body('*VIDEO BERHASIL DI CONVERT*\n\nLINK : ' +reqq.text+'\n\n_Cara Download Lihat Foto Diatas_')
        msg.media('https://user-images.githubusercontent.com/58212770/78709692-47566900-793e-11ea-9b48-69c72f9bec1e.png')
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

    if '/YT' in incoming_msg:
        import pafy
        import requests as r
        par = incoming_msg[4:]
        audio = pafy.new(par)
        gen = audio.getbestaudio(preftype='m4a')
        genn = audio.getbestvideo(preftype='mp4')
        req = r.get('http://tinyurl.com/api-create.php?url='+gen.url)
        popo = r.get('http://tinyurl.com/api-create.php?url='+genn.url)
        msg.body('_=========================_\n\n     _Video Berhasil Diconvert_\n\n_=========================_\n\n''*'+gen.title+'*''\n\n*Link Download Music* :' +req.text+'\n\n*Link Download Video* :' +popo.text)
        responded = True
        
    if '/SY' in incoming_msg:
        import requests as r
        par = incoming_msg[3:]
        req = r.get('http://api.farzain.com/yt_search.php?id='+par+'&apikey=JsaChFteVJakyjBa0M5syf64z&')
        js = req.json()[1]
        text = f'*Judul* :  _{js["title"]}_ \n\n*Url Video* : _{js["url"]}_\n\n*Video ID* : _{js["videoId"]}\n\n_Note : Jika Ingin Download Video Ini Atau Convert Ke Musik, Salin Link Diatas Dan Gunakan Command /YT_'
        msg.body(text)
        msg.media((js['videoThumbs']))
        responded = True
 
    if 'help' in incoming_msg:
       text = f'💻 *Help For Instagram*\n\n/IG <Link Video> Contoh : \n/IG https://www.instagram.com/p/BWhyIhRDBCw/\n\n\n*Note* : Link Harus Seperti Di Contoh Kalo link Akhirannya Ada ?utm_source=ig_web_copy_link hapus bagian itu\n\n 💻 *Help For Facebook*\n\n/FB _link video_ Contoh :\n\n/FB https://www.facebook.com/100010246050928/posts/1143182719366586/?app=fbl \n\n💻 *Help For Google Search* \n\n /GL <Query> Contoh :  \n\n/GL rezzaapr \n\n💻 *Help For Instagram Stalking \n\n/SG <username> Contoh : \n\n/SG rzapr \n\n💻 *Help For Translate* \n\nTR-id-en Translate indonesia Ke inggris\n\n/TR-en-id Translate Inggris Ke Indonesia\n\n/TR-id-kor Translate Indonesia Ke Korea \n\n/TR-kor-id Translate Korea Ke Indonesia \n\n💻 *Help For Text To Speech* \n\n/TTS WhatsappBotRezzaapr\n\nJika Ingin Menggunakan Spasi Ganti Dengan %20\n\nContoh : /TTS Whatsapp%20Bot%Rezzaapr'
       msg.body(text)
       responded = True

    if responded == False:
        msg.body('Maaf Saya Hanya Bot Tidak Mengenal Perintah Itu :), Silahkan Kirim start Untuk Menunju Ke Menu')

    return str(resp)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
