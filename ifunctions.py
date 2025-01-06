class Message:
    def __init__(self):
        pass
    def user_mesasage(self,content):
        response = {"role": "user", "content": content}
        return response
    def system_mesasage(self,content):
        response = {"role": "system", "content": content}
        return response
    def assistant_mesasage(self,content):
        response = {"role": "assistant", "content": content}
        return response