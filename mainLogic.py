# IDE : PyCharm Community Edition 5.0.3
# Development language : Python 3.5.1
# this is the client main logic used to test the server performance
import random
import select
import threading
import time

import people
import receive
import report

players = []
sockets = []
BUFFSIZE = 1024
playerNum = 2
aGroup = 2
groupNum = int(playerNum / aGroup)


def createPlayer():
    for i in range(playerNum):
        aplayer = people.creatPlayer(i)
        sockets.append(aplayer.sock)
        players.append(aplayer)
        print('--------------create player %d succeed--------------' % i)
    print('--------------------create %d player in players[]--------------------' % len(players))


def getMsg():
    while True:
        try:
            sock, se, err = select.select(sockets, [], [], 5)
            for re in sock:
                msg = receive.getKind(re.recv(BUFFSIZE))  # recv msg
                players[msg['ID']].choose(msg)  # msg function
        except Exception as e:
            pass


def hit():
    while True:
        try:
            aplayer = random.choice(players)
            print('ID:%d,field:%d,table:%d,mode:%d,ownNick:%s,ownCoin:%d,mateNick:%s,mateCoin:%d,position'
                  % (aplayer.ID, aplayer.field, aplayer.table, aplayer.mode, aplayer.ownNick, aplayer.ownCoin,
                     aplayer.mateNick, aplayer.mateCoin), end="")
            for i in aplayer.egg:
                print(' %d ' % i, end="")
            print('have eggs')
            aplayer.send(report.hitEgg(aplayer.ID, aplayer.table, aplayer.field, random.choice(aplayer.egg)))
            # time.sleep(5)
            # time.sleep(random.uniform(0, 3))
        except Exception as e:
            time.sleep(5)
        finally:
            time.sleep(5)


t1 = threading.Thread(target=createPlayer)
t2 = threading.Thread(target=hit)
t3 = threading.Thread(target=getMsg)
t1.start()
t2.start()
t3.start()

# for i in range(groupNum):
#    threading._start_new_thread(hit, ())
while True:
    pass
