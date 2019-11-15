from twilio.rest import Client


class Notifciation:
    def __init__(self):
        self.authCode = "0b794dd4d64f7851cca07fc2b99a0c38"
        self.accountSID = "ACf067728b0868e90f89450b908b273f71"
        self.number = "+12028914655"

    def send_messsage(self, message, toContact):
        client = Client(self.accountSID, self.authCode)
        message =client.messages.create(to=toContact, from_=self.number, body=message)
        return message
