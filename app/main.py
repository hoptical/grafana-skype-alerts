import os

from fastapi import FastAPI, Request, HTTPException, status, Depends

from app.helper.skype_utils import SkypeUtils
from app.helper.model import GrafanaAlert
from app.helper.logger import logger

app = FastAPI()


@app.on_event("startup")
def create_skype_instance():
    app.state.skype_instance = SkypeUtils(connect=True)

async def get_skype():
    yield app.state.skype_instance


@app.get('/api/skype/grafana_alert/{room_name}')
def room_name_to_chat_id(room_name,
                         skype_instance: SkypeUtils = Depends(get_skype)):
    chat_id = skype_instance.translate_room_name(room_name)
    if chat_id:
        return chat_id
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found!"
        )


@app.post('/api/skype/grafana_alert/{chat_id}')
def notify(chat_id, alert: GrafanaAlert, verbose: bool = False,
           skype_instance: SkypeUtils = Depends(get_skype)):

    logger.info("Grafana Alert Message %s", alert)
    skype_instance.send_message(
        chat_id, alert.model_representer(verbose=verbose))
    return "Grafana alert sent to the channel"


@app.post('/minio_notifications')
def minio_notifier(request: Request, skype_instance: SkypeUtils = Depends(get_skype)):

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


@app.post('/api/log_body')
async def log_requesst_body(request: Request):
    data = await request.json()
    logger.info(data)
