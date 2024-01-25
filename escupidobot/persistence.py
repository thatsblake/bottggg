import json
import datetime
from escupidobot.model import Message


class DataEngine:

    @staticmethod
    def save(user, target, message):
        with open('data.json', 'a+') as file:
            date = datetime.datetime.now()
            new_data = {
                'source': user['username'],
                'target': target,
                'when': str(date),
                'text': message
            }
            json.dump(new_data, file)
            file.write("\n")

    @staticmethod
    def read(user):
        username = '@' + user['username']
        with open('data.json', 'r') as file:
            lines = file.readlines()
            messages = list(map(lambda x: Message(x), lines))
            return list(filter(lambda x: x.target == username, messages))

