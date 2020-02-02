from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http.response import JsonResponse
from janome.tokenizer import Tokenizer
import os, json, random


URL = 'chatbot.html'
DICT_FILE = "chatbot/templates/chatbot-data.json"
dic = {}
# janome
tokenizer = Tokenizer()


def index(request):
    return render(request, URL)


@csrf_protect
def ajax_index(request):
    txt = request.POST.get('message')
    res = {}
    if txt == "":
        res = '何か発言してください'
    else:
        res = make_reply(txt)

    content = {
        'status': 'success',
        'res': res,
        'me_res': txt
    }
    return JsonResponse(content)


# 辞書に単語を記録する --- (*1)
def register_dic(words):
    global dic
    if len(words) == 0:
        return
    tmp = ["@"]
    for i in words:
        word = i.surface
        if word == "" or word == "\r\n" or word == "\n":
            continue
        tmp.append(word)
        if len(tmp) < 3:
            continue
        if len(tmp) > 3:
            tmp = tmp[1:]
        set_word3(dic, tmp)
        if word == "。" or word == "？":
            tmp = ["@"]
            continue
    # 辞書を更新するごとにファイルへ保存
    json.dump(dic, open(DICT_FILE, "w", encoding="utf-8"))


# 三要素のリストを辞書として登録
def set_word3(dic, s3):
    w1, w2, w3 = s3
    if w1 not in dic:
        dic[w1] = {}
    if w2 not in dic[w1]:
        dic[w1][w2] = {}
    if w3 not in dic[w1][w2]:
        dic[w1][w2][w3] = 0
    dic[w1][w2][w3] += 1


# 作文する --- (*2)
def make_sentence(head):
    if head not in dic:
        return ""
    ret = []
    if head != "@":
        ret.append(head)
    top = dic[head]
    w1 = word_choice(top)
    w2 = word_choice(top[w1])
    ret.append(w1)
    ret.append(w2)
    while True:
        if w1 in dic and w2 in dic[w1]:
            w3 = word_choice(dic[w1][w2])
        else:
            w3 = ""
        ret.append(w3)
        if w3 == "。" or w3 == "？" or w3 == "": break
        w1, w2 = w2, w3
    return "".join(ret)


def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))


# チャットボットに返答させる --- (*3)
def make_reply(text):
    # まず単語を学習する
    if text[-1] != "。":
        text += "。"
    words = tokenizer.tokenize(text)
    register_dic(words)
    # 辞書に単語があれば、そこから話す
    for w in words:
        face = w.surface
        ps = w.part_of_speech.split(',')[0]
        if ps == "感動詞":
            return face + "。"
        if ps == "名詞" or ps == "形容詞":
            if face in dic: return make_sentence(face)
    return make_sentence("@")


# 辞書があれば最初に読み込む
if os.path.exists(DICT_FILE):
    dic = json.load(open(DICT_FILE, "r"))
