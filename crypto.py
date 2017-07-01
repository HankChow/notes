#!/usr/bin/python3
# coding: utf-8

import base64
import sys
import time
import zlib


def crypto(enc_series, content):
    is_encode = enc_series[0]
    if is_encode:
        output = content.encode('utf-8')
    else:
        output = content
    for item in encrypt_series[1:-1]:
        if item == 'b64':
            if is_encode:
                output = base64.b64encode(output)
            else:
                ### Python 关于 Base64 decode 的坑 ###
                # 当长度不是4的倍数时，decode 会报 incorrect padding error，需要补足
                missing_padding = 4 - len(output) % 4
                if missing_padding:
                    output += b'=' * missing_padding
                ### Python 关于 Base64 decode 的坑 ###
                output = base64.b64decode(output)
        if item == 'compress':
            if is_encode:
                output = zlib.compress(output)
            else:
                output = zlib.decompress(output)
    if not is_encode:
        output = output.decode('utf-8')
    return output


def encode():
    global encrypt_series
    notes = open('notes.md', 'r').read()
    open('encrypted.txt', 'wb').write(crypto(encrypt_series, notes))
    print('encoded.')


def decode():
    global encrypt_series
    encrypt_series.reverse()
    encrypted = open('encrypted.txt', 'rb').read()
    nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    open('note{0}.md'.format(nowtime), 'w').write(crypto(encrypt_series, encrypted))
    print('decoded.')


if __name__ == '__main__':
    encrypt_series = [True, 'b64', 'compress', False]
    execution = input('Execution:')
    if execution == 'encode':
        encode()
    elif execution == 'decode':
        decode()
    else:
        print('Did nothing.')
