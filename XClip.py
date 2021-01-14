#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import hashlib
import threading
from flask import Flask, request, abort, redirect
from configparser import ConfigParser
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()


def getMD5(s0):
    m = hashlib.md5()
    m.update(bytes(str(s0), encoding='utf-8'))
    return m.hexdigest()


def cleanPool():
    tn = int(time.time())
    rdict = dict()
    for k in datapool:
        (v, l, t) = datapool[k]
        if tn-t >= 300:
            l.acquire()
            if tn-t >= 300:
                rdict[k] = l
            else:
                l.release()
    for k in rdict:
        datapool.pop(k)
        rdict[k].release()


@app.route('/', methods=['post', 'get'])
def usage():
    return redirect('https://github.com/RyoLee/XClip')


@app.route('/ping', methods=['post', 'get'])
def ping():
    return 'pong'


@app.route('/set', methods=['post'])
def setValue():
    key = request.form.to_dict()["key"]
    value = request.form.to_dict()["value"]
    pw = request.form.to_dict()["password"]
    tn = int(time.time())
    if mainpw == pw:
        if key in datapool:
            v, l, t = datapool[key]
            l.acquire()
            datapool[key] = (value, l, tn)
            l.release()
        else:
            lock = threading.Lock()
            datapool[key] = (value, lock, tn)
        return 'Done'
    else:
        abort(403)


@app.route('/get', methods=['post'])
def getValue():
    key = request.form.to_dict()["key"]
    pw = request.form.to_dict()["password"]
    if mainpw == pw:
        if key in datapool:
            v, l, t = datapool[key]
            return v
        else:
            return ''
    else:
        abort(403)


cp = ConfigParser()
cp.read('/config/XClip.cfg')
host = cp.get('main', 'host')
port = int(cp.get('main', 'port'))
debug = ("1" == cp.get('main', 'debug'))
mainpw = getMD5(cp.get('main', 'password'))
datapool = dict()
if __name__ == '__main__':
    scheduler.init_app(app=app)
    scheduler.start()
    scheduler.add_job(func=cleanPool, args=(),
                      trigger='interval', minutes=1, id='cleanDatapool')
    app.run(host=host, port=port, debug=debug)
