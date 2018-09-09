# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import logging
import argparse
import threading
import traceback

from core import tts
from core import stt
from core.mic import Mic
from core.conversation import Conversation

sys.path.append("..")
from client import WechatBot
from utils import aliadapath
from utils import diagnose
from utils import config

# Add Aliada configuration path.LIB_PATH to sys.path
sys.path.append(aliadapath.LIB_PATH)

parser = argparse.ArgumentParser(description='Aliada Voice Control Center')
parser.add_argument('--local', action='store_true',
                    help='Use text input instead of a real microphone')
parser.add_argument('--no-network-check', action='store_true',
                    help='Disable the network connection check')
parser.add_argument('--diagnose', action='store_true',
                    help='Run diagnose and exit')
parser.add_argument('--debug', action='store_true', help='Show debug messages')
parser.add_argument('--info', action='store_true', help='Show info messages')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Directly print logs rather than writing to log file')
args = parser.parse_args()


class Aliada(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.wxBot = None
        config.init()

        tts_engine_slug = config.get('tts_engine', tts.get_default_engine_slug())
        tts_engine_class = tts.get_engine_by_slug(tts_engine_slug)

        stt_active_engine_slug = config.get('stt_engine', 'sphinx')
        stt_active_engine_class = stt.get_engine_by_slug(stt_active_engine_slug)

        stt_passive_engine_slug = config.get('stt_passive_engine', stt_active_engine_slug)
        stt_passive_engine_class = stt.get_engine_by_slug(stt_passive_engine_slug)

        self._logger.info("Active engine:%s; Passive engine:%s" % (stt_active_engine_slug, stt_passive_engine_slug))

        # Initialize Mic
        self.mic = Mic(
            tts_engine_class.get_instance(),
            stt_passive_engine_class.get_passive_instance(),
            stt_active_engine_class.get_active_instance())

    def start_wxbot(self):
        print(u"请扫描如下二维码登录微信")
        print(u"登录成功后，可以与自己的微信账号（不是文件传输助手）交互")
        self.wxBot.run(self.mic)

    def run(self):
        salutation = (u"%s，我能为您做什么?" % config.get("first_name", u'主人'))

        persona = config.get("robot_name", 'ALIADA')
        conversation = Conversation(persona, self.mic)

        # create wechat robot
        if config.get('wechat', False):
            self.wxBot = WechatBot.WechatBot(conversation.brain)
            self.wxBot.DEBUG = True
            self.wxBot.conf['qr'] = 'tty'
            conversation.wxbot = self.wxBot
            t = threading.Thread(target=self.start_wxbot)
            t.start()

        self.mic.say(salutation, cache=True)
        conversation.handle_forever()


if __name__ == "__main__":
    print(u'''
*********************************************************************
*            Aliada - Chinese Speech Dialogue Car Robot             *
*              (c) 2017 Rocky.Qi <rocskyfly@gmail.com>              *
*         https://github.com/rocskyfly/aliada-car-robot.git         *
*********************************************************************
''')
    if args.verbose:
        logging.basicConfig(
            format='%(asctime)s %(filename)s[line:%(lineno)d] '
                   + '%(levelname)s: %(message)s',
            level=logging.INFO)
    else:
        logging.basicConfig(
            filename=os.path.join(
                aliadapath.TEMP_PATH, "aliada.log"
            ),
            filemode="w",
            format='%(asctime)s %(filename)s[line:%(lineno)d] '
                   + '%(levelname)s: %(message)s',
            level=logging.INFO)

    logger = logging.getLogger()
    logger.getChild("client.stt").setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.info:
        logger.setLevel(logging.INFO)

    if not args.no_network_check and not diagnose.check_network_connection():
        logger.warning("Network not connected. This may prevent Aliada " +
                       "from running properly.")

    if args.diagnose:
        failed_checks = diagnose.run()
        sys.exit(0 if not failed_checks else 1)

    try:
        app = Aliada()
    except Exception, e:
        logger.exception("Error occured! details:%s" % e)
        sys.exit(1)

    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Aliada get Keyboard Interrupt, exit.")
        print("Aliada exit.")
    except Exception, e:
        logger.exception("Aliada quit unexpectedly!details:%s" % e)
        if not args.verbose:
            msg = traceback.format_exc()
            print("** Aliada quit unexpectedly! ** ")
            print(msg)
        sys.exit(1)
