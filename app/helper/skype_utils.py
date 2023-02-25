import os
from skpy import Skype, SkypeAuthException, SkypeApiException
from app.helper.logger import logger


class SkypeUtils(object):

    def __init__(self):

        self._username = os.environ["USERNAME"]
        self._password = os.environ["PASSWORD"]
        # Login with the credentials
        self._login()

    def _login(self):
        logger.info(
            "Connecting to Skype with {} as username".format(self._username))
        try:
            self.session = Skype(self._username, self._password)
        except SkypeAuthException:
            logger.error("Skype authenticaion Error!")
            raise
        except:
            logger.error("Cannot Login!")
            raise

    def _retry(func):
        """Retry decorator."""

        def wrapper(self, *args, **kwargs):
            MAX_ATTEMPTS = 2
            for attempt in range(1, MAX_ATTEMPTS + 1):
                try:
                    return func(self, *args, **kwargs)
                except SkypeApiException:
                    logger.warn(f"Attempt {attempt}/{MAX_ATTEMPTS} failed")
                    logger.warn("Token expired; Login again...")
                    self._login()
        return wrapper

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

    @_retry
    def send_message(self, chat_id: str, message: str):

        channel = self.session.chats.chat(chat_id)
        channel.sendMsg(message, rich=True)

skype_instance = SkypeUtils()
