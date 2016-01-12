# coding =utf-8
import struct


def getTable(getMsg):
    head, kind, size, table, ownNick, ownCoin, mateNick, mateCoin, end = struct.unpack('!BBBH4sI4sIB', getMsg)
    ownNick = ownNick.decode('utf-8')
    mateNick = mateNick.decode('utf-8')
    getMsg = {'head': head, 'kind': kind, 'size': size, 'table': table, 'ownNick': ownNick,
              'ownCoin': ownCoin, 'mateNick': mateNick, 'mateCoin': mateCoin, 'end': end}
    print('<<<<<<<Server:you are playing in table %d,your nick is %s,your coin is %d;your mate\'s nick is %s,'
          'your mate\'s coin is %d' % (table, ownNick, ownCoin, mateNick, mateCoin))
    return getMsg


def getEgg(getMsg):
    head, kind, size, ID, eggList, end = struct.unpack('!BBBHIB', getMsg)
    a = 0x0001
    egg = []
    for i in range(32):
        if a & eggList == 1:
            egg.append(i+1)
        eggList = eggList >> 1

    getMsg = {'head': head, 'kind': kind, 'size': size, 'ID': ID, 'egg': egg, 'end': end}
    print('<<<<<<<Server:To player %d:the ' % ID, end="")
    for i in egg:
        print(' %d ' % i, end="")
    print('positions have eggs')
    return getMsg


def getState(getMsg):
    head, kind, size, ID, site, state, WinnerNick, prize, ownNick, ownCoin, mateNick, mateCoin, addTag, addSite, end = \
        struct.unpack('!BBBHBB4sI4sI4sIBBB', getMsg)
    WinnerNick = WinnerNick.decode('utf-8')
    ownNick = ownNick.decode('utf-8')
    mateNick = mateNick.decode('utf-8')
    getMsg = {'head': head, 'kind': kind, 'size': size, 'ID': ID, 'site': site, 'state': state,
              'winnerNick': WinnerNick, 'prize': prize, 'ownNick': ownNick, 'ownCoin': ownCoin,
              'mateNick': mateNick, 'mateCoin': mateCoin, 'addTag': addTag, 'addSite': addSite, 'end': end}
    if state != 0:
        print('<<<<<<<Server:To player %d:the NO.%d position\'s egg is the NO.%d times been hit,がんばれ!'
              % (ID, site, state))
    elif state == 0:
        print('<<<<<<<Server:To player %d:the NO.%d position\'s egg was broken,player %s break it and get %d '
              'coins,congratulations!' % (ID, site, WinnerNick, prize))
    if addTag == 1:
        print('<<<<<<<Server:To player %d:the position %d will be add a egg' % (ID, addSite))
    print('<<<<<<<Server:To player %d:now your have %d coins,your mate have %d coins' % (ID, ownCoin, mateCoin))
    return getMsg


def morraBegin(getMsg):
    head, kind, size, beginTag, end = struct.unpack('!BBBBB', getMsg)
    getMsg = {'head': head, 'kind': kind, 'size': size, 'beginTag': beginTag, 'end': end}
    if beginTag == 1:
        print('<<<<<<<Server:morra began!')
    return getMsg


def morraAmount(getMsg):
    head, kind, size, stoneAmount, scissorAmount, fabricAmount, end = struct.unpack('!BBBIIIB', getMsg)
    getMsg = {'head': head, 'kind': kind, 'size': size, 'stoneAmount': stoneAmount, 'scissorAmount': scissorAmount,
              'fabricAmount': fabricAmount, 'end': end}
    print('<<<<<<<Server:now stoneAmount is %d,scissorAmount is %d,fabricAmount is %d'
          % (stoneAmount, scissorAmount, fabricAmount))
    return getMsg


def morraResult(getMsg):
    head, kind, size, ID, result, end = struct.unpack('!BBBHiB', getMsg)
    getMsg = {'head': head, 'kind': kind, 'size': size, 'ID': ID, 'result': result, 'end': end}
    print('<<<<<<<Server:To player %d:in this morra ,your get %d coins' % (ID, result))
    return getMsg


kindType = {0x28: getTable, 0x30: getEgg, 0x32: getState, 0x34: morraBegin, 0x36: morraAmount, 0x38: morraResult}


def getKind(getMsg):
    # kind=struct.unpack('!B',getMsg[1])
    kind = getMsg[1]
    msg = kindType[kind](getMsg)
    return msg
