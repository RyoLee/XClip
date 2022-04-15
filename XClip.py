#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import hashlib
import threading
from flask import Flask, request, abort, redirect
from configparser import ConfigParser
from flask_apscheduler import APScheduler
import sqlite3

app = Flask(__name__)
scheduler = APScheduler()


def get_md5(s0):
    m = hashlib.md5()
    m.update(bytes(str(s0), encoding="utf-8"))
    return m.hexdigest()


def clean_pool():
    tn = int(time.time())
    rdict = dict()
    for k in datapool:
        (v, l, t) = datapool[k]
        if tn - t >= 300:
            l.acquire()
            if tn - t >= 300:
                rdict[k] = l
            else:
                l.release()
    for k in rdict:
        datapool.pop(k)
        rdict[k].release()


@app.route("/", methods=["post", "get"])
def home_page():
    return redirect("https://github.com/RyoLee/XClip")


@app.errorhandler(404)
def resource_not_found(e):
    return redirect("https://github.com/RyoLee/XClip")


@app.route("/ping", methods=["post", "get"])
def ping():
    return "pong"


@app.route("/<id>", methods=["post"])
def set_value(id):
    if id not in users:
        abort(403)
    else:
        username, pw_hash = users[id]
        token = request.headers.get("token").casefold()
        value = request.form.to_dict()["value"]
        if token not in get_tokens(pw_hash.casefold()):
            abort(403)
        else:
            tn = int(time.time())
            if id in datapool:
                v, l, t = datapool[id]
                l.acquire()
                datapool[id] = (value, l, tn)
                l.release()
            else:
                lock = threading.Lock()
                datapool[id] = (value, lock, tn)
            return "done"


@app.route("/<id>", methods=["get"])
def get_value(id):
    if id not in users:
        abort(403)
    else:
        username, pw_hash = users[id]
        token = request.headers.get("token").casefold()
        if token not in get_tokens(pw_hash.casefold()):
            abort(403)
        else:
            if id in datapool:
                v, l, t = datapool[id]
                return v
            else:
                return ("", 204)


def get_tokens(pw_hash):
    tokens = []
    ts = int(time.time())
    salt = (ts - ts % 10) / 10
    tokens.append(get_md5(pw_hash + str(ts % 10 - 1)).casefold())
    tokens.append(get_md5(pw_hash + str(ts % 10)).casefold())
    tokens.append(get_md5(pw_hash + str(ts % 10 + 1)).casefold())
    return tokens


cp = ConfigParser()
cp.read("/config/XClip.cfg")
host = cp.get("main", "host")
port = int(cp.get("main", "port"))
debug = "1" == cp.get("main", "debug")
datapool = dict()
users = dict()
if __name__ == "__main__":
    conn = sqlite3.connect("/config/data.db")
    cur = conn.cursor()
    res = cur.execute("select id,name,passowrd from users where flag =1 ")
    for row in res:
        users[row[0]] = (row[1], row[2])
    conn.close()
    scheduler.init_app(app=app)
    scheduler.start()
    scheduler.add_job(
        func=clean_pool, args=(), trigger="interval", minutes=1, id="clean_datapool"
    )
    app.run(host=host, port=port, debug=debug)
