import os
from skpy import Skype, SkypeAuthException, SkypeMsg
from app.helper.logger import logger
from app.helper.text_utils import TextUtils
from app.helper.model import GrafanaAlert


class SkypeUtils(object):

    def __init__(self):

        username = os.environ["USERNAME"]
        password = os.environ["PASSWORD"]
        logger.info("Connecting to Skype with {} as username".format(username))
        try:
            self.session = Skype(username, password)
        except SkypeAuthException:
            logger.error("Skype authenticaion Error!")
            raise
        except:
            logger.error("Cannot Login!")
            raise

    def translate_room_name(self, room_name):
        # Skype uses group id to send messages to groups
        # finding group id is not easy without Pyhton so we get the group name and
        # look for its id in this method
        # the account should  be added to the group before hand
        recent_chats = self.session.chats.recent()
        for chat in recent_chats:
            if 'topic' in dir(recent_chats[chat]):
                group_name = recent_chats[chat].__getattribute__('topic')
                if group_name == room_name:
                    return chat


def grafana_message_transformer(grafana_message: GrafanaAlert):
    # if there's a message, try to customize it for a skype message
    msg = '\n'
    # get the value of rule URL key
    # 'ruleUrl': 'http://localhost:3000/'
    url = str(grafana_message.ruleUrl)
    # since the Grafana sees itself as of localhost, we replace the
    # local host with its real IP
    #url = url.replace('localhost', '172.16.77.69')
    # We have attached the IP as a clickable link
    # instead of showing: 172.16.77.69 in our skype message we put the rule title and
    # made the title clickable which redirects through the dashboard
    #msg = msg + SkypeMsg.link(url, data.title)
    msg = msg + url + '\n'
    # this part is a list of problems we have received, sometimes more than one
    # metric is evaluated through a single alert, this part lists all the reported issues
    # 'evalMatches': [{'value': 100, 'metric': 'High value', 'tags': None},
    # {'value': 200, 'metric': 'Higher Value', 'tags': None}]
    evals = grafana_message.evalMatches
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
            extra_msg = '\n ' + \
                SkypeMsg.bold(evals[i].metric) + ' ' + str(value) + '\n '
            msg += extra_msg

    return msg


skype_instance = SkypeUtils()
