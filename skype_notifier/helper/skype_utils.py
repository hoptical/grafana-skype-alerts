from pathlib import Path

from skpy import Skype, SkypeAuthException


class SkypeUtils(object):

    @staticmethod
    def __create_token_file(token_file):
        file = Path(token_file)
        file.touch(exist_ok=True)
        open(file)

    @staticmethod
    def generate_token_if_not_exists(username, password, token_file):
        # Skype uses token for authentication. Also it is possible to work without token but
        # inorder to be reusable, better to use token
        s = Skype(connect=False)
        s.conn.setTokenFile(token_file)
        try:
            s.conn.readToken()
        except SkypeAuthException:
            SkypeUtils.__create_token_file(token_file)
            s.conn.setUserPwd(username, password)
            s.conn.getSkypeToken()
            s.conn.writeToken()

    @staticmethod
    def translate_room_name(skype_connect, room_name):
        # Skype uses group id to send messages to groups
        # finding group id is not easy without Pyhton so we get the group name and
        # look for its id in this method
        # the account should  be added to the group before hand
        recent_chats = skype_connect.chats.recent()
        for chat in recent_chats:
            if 'topic' in dir(recent_chats[chat]):
                group_name = recent_chats[chat].__getattribute__('topic')
                if group_name == room_name:
                    return chat
