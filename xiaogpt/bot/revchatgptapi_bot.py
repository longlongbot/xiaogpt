from revChatGPT.V1 import Chatbot, AsyncChatbot
from rich import print

from xiaogpt.bot.base_bot import BaseBot
from xiaogpt.utils import split_sentences


class RevChatGPTBot(BaseBot):
    def __init__(self, access_token, api_base=None, proxy=None):
        self.history = []
        self.asyncChatbot = AsyncChatbot(config={ "access_token": access_token})
        self.chatbot = Chatbot(config={ "access_token": access_token})

    async def ask(self, query, **options):
        ms = []
        for h in self.history:
            ms.append({"role": "user", "content": h[0]})
            ms.append({"role": "assistant", "content": h[1]})
        ms.append({"role": "user", "content": f"{query}"})
        
        completion = self.chatbot.ask(query, **options)
        for data in completion:
            message = data["message"]

        self.history.append([f"{query}", message])
        # only keep 5 history
        first_history = self.history.pop(0)
        self.history = [first_history] + self.history[-5:]
        print(message)
        return message        
        
    async def ask_stream(self, query, **options):
        ms = []
        for h in self.history:
            ms.append({"role": "user", "content": h[0]})
            ms.append({"role": "assistant", "content": h[1]})
        ms.append({"role": "user", "content": f"{query}"})
        completion = self.asyncChatbot.ask(query, **options)
        message = ""
        try:
            async for data in completion:
                delta = data["message"][len(message) :]
                message = data["message"]
                yield delta
        finally:
            print()
            self.history.append([f"{query}", message])
            first_history = self.history.pop(0)
            self.history = [first_history] + self.history[-5:]

