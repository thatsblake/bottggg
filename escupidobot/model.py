import json


class InputBot:
    def __init__(self, token):
        self.token = token


class Message:

    def __init__(self, line):
        data = json.loads(line)
        self.source = data['source']
        self.target = data['target']
        self.text = data['text']
        self.when = data['when']

    def __str__(self):
        return "Message from " + self.source + " to " + self.target + ": " + self.text
