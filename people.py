# coding=utf-8
import socket, random, report, reveive

addrto = ('192.168.1.10', 8888)
BUFFSIZE = 1024


class player:
    def __init__(self, ID, field, mode):
        self.ID = ID
        self.field = field
        self.mode = mode
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addrto)

    def setTable(self, getMsg):
        self.table = getMsg['table']
        self.ownNick = getMsg['ownNick']
        self.ownCoin = getMsg['ownCoin']
        self.mateNick = getMsg['mateNick']
        self.mateCoin = getMsg['mateCoin']

    def setEgg(self, getMsg):
        self.egg = getMsg['egg']

    def changeState(self, getMsg):
        self.ownNick = getMsg['ownNick']
        self.ownCoin = getMsg['ownCoin']
        self.mateNick = getMsg['mateNick']
        self.mateCoin = getMsg['mateCoin']
        if getMsg['state'] == 0:
            self.egg.remove(getMsg['site'])
        if getMsg['addTag'] == 1:
            self.egg.append(getMsg['addSite'])

    def choose(self, getMsg):
        if getMsg['kind'] == 0x28:
            self.setTable(getMsg)
        elif getMsg['kind'] == 0x30:
            self.setEgg(getMsg)
        elif getMsg['kind'] == 0x32:
            self.changeState(getMsg)

    def recv(self):
        getMsg = self.sock.recv(BUFFSIZE)
        return getMsg

    def send(self, msg):
        self.sock.send(msg)


def creatPlayer(ID):
    aplayer = player(ID, random.choice([1, 2, 3]), random.choice([0, 1]))#create aplayer
    aplayer.send(report.chooseField(aplayer.ID, aplayer.field, aplayer.mode))#choose field and mode
    tableMsg = reveive.getTable(aplayer.recv())
    aplayer.setTable(tableMsg)#set table
    eggMsg = reveive.getEgg(aplayer.recv())
    aplayer.setEgg(eggMsg)#first set egg
    return aplayer
