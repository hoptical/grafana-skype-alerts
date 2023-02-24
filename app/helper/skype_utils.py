import os
from skpy import Skype, SkypeAuthException
from app.helper.logger import logger


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

skype_instance = SkypeUtils()
