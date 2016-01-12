# coding=utf-8
import struct

fields = {1: 'farm', 2: 'forest', 3: 'Jurassic Period'}
modes = {1: 'VIP', 2: 'normal'}


def chooseField(ID, field, mode):
    head, kind, ID, field, mode, end = 0x0a, 0x27, ID, field, mode, 0x55
    size = struct.calcsize('!HBB')
    msg = struct.pack('!BBBHBBB', head, kind, size, ID, field, mode, end)
    print('>>>>>>>Client:player %d play in field %s and mode is %s' % (ID, field, mode))
    return msg


def hitEgg(ID, table, field, site):
    head, kind, ID, table, field, site, end = 0x0a, 0x31, ID, table, field, site, 0x55
    size = struct.calcsize('!HHBB')
    msg = struct.pack('!BBBHHBBB', head, kind, size, ID, table, field, site, end)
    print('>>>>>>>Client:player %d player in field %s on %d table,hit the NO.%d egg' % (ID, fields[field], table, size))
    return msg


def morra(ID, stone, fabric, scissor):
    head, kind, ID, stone, fabric, scissor, end = 0x0a, 0x35, ID, stone, fabric, scissor, 0x55
    size = struct.calcsize('!HIII')
    msg = struct.pack('!BBBHIIIB', head, kind, size, ID, stone, fabric, scissor, end)
    print('>>>>>>>Client:player %d bet stone %d,fabric %d,scissor %d' % (ID, stone, fabric, scissor))
    return msg
