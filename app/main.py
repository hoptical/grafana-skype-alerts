import os

from fastapi import FastAPI, Request, HTTPException, status, Depends

from app.helper.skype_utils import SkypeUtils
from app.helper.model import GrafanaAlert
from app.helper.logger import logger

app = FastAPI()

# Create skype instance on startup and share it between requests
@app.on_event("startup")
def create_skype_instance():
    app.state.skype_instance = SkypeUtils(connect=True)

# Dependency function (get called on every request being depened on) 
async def get_skype():
    yield app.state.skype_instance

# Convert room name to chat id
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

# Post a Grafana alert to Skype 
@app.post('/api/skype/grafana_alert/{chat_id}')
def notify(chat_id, alert: GrafanaAlert, verbose: bool = False,
           skype_instance: SkypeUtils = Depends(get_skype)):

    logger.info("Grafana Alert Message %s", alert)
    try:
        skype_instance.send_message(
            chat_id, alert.model_representer(verbose=verbose))
    except:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Attempt on request has failed. It may be because of the wrong ChatId."
        )
    return "Grafana alert sent to the channel"


@app.get('/')
def hello():
    return 'Grafana Listener\n Use SkypeNotifier URI to receive messages on Skype on alerts'


# Called by Kubernetes
@app.get('/api/health')
def health_check():
    return "The server is healthy"


@app.post('/api/log_body')
async def log_requesst_body(request: Request):
    data = await request.json()
    logger.info(data)
