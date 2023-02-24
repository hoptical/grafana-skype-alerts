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
        while self.session.chats.recent():
            pass  # Just populate the cache.

        for chat in self.session.chats:
            try:
                topic = chat.topic
                if topic == room_name:
                    return chat.id
            except AttributeError:
                pass            
                
        logger.error("Room Name not found!")
        return None

skype_instance = SkypeUtils()
