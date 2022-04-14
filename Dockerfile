FROM python:3-alpine
ADD ./XClip.cfg.sample /
ADD ./XClip.py /
ADD ./entrypoint.sh /
ADD ./data.db /
RUN pip install flask Flask-APScheduler \
&& chmod +x /entrypoint.sh
WORKDIR /
ENTRYPOINT ["/entrypoint.sh"]