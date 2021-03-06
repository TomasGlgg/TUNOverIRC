import irc.client


class IRC:
    reactor = irc.client.Reactor()
    privmsg_handler = None

    def __on_privmsg(self, _, event):
        message = event.arguments[0]
        self.privmsg_handler(message)

    def __on_nicknameinuse(self, _, __):
        print('Error: IP address already in use')
        exit(1)

    def __on_connect(self, _, __):
        print('IRC connected. Nick: {}'.format(self.nick))
        self.client.mode(self.nick, '+Bx')

    def __init__(self, host, port, nick):
        self.client = self.reactor.server()
        self.client.connect(host, port, nick)
        self.client.add_global_handler('privmsg', self.__on_privmsg)
        self.client.add_global_handler('welcome', self.__on_connect)
        self.client.add_global_handler('nicknameinuse', self.__on_nicknameinuse)
        self.send = self.client.privmsg
        self.nick = nick

    def connect_privmsg(self, function):
        self.privmsg_handler = function

    def process(self):
        self.reactor.process_forever()

