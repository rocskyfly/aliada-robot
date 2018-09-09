# -*- coding: utf-8 -*-
# 获取IP插件
import logging
import sys
import time
import socket
import subprocess

reload(sys)
sys.setdefaultencoding('utf8')

WORDS = ["IP"]
SLUG = "speak_ip"


def getLocalIP():
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 0))
        ip = s.getsockname()[0]
    except:
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
    if ip.startswith("127."):
        cmd = '''/sbin/ifconfig | grep "inet " | cut -d: -f2 | awk '{print $1}' | grep -v "^127."'''
        a = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        a.wait()
        out = a.communicate()
        ip = out[0].strip().split("\n")  # 所有的列表
        if len(ip) == 1 and ip[0] == "" or len(ip) == 0:
            return False
        ip = '完毕'.join(ip)
    return ip


def handle(text, mic, profile, wxbot=None):
    logger = logging.getLogger(__name__)
    try:
        count = 0
        while True:
            ip = getLocalIP()
            logger.debug('getLocalIP: ', ip)

            if not ip:
                mic.say('正在获取中')
            else:
                count += 1
                mic.say("本机网络地址为：%s" % ip)
            if count == 1:
                break
            time.sleep(1)
    except Exception, e:
        logger.error(e)
        mic.say('抱歉，我没有获取到本机网络地址!')


def isValid(text):
    return any(word in text for word in [u"IP", u"网络地址"])
