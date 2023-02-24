import os

from skpy import Skype, SkypeMsg
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from typing import Any, Dict, List

from app.helper.skype_utils import SkypeUtils
from app.helper.text_utils import TextUtils

app = FastAPI()

username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

import logging

# setup loggers
logging.config.fileConfig('app/logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project. 
                                      # This will get the root logger since no logger in the configuration has this name.

class EvalMatch(BaseModel):
    value: int
    metric: str
    tags: Any


class Data(BaseModel):
    title: str
    ruleId: int
    ruleName: str
    state_: str = Field(..., alias='state ')
    evalMatches: List[EvalMatch]
    orgId: int
    dashboardId: int
    panelId: int
    tags: Dict[str, Any]
    ruleUrl: str
    imageUrl: str
    message: str

@app.post('/SkypeNotifier/{room_name}')
# data is the data sent from Grafana alert data is read in the format of JSON Json response is like follows: {
# 'title': '[Alerting] Test notification', 'ruleId': 7008839925862512012, 'ruleName': 'Test notification',
# 'state': 'alerting', 'evalMatches': [{'value': 100, 'metric': 'High value', 'tags': None}, {'value': 200,
# 'metric': 'Higher Value', 'tags': None}], 'orgId': 0, 'dashboardId': 1, 'panelId': 1, 'tags': {}, 'ruleUrl':
# 'http://localhost:3000/', 'imageUrl': 'https://grafana.com/assets/img/blog/mixed_styles.png', 'message':
# 'Someone is testing the alert notification within Grafana.'}
def notify(room_name, data:Data):
    # create token for login
    SkypeUtils.generate_token_if_not_exists(username, password, 'skype_token')
    # connect to Skype using provided user name and password
    skype_connect = Skype(username, password)
    # get the chat id of the given room name
    chat_id = SkypeUtils.translate_room_name(skype_connect, room_name)

    logger.info(data)
    try:
        # if there's a message, try to customize it for a skype message
        msg = ''
        msg = msg + '\n'
        # get the value of rule URL key
        # 'ruleUrl': 'http://localhost:3000/'
        url = str(data.ruleUrl)
        # since the Grafana sees itself as of localhost, we replace the
        # local host with its real IP
        url = url.replace('localhost', '172.1.1.1')
        # We have attached the IP as a clickable link
        # instead of showing: 172.1.1.1 in our skype message we put the rule title and
        # made the title clickable which redirects through the dashboard
        msg = msg + SkypeMsg.link(url, data.title)
        msg = msg + '\n'
        # this part is a list of problems we have received, sometimes more than one
        # metric is evaluated through a single alert, this part lists all the reported issues
        # 'evalMatches': [{'value': 100, 'metric': 'High value', 'tags': None},
        # {'value': 200, 'metric': 'Higher Value', 'tags': None}]
        evals = data.evalMatches
        # evals is a list of dictionaries which the key is the metric name and value is the metric value
        # these metric values have set our alert value to True
        if len(evals) == 0:
            pass
        else:
            for i in range(0, len(evals)):
                # append all metrics and their values to our message
                value = evals[i].value
                if isinstance(value, int):
                    # we add ',' for every 3 digits: 1000 is changed to 1,000 for ease of use
                    value = TextUtils.add_thousand_seperator(value)
                # the metric and its value is added to our skype message in bold format
                extra_msg = '\n ' + SkypeMsg.bold(evals[i].metric) + ' ' + str(value) + '\n '
                msg += extra_msg

        if 'No Data' not in msg:
            # this part is added since the alert is sent by Grafana no matter if there's an issue or not
            # no data means that there are no issues so we do no want to receive a skype message telling
            # us that everything is fine
            channel = skype_connect.chats.chat(chat_id)
            # mentioning all and sending our created message
            channel.sendMsg("<at id=\" * \">all</at> \n" + msg, rich=True)

    except Exception as e:
        logger.exception("An exception occurred:", str(e))

    return data


@app.post('/minio_notifications')
def minio_notifier(request: Request):

    # msg=request.data
    skype_connect = Skype(username, password)
    channel = skype_connect.contacts['live:.cid'].chat
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
    logger.info("HI")
    return 'Grafana Listener\n Use SkypeNotifier URI to receive messages on Skype on alerts'
