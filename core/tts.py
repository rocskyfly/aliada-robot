# -*- coding: utf-8 -*-
"""
A Speaker handles audio output from Aliada to the user

Speaker methods:
    say - output 'phrase' as speech
    player - player the audio in 'filename'
    is_available - returns True if the platform supports this implementation
"""
from __future__ import print_function
from __future__ import absolute_import
import os
import sys
import platform
import tempfile
import logging
import requests
import datetime
import base64
import hmac
import hashlib
import json
import time
from dateutil import parser as dparser
from abc import ABCMeta, abstractmethod
from uuid import getnode as get_mac

try:
    import urllib.parse as parse
except ImportError:
    import urllib as parse

import argparse

from . import player

sys.path.append("..")
from utils import diagnose
from utils import aliadapath
from utils import config

try:
    import gtts
except ImportError:
    pass

try:
    reload  # Python 2
except NameError:  # Python 3
    from importlib import reload

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class AbstractTTSEngine(object):
    """
    Generic parent class for all speakers
    """
    __metaclass__ = ABCMeta

    @classmethod
    def get_config(cls):
        return {}

    @classmethod
    def get_instance(cls):
        param = cls.get_config()
        instance = cls(**param)
        return instance

    @classmethod
    @abstractmethod
    def is_available(cls):
        return diagnose.check_executable('aplay')

    def __init__(self, **kwargs):
        self._logger = logging.getLogger(__name__)

    @abstractmethod
    def say(self, phrase, *args):
        pass

    @staticmethod
    def play(filename):
        """
        The method has deprecated, use 'mic.Mic.play' instead.
        play wave by aplay
        """
        sound = player.get_sound_manager()
        sound.play_block(filename)


class AbstractMp3TTSEngine(AbstractTTSEngine):
    """
    Generic class that implements the 'play' method for mp3 files
    """
    SLUG = ''

    @classmethod
    def is_available(cls):
        return (super(AbstractMp3TTSEngine, cls).is_available() and
                diagnose.check_python_import('mad'))

    @staticmethod
    def play_mp3(filename):
        music = player.get_music_manager()
        music.play_block(filename)

    @staticmethod
    def remove_punctuation(phrase):
        to_remove = [
            ',', '/', ':', '\\', '@', '!', '%', '&', '*', '(',
            ')', '{', '}'
        ]
        for note in to_remove:
            phrase = phrase.replace(note, '')
        return phrase

    def say(self, phrase, cache=False):
        self._logger.debug(u"Saying '%s' with '%s'", phrase, self.SLUG)
        h = hashlib.md5()
        h.update(phrase)
        cache_file_path = os.path.join(
            aliadapath.TEMP_PATH,
            self.SLUG + h.hexdigest() + '.mp3'
        )
        if cache and os.path.exists(cache_file_path):
            self._logger.info(
                "found speech in cache, playing...[%s]" % cache_file_path)
            self.play_mp3(cache_file_path)
        else:
            tmpfile = self.get_speech(phrase)
            if tmpfile is not None:
                self.play_mp3(tmpfile)
                if cache:
                    self._logger.info(
                        "not found speech in cache," +
                        " caching...[%s]" % cache_file_path)
                    os.rename(tmpfile, cache_file_path)
                else:
                    os.remove(tmpfile)

    def get_speech(self, phrase):
        # it needs to be implemented in subclass.
        return None


class BaiduTTS(AbstractMp3TTSEngine):
    """
    使用百度语音合成技术: 要使用本模块, 首先到 yuyin.baidu.com 注册一个开发者账号,
    之后创建一个新应用, 然后在应用管理的"查看key"中获得 API Key 和 Secret Key
    填入 profile.yml 中.
    """

    SLUG = "baidu-tts"

    def __init__(self, api_key, secret_key, per=0):
        super(self.__class__, self).__init__()
        self._logger = logging.getLogger(__name__)
        self.api_key = api_key
        self.secret_key = secret_key
        self.per = per
        self.token = ''

    @classmethod
    def get_config(cls):
        # Try to get baidu_yuyin config from config
        return config.get('baidu_yuyin', {})

    @classmethod
    def is_available(cls):
        return diagnose.check_network_connection()

    def get_token(self):
        cache = open(os.path.join(aliadapath.TEMP_PATH, 'baidustt.ini'), 'a+')
        try:
            pms = cache.readlines()
            if len(pms) > 0:
                start_time = pms[0]
                tk = pms[1]
                # 计算token是否过期 官方说明一个月，这里保守29天
                start_time = dparser.parse(start_time)
                end_time = datetime.datetime.now()
                if (end_time - start_time).days <= 29:
                    return tk
        finally:
            cache.close()
        URL = 'http://openapi.baidu.com/oauth/2.0/token'
        params = parse.urlencode({'grant_type': 'client_credentials',
                                  'client_id': self.api_key,
                                  'client_secret': self.secret_key})
        r = requests.get(URL, params=params)
        try:
            r.raise_for_status()
            token = r.json()['access_token']
            return token
        except requests.exceptions.HTTPError:
            self._logger.critical('Token request failed with response: %r',
                                  r.text,
                                  exc_info=True)
            return ''

    @staticmethod
    def split_sentences(text):
        punctuations = ['.', '。', ';', '；', '\n']
        for punc in punctuations:
            text = text.replace(punc, '@@@')
        return text.split('@@@')

    def get_speech(self, phrase):
        if self.token == '':
            self.token = self.get_token()
        query = {'tex': phrase,
                 'lan': 'zh',
                 'tok': self.token,
                 'ctp': 1,
                 'cuid': str(get_mac())[:32],
                 'per': self.per
                 }
        r = requests.post('http://tsn.baidu.com/text2audio',
                          data=query,
                          headers={'content-type': 'application/json'})
        try:
            r.raise_for_status()
            if r.json()['err_msg'] is not None:
                self._logger.critical('Baidu TTS failed with response: %r',
                                      r.json()['err_msg'],
                                      exc_info=True)
                return None
        except Exception, e:
            self._logger.critical(e)
            pass

        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(r.content)
            tmpfile = f.name
            return tmpfile


class IFlyTekTTS(AbstractMp3TTSEngine):
    """
    使用讯飞的语音合成技术
    要使用本模块, 请先在 profile.yml 中启用本模块并选择合适的发音人.
    """

    SLUG = "iflytek-tts"

    def __init__(self, api_id, api_key, proxy='', voice_name='xiaoyan',
                 speed='50', volume='80', pitch='50'):
        super(self.__class__, self).__init__()
        self._logger = logging.getLogger(__name__)
        self.api_id = api_id
        self.api_key = api_key
        self.proxy = proxy
        self.voice_name = voice_name
        self.speed = str(speed)
        self.volume = str(volume)
        self.pitch = str(pitch)

    @classmethod
    def get_config(cls):
        # Try to get iflytek_yuyin config from config
        param = config.get('/iflytek_yuyin/tts', {})
        if 'api_id' not in param or not param['api_id']:
            param['api_id'] = config.get('/iflytek_yuyin/api_id')
        return param

    @classmethod
    def is_available(cls):
        return diagnose.check_network_connection()

    def get_speech(self, phrase):
        url = 'http://api.xfyun.cn/v1/service/v1/tts'
        param = {
            'auf': 'audio/L16;rate=16000',
            'aue': 'lame',
            'voice_name': self.voice_name,
            'speed': self.speed,
            'volume': self.volume,
            'pitch': self.pitch
        }
        xparam = base64.b64encode(json.dumps(param))
        curTime = str(int(time.time()))
        h = hashlib.md5()
        h.update(self.api_key + curTime + xparam)
        header = {
            'X-Appid': self.api_id,
            'X-CurTime': curTime,
            'X-Param': xparam,
            'X-CheckSum': h.hexdigest(),
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        }
        data = {
            'text': phrase.encode('utf8')
        }
        if self.proxy:
            session = requests.session()
            session.proxies = {
                'http': self.proxy,
                'https': self.proxy
            }
            resp = session.post(url, data=parse.urlencode(data),
                                headers=header, )
        else:
            resp = requests.post(url, data=parse.urlencode(data),
                                 headers=header)
        if resp.headers['Content-Type'] != 'audio/mpeg':
            self._logger.error("get tts by xunfei error, resp:%s", resp.text)
            return None
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(resp.content)
            return f.name


class ALiBaBaTTS(AbstractMp3TTSEngine):
    """
    使用阿里云的语音合成技术: 要使用本模块, 请先在 profile.yml 中启用本模块并选择合适的发音人.
    """

    SLUG = "ali-tts"

    def __init__(self, ak_id, ak_secret, voice_name='xiaoyun'):
        super(self.__class__, self).__init__()
        self._logger = logging.getLogger(__name__)
        self.ak_id = ak_id
        self.ak_secret = ak_secret
        self.voice_name = voice_name

    @classmethod
    def get_config(cls):
        # Try to get ali_yuyin config from config
        return config.get('ali_yuyin', {})

    @classmethod
    def is_available(cls):
        return diagnose.check_network_connection()

    @staticmethod
    def split_sentences(text):
        punctuations = ['.', '。', ';', '；', '\n']
        for punc in punctuations:
            text = text.replace(punc, '@@@')
        return text.split('@@@')

    @staticmethod
    def get_current_date():
        date = datetime.datetime.strftime(datetime.datetime.utcnow(),
                                          "%a, %d %b %Y %H: %M: %S GMT")
        return date

    @staticmethod
    def to_md5_base64(str_body):
        hs = hashlib.md5()
        hs.update(str_body)
        return hs.digest().encode('base64').strip()

    @staticmethod
    def to_sha1_base64(string_to_sign, secret):
        hmacsha1 = hmac.new(str(secret), str(string_to_sign), hashlib.sha1)
        return base64.b64encode(hmacsha1.digest())

    def get_speech(self, phrase):
        options = {
            'url': 'http://nlsapi.aliyun.com/speak?encode_type=' +
                   'mp3&voice_name=' + self.voice_name + '&volume=50',
            'method': 'POST',
            'body': phrase.encode('utf8'),
        }
        headers = {
            'date': self.get_current_date(),
            'content-type': 'text/plain',
            'authorization': '',
            'accept': 'audio/wav, application/json'
        }

        body = ''
        if 'body' in options:
            body = options['body']

        bodymd5 = ''
        if not body == '':
            bodymd5 = self.to_md5_base64(body)

        stringToSign = options['method'] + '\n' + headers['accept'] + '\n' + bodymd5 + '\n' + headers[
            'content-type'] + '\n' + headers['date']
        signature = self.to_sha1_base64(stringToSign, self.ak_secret)
        authHeader = 'Dataplus ' + self.ak_id + ':' + signature
        headers['authorization'] = authHeader
        url = options['url']
        r = requests.post(url, data=body, headers=headers, verify=False)

        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(r.content)
            tmpfile = f.name
            return tmpfile


class GoogleTTS(AbstractMp3TTSEngine):
    """
    Uses the Google TTS online translator: Requires pymad and gTTS to be available
    """

    SLUG = "google-tts"

    def __init__(self, language='en'):
        super(self.__class__, self).__init__()
        self.language = language

    @classmethod
    def is_available(cls):
        return (super(cls, cls).is_available() and
                diagnose.check_python_import('gtts') and
                diagnose.check_network_connection())

    @classmethod
    def get_config(cls):
        # Try to get google_yuyin from config
        return config.get('google_yuyin', {})

    @property
    def languages(self):
        langs = ['af', 'sq', 'ar', 'hy', 'ca', 'zh-CN', 'zh-TW', 'hr', 'cs',
                 'da', 'nl', 'en', 'eo', 'fi', 'fr', 'de', 'el', 'ht', 'hi',
                 'hu', 'is', 'id', 'it', 'ja', 'ko', 'la', 'lv', 'mk', 'no',
                 'pl', 'pt', 'ro', 'ru', 'sr', 'sk', 'es', 'sw', 'sv', 'ta',
                 'th', 'tr', 'vi', 'cy', 'zh-yue']
        return langs

    def get_speech(self, phrase):
        if self.language not in self.languages:
            raise ValueError("Language '%s' not supported by '%s'",
                             self.language, self.SLUG)
        tts = gtts.gTTS(text=phrase, lang=self.language)
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            tmpfile = f.name
        tts.save(tmpfile)
        return tmpfile


def get_default_engine_slug():
    return 'osx-tts' if platform.system().lower() == 'darwin' else 'espeak-tts'


def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses

    return [tts_engine for tts_engine in
            list(get_subclasses(AbstractTTSEngine))
            if hasattr(tts_engine, 'SLUG') and tts_engine.SLUG]


def get_engine_by_slug(slug=None):
    """
    Returns:
        A speaker implementation available on the current platform

    Raises:
        ValueError if no speaker implementation is supported on this platform
    """

    if not slug or type(slug) is not str:
        raise TypeError("Invalid slug '%s'", slug)

    selected_engines = filter(lambda tts_engine: hasattr(tts_engine, "SLUG") and tts_engine.SLUG == slug, get_engines())
    if len(selected_engines) == 0:
        raise ValueError("No TTS engine found for slug '%s'" % slug)
    else:
        if len(selected_engines) > 1:
            print("WARNING: Multiple TTS engines found for slug '%s'. " +
                  "This is most certainly a bug." % slug)
        engine = selected_engines[0]
        if not engine.is_available():
            raise ValueError(("TTS engine '%s' is not available (due to " +
                              "missing dependencies, etc.)") % slug)
        return engine


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Aliada TTS module')
    parser.add_argument('--debug', action='store_true',
                        help='Show debug messages')
    arges = parser.parse_args()

    logging.basicConfig()
    if arges.debug:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

    engines = get_engines()
    available_engines = []
    for eng in get_engines():
        if eng.is_available():
            available_engines.append(eng)
    disabled_engines = list(set(engines).difference(set(available_engines)))
    print("Available TTS engines:")
    for i, eng in enumerate(available_engines, start=1):
        print("%d. %s" % (i, eng.SLUG))

    print("")
    print("Disabled TTS engines:")

    for i, eng in enumerate(disabled_engines, start=1):
        print("%d. %s" % (i, eng.SLUG))

    print("")
    for i, eng in enumerate(available_engines, start=1):
        print("%d. Testing engine '%s'..." % (i, eng.SLUG))
        eng.get_instance().say("This is a test.")
    print("Done.")
