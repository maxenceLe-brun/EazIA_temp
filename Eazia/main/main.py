import openai
from craiyon import Craiyon
from PIL import Image
from itertools import product
import json
import requests
import random
import math
import base64
import os



class reaction:
    def __init__(self, base, header):
        self._header = header
        self._base = base

    def add(self, channel_id, message_id, emoji_name, emoji_id):
        return json.loads(requests.put(f"{self._base}/channels/{channel_id}/messages/{message_id}/reactions/{emoji_name}%3A{emoji_id}/%40me", headers=self._header).text)

    def remove(self, channel_id, message_id, emoji_name, emoji_id, user_id="%40me"):
        requests.delete(f"{self._base}/channels/{channel_id}/messages/{message_id}/reactions/{emoji_name}%3A{emoji_id}/{user_id}", headers=self._header)

class message:
    def __init__(self, base, header):
        self._header = header
        self._base = base
        self.reaction = reaction(self._base, self._header)

    def get(self, channel_id: str, amount: int):
        # x = Max Amount of message with one get [100: default]
        x = 100
        base = self._base + '/channels/'
        pending = [str(x),]*(amount//x) + [str(amount%x)]
        data = json.loads(requests.get(f"{base}{channel_id}/messages?limit={pending.pop(0)}", headers=self._header).text)
        try:
            for x in pending:
                t_data = json.loads(requests.get(f"{base}{channel_id}/messages?before={data[-1]['id']}&limit={x}", headers=self._header).text)
                if not t_data: raise StopIteration
                for i in t_data:
                    data.append(i)
        except StopIteration:
            pass
        return data

    def send(self, channel_id, message, reply_id=None, tts=None):
        json_payload = {'content': message, 'tts':tts}
        if reply_id:
            json_payload['message_reference'] = {'message_id': reply_id}
        return json.loads(requests.post(f"{self._base}/channels/{channel_id}/messages", headers=self._header, json=json_payload).text)

    def delete(self, channel_id, message_id):
        json.loads(requests.delete(f"{self._base}/channels/{channel_id}/messages/{message_id}", headers=self._header).text)

    def modify(self, channel_id, message_id, message):
        json.loads(requests.patch(f"{self._base}/channels/{channel_id}/messages/{message_id}", headers=self._header, json={'content':message}).text)

class channel:
    def __init__(self, base, header):
        self._header = header
        self._base = base   

    def list(self, id: str):
        text = requests.get(f"{self._base}/guilds/{id}/channels", headers=self._header).text
        return json.loads(text)

    def create(self, guild_id, name, ctype, parent_id=None, nsfw=False):
        json_payload = {
        'name': name,
        'type': ctype,
        'parent_id': parent_id,
        'permissions': [],
        'nsfw': nsfw
        }
        return json.loads(requests.post(f"{self._base}/guilds/{guild_id}/channels", headers=self._header, json=json_payload).text)

    def delete(self, channel_id):
        return json.loads(requests.delete(f"{self._base}/channels/{channel_id}", headers=self._header).text)

class emoji:
    def __init__(self, base, header):
        self._header = header
        self._base = base

    def list(self, guild_id):
        return json.loads(requests.get(f"{self._base}/guilds/{guild_id}/emojis", headers=self._header).text)

    def add(self, guild_id, name, filepath):
        ext = os.path.splitext(filepath)[1].split('.')[1]
        if ext in ['jpeg', 'png', 'gif']:
            payload = {
                "name": name,
                "image": f"data:image/{ext};base64,{base64.b64encode(open(filepath, 'rb').read()).decode('utf-8')}"
            }

            return json.loads(requests.post(f"{self._base}/guilds/{guild_id}/emojis", headers=self._header, json=payload).text)

class guild:
    def __init__(self, base, header):
        self._header = header
        self._base = base
        self.channel = channel(self._base, self._header)
        self.emoji = emoji(self._base, self._header)

    def getAll(self):
        request = requests.get(self._base + '/users/@me/guilds', headers=self._header)
        if request.status_code == 200:
            return json.loads(request.text)

    def get(self, id):
        return json.loads(requests.get(f"{self._base}/guilds/{id}", headers=self._header).text)

    def leave(self, guild_id):
        json.loads(requests.delete(f"{self._base}/users/@me/guilds/{guild_id}", headers=header).text)

class user:
    def __init__(self, base, header):
        self._header = header
        self._base = base
    
    def selfUser(self):
        return json.loads(requests.get(self._base + "/users/@me", headers=self._header).text)

    def get(self, user_id):
        return json.loads(requests.get(f"{self._base}/users/{user_id}", headers=self._header).text)

class discord:
    def __init__(self, token: str):
        self._token = token
        self._base = 'https://discord.com/api/v9'
        self._header = {'authorization': token, 'content-type': 'application/json'}

        self.message = message(self._base, self._header)
        self.reaction = reaction(self._base, self._header)
        self.guild = guild(self._base, self._header)
        self.user = user(self._base, self._header)


def createChannel(token: str,server_id: str, parent_id: str, name: str):
    """
    
    Parameters
    ----------
    token : str
        your Discord token. Be sure to not leak it, or you could lost your account
    server_id : str
        the server ID you want to use, be sure you have the right to do it
    parent_id : str
        the parent ID you're locating your future channel
    name : str
        the name you want to use for the new channel (default : pending_command)

    Returns
    -------
    TYPE : int
        the ID of the channel created

    """
    return json.loads(requests.post("https://discord.com/api/v9/guilds/"+server_id+'/channels', 
                                    headers={'authorization': token, 'content-type':'application/json'},
                                    json={"type":0, "name":name,"permission_overwrites":[],"parent_id":parent_id}).content.decode('utf-8'))['id']

def deleteChannel(token: str, channel_id: str):
    """

    Parameters
    ----------
    token : str
        your Discord token. Be sure to not leak it, or you could lost your account
    channel_id : str
        the channel ID you generated by the createChannel() function

    """
    requests.delete("https://discord.com/api/v9/channels/"+channel_id, headers={'authorization': token})

def postMessage(token: str, channel_id: str, message: str):
    """

    Parameters
    ----------
    token : str
        your Discord token. Be sure to not leak it, or you could lost your account
    channel_id : str
        the channel ID you generated by the createChannel() function
    message : str
        what you want to write on your next message

    """
    requests.post("https://discord.com/api/v9/channels/"+channel_id+"/messages",
                  headers={'authorization': token, 'content-type': 'application/json'}, json={'content':message})

def createIntegration(token: str, server_id: str, bot_id: str, channel_id: str, command_id: str, command_name: str, command_version: str, option=[]):
    """
    Parameters
    ----------
    token : str
        your Discord token. Be sure to not leak it, or you could lost your account
    server_id : str
        the server ID you want to use, be sure you have the right to do it
    bot_id : str
        the parent ID you're locating your future channel.
    channel_id : str
        the channel ID you generated by the createChannel() function
    command_id : str 
        if a number is linked to the command, put it here
    command_name : str "imagine"
        name of the command (useless bcs they have the same name by default)
    command_version : str
        the version of the command, if it's a free use, a paid use or a special use. Not used rn
    option : TYPE, optional
        DESCRIPTION. The default is [].

    """
    head = {'authorization': token, 'content-type': 'application/json'}
    data = {"application_id": bot_id,"channel_id": channel_id,"data"
            :{"id": command_id,"name": command_name,"options": option,"version": command_version},"guild_id": server_id,"session_id": "a","type": 2}
    requests.post("https://discord.com/api/v9/interactions", headers=head, json=data)

def postImage(token : str, channel_id : str, fl_path : str, message="" ):
    header = {
        'authorization': token,
    }

    files = {
        "file" : (fl_path, open(fl_path, 'rb'))
    }

    payload = {
        "content" : message
    }

    r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=header, files=files)

inter = discord("MTEwNjUzODMxNjg5MzAwMzc4Ng.GJTqj3.8i4PuxiL0MgnsWJuUySJPx9DsqKYNYeIZHOwo0")

def tile(filename, dir_in, dir_out, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size
    
    grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
    for i, j in grid:
        box = (j, i, j+d, i+d)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)

def download(imagelist):
    pdf = FPDF()
    for image in imagelist:
        pdf.add_page()
        pdf.image(image,x,y,100,100)
    pdf.output("yourfile.pdf", "F")

def downloadPicture(filepath, url):
    open(filepath, "wb").write(requests.get(url).content)

def text(txt):
    textOut = ""
    hashTag = []

    token = "__YOUR_TOKEN__"
    server_id = "1113874867276742688"
    parent_id = "1113942565633400992"
    name = "pending-command"

    liste = ["",]
    for a in text:
        if a == " ":
            liste.append("")
        else:
            liste[-1] += a
    for b in liste:
        if len(b)<=3:
            liste.remove(b)
    openai.api_key = "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"

    startPrompt = "Fait moi un article de " + str(len(liste)//10 + 1) + " paragraphes sur : "
    prompt = startPrompt + text + ". Fait ressortir les mots clés a la fin"

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", 
      messages=[{"role": "user", "content": prompt}]
    )
    textOut = completion["choices"][0]["message"]["content"]
    for a in range(len(textOut)):
        if textOut[a] == "\n":
            Target = a
    start = 0
    textOut = textOut.replace(textOut[a:],"")
    keyWord = textOut[a:].replace("Mots-clés : ", "")

    for charset in range(len(keyWord)):
        if keyWord[charset] == ",":
            hashTag.append(keyWord[start:charset])
            start = charset+2
        if keyWord[charset] == ".":
            hashTag.append(keyWord[start:])
    for j in range(len(hashTag)):
        hashTag[j].replace(" ", "_")

    return (textOut, keyWord)


def img(geneimg=""):

    geneImgOut = ""

    token = "__YOUR_TOKEN__"
    server_id = "880420256798101554"
    parent_id = "968938556829614090"
    name = "pending-command"

    if geneImg != "":
        channel_id = createChannel(token, server_id, parent_id, name)
        generator = Craiyon()
        result = generator.generate(geneImg)
        for a in result.images:
            postMessage(token, channel_id, a)
        geneImgOut = result.images
        human = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": "réponds uniquement par Oui ou Non : est ce que " + geneImg + " est un être humain"}]
        )
        if human["choices"][0]["message"]["content"] == "Oui.":
            #utiliser midjourney
            pass
    return geneImgOut


def main(text : str, geneImg : str, fileIp):
    textOut = ""
    geneImgOut = ""
    hashTag = []

    outPut = [textOut,geneImgOut, []]
    token = "MTEwNjUzODMxNjg5MzAwMzc4Ng.GJTqj3.8i4PuxiL0MgnsWJuUySJPx9DsqKYNYeIZHOwo0"
    server_id = "1113874867276742688"
    parent_id = "1141351077317459968"
    name = "pending-command"

    liste = ["",]
    for a in text:
        if a == " ":
            liste.append("")
        else:
            liste[-1] += a
    for b in liste:
        if len(b)<=3:
            liste.remove(b)
    openai.api_key = "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"

    prompt = "Réalise les étapes suivante: 1. voici mon thème : '" + text + "'; 2, crée une description en FRANCAIS de 300 caractères maximum d'un post Instagram et tu la mets entre crochets; 3. écris une instruction en 100 caractères, en ANGLAIS, à donner à une IA génératrice d'images à partir de la description que tu as inventé juste avant pour l'illustrer et mets la entre accolades : {}."
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", 
      messages=[{"role": "user", "content": prompt}]
    )
    print(completion)
    return None
    textOut = completion["choices"][0]["message"]["content"]
    for a in range(len(textOut)):
        if textOut[a] == "\n":
            Target = a
    start = 0
    n = -1
    N = 0
    while N != 2:
        if textOut[n] == ".":
            N += 1
        n -= 1
    hashTag = textOut[n+2:]
    textOut = textOut[:n+2]
    hashTag = hashTag.replace("\n","")

    hashTag = hashTag.replace(" Mots clés : ","")
    hashTag = hashTag.replace("Mots clés : ","")
    hashTag = hashTag.replace(", ",",")
    hashTag = hashTag.replace(' ', "_")
    keyWord = []
    temp = "#"
    for a in hashTag:
        if a != ",":
            temp += a
        else:
            keyWord.append(temp)
            temp = "#"
    if geneImg:
        channel_id = createChannel(token, server_id, parent_id, name)
        geneImgOut = []
        #generator = Craiyon()
        #result = generator.generate(geneImg)
        #for a in result.images:
        #    postMessage(token, channel_id, a)
        #geneImgOut = result.images
        #human = openai.ChatCompletion.create(
        #    model="gpt-3.5-turbo", 
        #    messages=[{"role": "user", "content": "réponds uniquement par Oui ou Non : est ce que " + geneImg + " est un être humain"}]
        #)
        #if human["choices"][0]["message"]["content"] == "Oui.":
        #    #utiliser midjourney
        #    pass
        createIntegration(token, server_id, "936929561302675456", channel_id, "938956540159881230", "imagine", "1118961510123847772", [{"type":3,"name":"prompt","value":geneImg}])
        tempImg = ""
        while tempImg == "":
            roam = inter.message.get(channel_id, 4)
            for a in roam:
                if 'author' in a and 'id' in a['author'] and 'content' in a and "**" + geneImg + "**" in a['content'] and "%" not in a['content'][len("**" + geneImg + "**"):] and 'attachments' in a and len(a['attachments']) > 0 and 'url' in a['attachments'][0]:
                    tempImg = a['attachments'][0]['url']
        cwd = os.getcwd()

        if "quart.png" in os.listdir(cwd + "/backup/"+fileIp):
            os.remove(cwd + "/backup/"+fileIp+"/quart.png")
            os.remove(cwd + "/backup/"+fileIp+"/quart_0_0.png")
            os.remove(cwd + "/backup/"+fileIp+"/quart_0_1024.png")
            os.remove(cwd + "/backup/"+fileIp+"/quart_1024_0.png")
            os.remove(cwd + "/backup/"+fileIp+"/quart_1024_1024.png")
        downloadPicture(cwd+"/backup/"+fileIp+"/quart.png",tempImg)

        tile("quart.png",cwd+"/backup/"+fileIp, cwd+"/backup/"+fileIp,1024)

        postImage(token, channel_id, cwd+"/backup/"+fileIp+"/quart_0_0.png", geneImg)
        postImage(token, channel_id, cwd+"/backup/"+fileIp+"/quart_1024_0.png", geneImg)
        postImage(token, channel_id, cwd+"/backup/"+fileIp+"/quart_0_1024.png", geneImg)
        postImage(token, channel_id, cwd+"/backup/"+fileIp+"/quart_1024_1024.png", geneImg)

        if "quart.png" in os.listdir(cwd + "/backup/"+fileIp):
            os.remove(cwd + "/backup/"+fileIp+"/quart.png")
            os.remove(cwd + "/backup/"+fileIp+"/quart_0_0.png")
            os.remove(cwd + "/backup/"+fileIp+"/quart_0_1024.png")
            os.remove(cwd + "/backup/"+fileIp+"/quart_1024_0.png")
            os.remove(cwd + "/backup/"+fileIp+"/quart_1024_1024.png")


        templink = []
        while len(templink)< 4:
            roam = inter.message.get(channel_id, 100)
            for a in roam:
                if 'attachments' in a and len(a['attachments']) >= 1 and 'author' in a and a['author']['id'] == "1106538316893003786" and a['content'] == geneImg and 'url' in a['attachments'][0] and len(a['attachments'][0]['url'])>1 and a['attachments'][0]['url'] not in templink:
                    templink.append(a['attachments'][0]['url'])
                    break

        for a in templink:
            geneImgOut.append(a)




        geneImgOut.append(tempImg)


    return (textOut,geneImgOut, keyWord)




"""def product_created_view(request):
    form = ProductForm(request.POST or None)

    strform = str(form)
    listform = [[]]
    for a in strform:
        if a == "\n":
            listform.append("")
        else:
            listform[-1] += a
    prompt = ""
    image_generator = ""
    inPut = [prompt,image_generator]
    n = 0
    for a in listform:
        if "</textarea>" in a:
            inPut[n] = a.replace("</textarea>","")
            n+=1
    P = Process(target=main,args=(inPut[0], inPut[1]))
    P.start()
    path('load/', product_load_view, name='product-list')
    P.join()
    print(Value(P))
    #textOut,geneImgOut,hashtag = main(inPut[0],inPut[1])        

    context = {
        'prompt':textOut,
        'image_generator':geneImgOut,
        'hashtag':hashtag,
        'form': form

    }
    print()
    return render(request, "products/product_created.html", context)"""

