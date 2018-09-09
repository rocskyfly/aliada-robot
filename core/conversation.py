# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
import time

from .brain import Brain
import sys

sys.path.append("..")
from client.notifier import Notifier
from utils import config
from client.drivers.pixels import Pixels


class Conversation(object):
    def __init__(self, persona, mic):
        self._logger = logging.getLogger(__name__)
        self.persona = persona
        self.mic = mic
        self.brain = Brain(mic)
        self.notifier = Notifier(config.get(), self.brain)
        self.wxbot = None
        self.pixels = None

        if config.has('signal_led'):
            signal_led_profile = config.get('signal_led')
            if signal_led_profile['enable'] and \
                    signal_led_profile['gpio_mode'] and \
                    signal_led_profile['pin']:
                self.pixels = Pixels(signal_led_profile['gpio_mode'], signal_led_profile['pin'])

    @staticmethod
    def is_proper_time():
        """
        whether it's the proper time to gather notifications without disturb user.
        """
        if not config.has('do_not_bother'):
            return True

        bother_profile = config.get('do_not_bother')
        if not bother_profile['enable']:
            return True
        if 'since' not in bother_profile or 'till' not in bother_profile:
            return True

        since = bother_profile['since']
        till = bother_profile['till']
        current = time.localtime(time.time()).tm_hour
        if till > since:
            return current not in range(since, till)
        else:
            return not (current in range(since, 25) or current in range(-1, till))

    def handle_forever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.info("Starting to handle conversation with keyword '%s'." % self.persona)
        while True:
            # Print notifications until empty
            if self.is_proper_time():
                notifications = self.notifier.getAllNotifications()
                for nf in notifications:
                    self._logger.info("Received notification: '%s'" % str(nf))
                    self.mic.say(str(nf))

            if self.mic.stop_passive:
                self._logger.info("skip conversation for now.")
                time.sleep(1)
                continue

            if not self.mic.skip_passive:
                self._logger.debug("Started listening for keyword '%s'" % self.persona)
                threshold, transcribed = self.mic.passive_listen(self.persona)
                self._logger.debug("Stopped listening for keyword '%s'" % self.persona)

                if not transcribed or not threshold:
                    self._logger.info("Nothing has been said or transcribed.")
                    continue
                self._logger.info("Keyword '%s' has been said!" % self.persona)
                # self.mic.play_no_block(aliadapath.data('audio', 'beep_hi.wav'))
            else:
                self._logger.debug("Skip passive listening")
                if not self.mic.chatting_mode:
                    self.mic.skip_passive = False
                continue

            if self.pixels:
                self.pixels.wakeup()

            # Start active listening after listening arousing keyword "persona", and handling what's user told?
            self._logger.info("Started to listen actively with threshold: %r" % threshold)

            text_content = self.mic.active_listen_to_all_options(threshold)
            self._logger.info("Stopped to listen actively with threshold: %r" % threshold)

            if self.pixels:
                self.pixels.think()

            if text_content:
                self.brain.query(text_content, self.wxbot)
            elif config.get('shut_up_if_no_input', False):
                self._logger.info("Active Listen return empty")
            else:
                self.mic.say(u"什么?")

            if self.pixels:
                self.pixels.off()
