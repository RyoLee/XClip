#!/bin/sh
mkdir -p /config
if [ ! -f "/config/XClip.cfg" ];then
    cp /XClip.cfg.sample /config/XClip.cfg
fi
if [ ! -f "/config/data.db" ];then
    cp /data.db /config/data.db
fi
python /XClip.py