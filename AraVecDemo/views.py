# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify, redirect, url_for, session

from datetime import datetime, timedelta
from dateutil import parser

from AraVecDemo import app

import os
import json
import operator
import re
import random
import csv
import codecs
import uuid
import gensim
import re

from numpy import array
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from bidi.algorithm import get_display
import arabic_reshaper

model = Word2Vec.load('D:\\Engineering\\Software\\Machine Learning\\NLP\\Datasets\\ar_wiki_word2vec')

@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route("/most_similar", methods=["POST"])
def most_similar():
    image_url = ''
    randName = random.randint(1, 100000)

    words = request.args.get(u"words")
    man = words.split(',')[0]
    king = words.split(',')[1]
    woman = words.split(',')[2]

    for word in words.split(','):
        try:
            most_similar = model.wv.most_similar(word)
        except:
            return jsonify(answer=word + u" غير موجودة في القاموس")

    answer = model.wv.most_similar(
        positive=[woman, king],
        negative=[man],
        topn=5)

    words = words.split(',')
    words.append(answer[0][0])

    X1 = {}
    for x in words:
        X1[x] = model.wv.vocab[x]
    X = array([model[x] for x in model.wv.vocab if x in words])

    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
    # create a scatter plot of the projection
    plt.figure()
    plt.scatter(result[:, 0], result[:, 1])
    newwords = list(X1)
    for i, word in enumerate(newwords):
        word = arabic_reshaper.reshape(word)
        word = get_display(word)
        plt.annotate(word, xy=(result[i, 0], result[i, 1]))
        plt.savefig('AraVecDemo/static/' + str(randName) + '.png')
        image_url = str(randName) + '.png'
    #plt.show()

    return jsonify(answer=answer[0][0], image_url=image_url)

@app.route("/doesnt_match", methods=["POST"])
def doesnt_match():
    words = request.args.get(u"words")
    words = words.split()
    image_url = ''
    randName = random.randint(1, 100000)

    #if os.path.exists('AraVecDemo/static/new_plot.png'):
    #    os.remove("AraVecDemo/static/new_plot.png")
        
    for word in words:
        try:
            most_similar = model.wv.most_similar(word)
        except:
            return jsonify(answer=word + u" غير موجودة في القاموس")

    answer = model.doesnt_match(words)

    X1 = {}
    for x in words:
        X1[x] = model.wv.vocab[x]
    X = array([model[x] for x in model.wv.vocab if x in words])

    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
    # create a scatter plot of the projection
    plt.figure()
    plt.scatter(result[:, 0], result[:, 1])
    newwords = list(X1)
    for i, word in enumerate(newwords):
        word = arabic_reshaper.reshape(word)
        word = get_display(word)
        plt.annotate(word, xy=(result[i, 0], result[i, 1]))
        plt.savefig('AraVecDemo/static/' + str(randName) + '.png')
        image_url = str(randName) + '.png'
    #plt.show()

    return jsonify(answer=answer, image_url=image_url)

@app.route("/similarity", methods=["POST"])
def similarity():
    keys = request.args.get(u"words")
    keys = keys.split()
    image_url = ''
    randName = random.randint(1, 100000)

    #if os.path.exists('AraVecDemo/static/new_plot.png'):
    #    os.remove("AraVecDemo/static/new_plot.png")
        
    for key in keys:
        try:
            most_similar = model.wv.most_similar(key)
        except:
            return jsonify(answer=word + u" غير موجودة في القاموس")

    words = model.most_similar(keys, topn=20)
    words = [x for (x, i) in words]
    words.extend(keys)

    X1 = {}
    for x in words:
        X1[x] = model.wv.vocab[x]
    X = array([model[x] for x in model.wv.vocab if x in words])

    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
    # create a scatter plot of the projection
    plt.figure()
    plt.scatter(result[:, 0], result[:, 1])
    newwords = list(X1)
    for i, word in enumerate(newwords):
        word = arabic_reshaper.reshape(word)
        word = get_display(word)
        plt.annotate(word, xy=(result[i, 0], result[i, 1]))
        plt.savefig('AraVecDemo/static/' + str(randName) + '.png')
        image_url = str(randName) + '.png'
    #plt.show()

    return jsonify(image_url=image_url)
