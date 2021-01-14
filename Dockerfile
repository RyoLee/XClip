FROM python:3.7.9-alpine
ADD ./XClip.cfg.sample /
ADD ./XClip.py /
ADD ./entrypoint.sh /
RUN pip install flask Flask-APScheduler \
&& chmod +x /entrypoint.sh
WORKDIR /
ENTRYPOINT ["/entrypoint.sh"]