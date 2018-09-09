# -*- coding: utf-8 -*-
import logging
from socket import *
import sys

sys.path.append("..")
from utils import aliadapath
import RPi.GPIO as GPIO
import time
import threading

reload(sys)
sys.setdefaultencoding('utf8')

# Standard module stuff
WORDS = ["XINGZOU"]
SLUG = "robot_walk"

u"""电机驱动接口定义
ENA = 13  L298使能A
ENB = 20  L298使能B
IN1 = 19  电机接口1
IN2 = 16  电机接口2
IN3 = 21  电机接口3
IN4 = 26  电机接口4
"""
ENA = 13
ENB = 20
IN1 = 19
IN2 = 16
IN3 = 21
IN4 = 26


def isValid(text):
    """
        Returns True if the input is related to music.
        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text for word in [u"行走", u"走两步", u"前进",
                                         u"后退", u"左转", u"右转",
                                         u"后退", u"过来"])


def beforeListen(mic, profile, wxbot=None):
    # Todo: need to be verified, using mic.play_block() to play these wav file.
    mic.play(aliadapath.data('audio', 'beep_hi.wav'))


def afterListen(mic, profile, wxbot=None):
    # Todo: need to be verified, using mic.play() to play these wav file.
    mic.play_no_block(aliadapath.data('audio', 'beep_lo.wav'))


def handle(text, mic, profile, wxbot=None):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        wxbot -- wechat bot instance
    """
    logger = logging.getLogger(__name__)
    logger.debug("Preparing to start robot walking mode")
    try:
        motor = Motor()
    except Exception as e:
        logger.error("Couldn't start walk mode:%s" % e, exc_info=True)
        mic.say(u"行走模式失败了，请稍后再试")
        return
    persona = 'ALIADA'
    if 'robot_name' in profile:
        persona = profile['robot_name']

    robot_name_cn = u'阿里阿达'
    if 'robot_name_cn' in profile:
        robot_name_cn = profile['robot_name_cn']

    walk_mode = WalkMode(persona, robot_name_cn, mic, motor, wxbot)
    walk_mode.stop = False
    mic.say(u"进入语音行走控制模式，请发出具体语音指令！")
    walk_mode.handle_forever()


class WalkMode(object):
    def __init__(self, PERSONA, robot_name_cn, mic, motor, wxbot=None):
        self._logger = logging.getLogger(__name__)
        self.persona = PERSONA
        self.robot_name_cn = robot_name_cn
        self.mic = mic
        self.motor = motor
        self.wxbot = wxbot
        self.search_mode = False
        self.to_listen = True
        self.delegating = False
        self.is_stop = False
        if self.wxbot is not None:
            self.msg_thread = threading.Thread(target=self.wxbot.proc_msg)

    def delegate_input(self, orders, call_by_wechat=False):
        command = orders.upper()
        if command.startswith(self.robot_name_cn + ": "):
            return

        if call_by_wechat:
            self._logger.debug('called by wechat')
            self.motor.stop()
            time.sleep(.1)

        if u"前进" in command:
            self.mic.say(u"往前走一步")
            self.motor.gogo()
            time.sleep(1)
            self.motor.stop()
            return
        elif u"后退" in command:
            self.mic.say(u"往后退一步")
            self.motor.back()
            time.sleep(1)
            self.motor.stop()
            return
        elif u"左转" in command:
            self.mic.say(u"左转")
            self.motor.go_left()
            time.sleep(0.5)
            self.motor.stop()
            return
        elif u"右转" in command:
            self.mic.say(u"右转")
            self.motor.go_right()
            time.sleep(0.5)
            self.motor.stop()
            return

    def handle_forever(self):
        if self.wxbot is not None:
            self.msg_thread.start()

        while True:
            if self.motor.is_stop:
                self._logger.info('Stop robot walk mode')
                return

            if not self.to_listen or self.delegating:
                self._logger.info("Listening mode is disabled.")
                continue
            try:
                self._logger.info('离线唤醒监听中')
                threshold, transcribed = self.mic.passive_listen(self.persona)
            except Exception, e:
                self._logger.debug(e)
                threshold, transcribed = (None, None)

            if not transcribed or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue

            # 当听到呼叫机器人名字时，停止
            self.motor.stop()
            time.sleep(.1)

            # 听用户说话
            order = self.mic.active_listen(MUSIC=True)

            if order:
                if any(ext in order for ext in [u"结束", u"退出", u"停止"]):
                    self.mic.say(u"退出行走模式")
                    self.motor.stop()
                    self.motor.exit()
                    return
                if not self.delegating:
                    self.delegating = True
                    self.delegate_input(order)
                    self.delegating = False
            else:
                self.mic.say(u"什么？")


class Motor(object):
    def __init__(self):
        self.is_stop = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # 电机初始化为LOW
        GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

    # 定义电机正转函数
    @staticmethod
    def gogo():
        print 'motor_gogo'
        GPIO.output(ENA, True)
        GPIO.output(IN1, False)
        GPIO.output(IN2, True)

        GPIO.output(ENB, True)
        GPIO.output(IN3, False)
        GPIO.output(IN4, True)

    @staticmethod
    def go_right():
        print 'motor_lef'
        GPIO.output(ENA, False)
        GPIO.output(IN1, False)
        GPIO.output(IN2, False)

        GPIO.output(ENB, True)
        GPIO.output(IN3, False)
        GPIO.output(IN4, True)

    @staticmethod
    def go_left():
        print 'motor_lef'
        GPIO.output(ENA, True)
        GPIO.output(IN1, False)
        GPIO.output(IN2, True)

        GPIO.output(ENB, False)
        GPIO.output(IN3, False)
        GPIO.output(IN4, False)

    # 定义电机反转函数
    @staticmethod
    def back():
        print 'motor back'
        GPIO.output(ENA, True)
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)

        GPIO.output(ENB, True)
        GPIO.output(IN3, True)
        GPIO.output(IN4, False)

    # 定义电机停止函数
    @staticmethod
    def stop():
        print 'motor_stop'
        GPIO.output(ENA, False)
        GPIO.output(ENB, False)
        GPIO.output(IN1, False)
        GPIO.output(IN2, False)
        GPIO.output(IN3, False)
        GPIO.output(IN4, False)

    def exit(self):
        self.is_stop = True
