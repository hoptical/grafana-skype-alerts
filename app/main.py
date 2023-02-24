import os

from fastapi import FastAPI, Request

from app.helper.skype_utils import skype_instance
from app.helper.model import GrafanaAlert
from app.helper.logger import logger

app = FastAPI()


@app.post('/api/skype/grafana_alert/{room_name}')
def notify(room_name, alert: GrafanaAlert):
    chat_id = skype_instance.translate_room_name(room_name)

    logger.info("Grafana Alert Message", alert)

    channel = skype_instance.session.chats.chat(chat_id)
    # mentioning all and sending our created message
    channel.sendMsg(str(alert), rich=True)

    return "Grafana alert sent to the channel"


@app.post('/minio_notifications')
def minio_notifier(request: Request):

    # msg=request.data
    channel = skype_instance.session.contacts['live:.cid'].chat
    # msg=request.data
    msg = request.json()
    bucket_name = str(msg['Key']).split('/')
    bucket = bucket_name[0]
    # TODO
    cmd = f'cmd /c "python C:\python_scripts\MinioWorker\main.py "{bucket}""'
    os.system(cmd)
    channel.sendMsg(cmd)

    return 'get'


@app.get('/')
def hello():
    return 'Grafana Listener\n Use SkypeNotifier URI to receive messages on Skype on alerts'


@app.get('/api/health')
def health_check():
    return "The server is healthy"
