from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http.response import JsonResponse
from janome.tokenizer import Tokenizer

import os, json, random


URL = 'chatbot.html'
DICT_FILE = "chatbot/templates/chatbot-data.json"
dic = {}
# janome
tokenizer = Tokenizer()


@login_required
@csrf_protect
def dashboard(request):
    return render(request, URL)

