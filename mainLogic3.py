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

players = {}
sockets = {}
BUFFSIZE = 1024
playerNum = 200
aGroup = 20
groupNum = int(playerNum / aGroup)
lock = threading.RLock()


def createPlayer(group):
    for i in range(aGroup):
        try:
            aplayer = people.creatPlayer(i + (group - 1) * aGroup)
            sockets[i + (group - 1) * aGroup] = aplayer.sock
            players[i + (group - 1) * aGroup] = aplayer
            print('··················create player %d succeed··················'
                  % (i + (group - 1) * aGroup))
        except Exception as e:
            print('#####################################################################################', e)


def getMsg():
    while True:
        try:
            sock, se, err = select.select(list(sockets.values()), [], [], 5)
            for re in sock:
                msg = receive.getKind(re.recv(BUFFSIZE))  # recv msg
                players[msg['ID']].choose(msg)  # msg function
        except Exception as e:
            pass


def hit(group):
    while True:
        try:
            NO = random.randint((group - 1) * aGroup, group * aGroup)
            aplayer = players[NO]
            print('ID:%d,field:%d,table:%d,mode:%d,ownNick:%s,ownCoin:%d,mateNick:%s,mateCoin:%d,position'
                  % (aplayer.ID, aplayer.field, aplayer.table, aplayer.mode, aplayer.ownNick, aplayer.ownCoin,
                     aplayer.mateNick, aplayer.mateCoin), end="")
            for i in aplayer.egg:
                print(' %d ' % i, end="")
            print('have eggs')
            aplayer.send(report.hitEgg(aplayer.ID, aplayer.table, aplayer.field, random.choice(aplayer.egg)))
            aplayer.time1 = time.time()
            # time.sleep(5)
            # time.sleep(random.uniform(0, 3))
        except Exception as e:
            time.sleep(random.uniform(0, 1))
        finally:
            time.sleep(random.uniform(0, 1))


for i in range(1, groupNum + 1):
    t1 = threading.Thread(target=createPlayer, args=(i,)).start()
    t2 = threading.Thread(target=hit, args=(i,)).start()
t3 = threading.Thread(target=getMsg).start()

# for i in range(groupNum):
#    threading._start_new_thread(hit, ())
while True:
    print('\n\n\n\n\n·············································'
          '·············································Count：%d'
          % len(players))
    time.sleep(10)
