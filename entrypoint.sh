#!/bin/sh
mkdir -p /config
if [ ! -f "/config/XClip.cfg" ];then
    cp /XClip.cfg.sample /config/XClip.cfg
fi
python /XClip.py