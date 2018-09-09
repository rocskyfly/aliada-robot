# 常见问题自助

* [信心问题](#信心问题)
* [启动报错](#启动报错)
* [更新报错](#更新报错)
* [账户密码](#账户密码)
* [使用问题](#使用问题)

## 信心问题

* 搭建叮当需要准备哪些东西？

1. 硬件方面，参考 [硬件选购建议](https://github.com/wzpan/dingdang-robot/wiki/hardware-choices) 。
2. 技能方面，建议具备基本的 Linux 使用能力。如果你连 ssh 都不会，那使用叮当会比较吃力。如果你想看懂代码，写插件，参与贡献，建议具备 Python 的开发能力。
3. 一颗认真而执着的心。

* 我零基础的啊，能够自己搭建叮当吗？

有没有基础不重要，关键是要认真、耐心。认真阅读文档，耐心照着步骤一步一步来。遇到问题，先求助下 Google 老师或百度老师，实在不明白再向其他人求助。零基础完成了搭建的用户有很多，他们都具备这两个优秀品质。

基础薄弱的朋友建议不要自己尝试手动安装，而应该选择镜像安装。节省自己时间，也节省其他人帮你解决问题的时间。

* 能手把手教我怎么安装吗？

不能。作者比牛仔还忙，不能保证很快响应你的问题。

镜像安装遇到问题，请先看文档，再到 [论坛](http://bbs.hahack.com) 和 [issue](http://github.com/wzpan/dingdang-robot/issues) 上找是否有类似问题，如果没有找到，再到群里提问。

手动安装遇到问题，同样按照上述思路先找答案，也可以观看[手动安装视频(密码：dingdang123)](http://v.youku.com/v_show/id_XMzA5NjY1OTU0MA==.html?spm=a2h3j.8428770.3416059.1)检视下自己漏了什么。

* 能跟我解释下整个工程的代码吗？

你既然都关心起代码实现了，自行阅读也不困难啊。如果你写了源码分析，欢迎发到论坛分享给其他人。

* 我不懂 Python 啊，怎么才能看懂并修改你的代码？

学习 Python 。

## 启动报错

* 启动后报错：

```
Traceback (most recent call last):
  File "dingdang/dingdang.py", line 191, in <module>
    app.run()
  File "dingdang/dingdang.py", line 157, in run
    conversation.handleForever()
  File "/home/pi/dingdang/client/conversation.py", line 65, in handleForever
    threshold, transcribed = self.mic.passiveListen(self.persona)
  File "/home/pi/dingdang/client/mic.py", line 143, in passiveListen
    frames_per_buffer=CHUNK)
  File "/usr/lib/python2.7/dist-packages/pyaudio.py", line 747, in open
    stream = Stream(self, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/pyaudio.py", line 442, in __init__
    self._stream = pa.open(**arguments)
IOError: [Errno Invalid input device (no default output device)] -9996
```

答：同时打开了多个叮当，而声卡已被之前的叮当进程占用导致。把叮当进程都结束了，再重新启动叮当即可。

* 启动后报如下错误：![](http://onmw7y6f4.bkt.clouddn.com/vocabularies.png)

答：请确保 [vocabularies.zip 已下载并解压到正确位置](https://github.com/wzpan/dingdang-robot/wiki/install#%E5%AE%89%E8%A3%85-phonetisaurus-m2m-aligner-%E4%BB%A5%E5%8F%8A-mitlm)。

* 启动后报这个错误是什么原因？

```
Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
```

答：PyAudio 的提醒信息。不影响工作，不用管。

* 启动后报这个错误是什么原因？

```
Traceback (most recent call last):
  File "dingdang.py", line 11, in <module>
    from client import tts
  File "/home/pi/dingdang/client/tts.py", line 25, in <module>
    import diagnose
  File "/home/pi/dingdang/client/diagnose.py", line 9, in <module>
    import pip.req
  File "/usr/lib/python2.7/dist-packages/pip/__init__.py", line 74, in <module>
    from pip.vcs import git, mercurial, subversion, bazaar  # noqa
  File "/usr/lib/python2.7/dist-packages/pip/vcs/mercurial.py", line 9, in <module>
    from pip.download import path_to_url
  File "/usr/lib/python2.7/dist-packages/pip/download.py", line 25, in <module>
    from requests.compat import IncompleteRead
ImportError: cannot import name IncompleteRead
```

答：新版本的dingdang-robot已取消使用 pip.req 。请先确保已切换到 dingdang-robot/dingdang-robot 仓库。

``` sh
cd $HOME/dingdang
git remote -v
```

如果结果是：

```
origin	https://github.com/wzpan/dingdang-robot.git (fetch)
origin	https://github.com/wzpan/dingdang-robot.git (push)
```

则需要切仓库。最直接的切换方法就是删除原有工程重拉：

``` sh
cd $HOME
rm -rf dingdang
git clone https://github.com/dingdang-robot/dingdang-robot.git dingdang
```

* 启动后报如下错误：


``` sh
Traceback (most recent call last):
  File "dingdang.py", line 178, in <module>
    app.run()
  File "dingdang.py", line 124, in run
    self.mic.say(salutation, cache=True)
  File "/home/pi/dingdang/client/mic.py", line 335, in say
    self.speaker.say(phrase, cache)
  File "/home/pi/dingdang/client/tts.py", line 133, in say
    tmpfile = self.get_speech(phrase)
  File "/home/pi/dingdang/client/tts.py", line 313, in get_speech
    result_info = requests.post(getinfo_url, data=data).json()
  File "/usr/local/lib/python2.7/dist-packages/requests/models.py", line 892, in json
    return complexjson.loads(self.text, **kwargs)
  File "/usr/lib/python2.7/dist-packages/simplejson/__init__.py", line 516, in loads
    return _default_decoder.decode(s)
  File "/usr/lib/python2.7/dist-packages/simplejson/decoder.py", line 374, in decode
    obj, end = self.raw_decode(s)
  File "/usr/lib/python2.7/dist-packages/simplejson/decoder.py", line 404, in raw_decode
    return self.scan_once(s, idx=_w(s, idx).end())
simplejson.scanner.JSONDecodeError: Expecting value: line 2 column 1 (char 2)
```

新版本的科大讯飞TTS需要额外进行一些配置。见如下 `tts:` 之后的字段：

``` yaml
# 讯飞语音服务
# api_id 及 api_key 需前往
# http://aiui.xfyun.cn/webApi
# 注册获取（注意创建的是WebAPI应用），仅使用语音合成无需注册
# 然后将主板的ip地址添加进ip白名单（建议使用中转服务器的ip地址 101.132.139.80）
iflytek_yuyin:
    api_id: '填写你的讯飞应用的Api ID'
    api_key: '填写你的讯飞应用的Api Key'  # 没看到这个说明不是注册的WebAPI应用，请改注册个WebAPI应用
    vid: '67100' #语音合成选项： 60120为小桃丸 67100为颖儿 60170为萌小新 更多音色见wiki
    url: 'http://api.musiiot.top/stt.php' # 白名单ip中转服务器（可选）
    tts:
        api_id: '***' # 这项不填可以使用上层配置
        api_key: '**********************'
        voice_name: xiaoyan
        proxy: 'http://123.207.49.217:8028' 
```

如果觉得麻烦，可以改用百度或者阿里的TTS。

* 启动后报如下错误：

![](http://7xj89i.com1.z0.glb.clouddn.com/problem-log.png)

这个问题可能是由于在 root 账号里使用过 dingdang 导致普通用户无法正常读写 log 文件。解决办法是删掉重建：

``` sh
rm -rf $HOME/dingdang/temp
mkdir $HOME/dingdang/temp
touch $HOME/dingdang/temp/dingdang.log
```

* 启动后报如下错误：

```
ERROR:apscheduler.executors.default:Job "Notifier.gather (trigger: interval[0:00:30], next run at: 2017-08-09 22:38:45 HKT)" raised an exception
Traceback (most recent call last):
  File "/usr/local/lib/python2.7/dist-packages/apscheduler/executors/base.py", line 108, in run_job
    retval = job.func(*job.args, **job.kwargs)
  File "/home/pi/dingdang/client/notifier.py", line 41, in gather
    [client.run() for client in self.notifiers]
  File "/home/pi/dingdang/client/notifier.py", line 18, in run
    self.timestamp = self.gather(self.timestamp)
  File "/home/pi/dingdang/client/notifier.py", line 45, in handleEmailNotifications
    emails = Email.fetchUnreadEmails(self.profile, since=lastDate)
  File "/home/pi/dingdang/client/plugins/Email.py", line 145, in fetchUnreadEmails
    (retcode, messages) = conn.search(None, '(UNSEEN)')
  File "/usr/lib/python2.7/imaplib.py", line 639, in search
    typ, dat = self._simple_command(name, *criteria)
  File "/usr/lib/python2.7/imaplib.py", line 1087, in _simple_command
    return self._command_complete(name, self._command(name, *args))
  File "/usr/lib/python2.7/imaplib.py", line 837, in _command
    ', '.join(Commands[name])))
error: command SEARCH illegal in state AUTH, only allowed in states SELECTED
```

答：邮箱没有配置好。注意如下几个要求：

1. 不要使用QQ邮箱，不要使用网易手机邮箱；
2. 如果使用网易邮箱，密码应该是客户端授权码；
3. 如果使用网易邮箱，还需开启未认证客户端的使用权限。

请详细参考 [配置](https://github.com/wzpan/dingdang-robot/wiki/configuration#%E7%BD%91%E6%98%93%E9%82%AE%E7%AE%B1%E8%AF%B4%E6%98%8E) 一节配置好邮箱。

* 启动后报下面这样的错误：![](http://onmw7y6f4.bkt.clouddn.com/6B78F63BD70AAE479C11EDCEADA45306.jpg)

答：/home/pi/.dingdang/profile.yml 格式错误。请检查你的内容是不是破坏了YAML格式要求。

* 启动后报如下错误：

```
Traceback (most recent call last):
File "dingdang.py", line 16, in 
from client.conversation import Conversation
File "/home/kevin/dingdang/client/conversation.py", line 6, in 
from drivers.pixels import pixels
File "/home/kevin/dingdang/client/drivers/pixels.py", line 124, in 
pixels = Pixels()
File "/home/kevin/dingdang/client/drivers/pixels.py", line 21, in init
self.dev = apa102.APA102(num_led=self.PIXELS_N)
File "/home/kevin/dingdang/client/drivers/apa102.py", line 90, in init
self.spi.open(bus, device) # Open SPI port 0, slave device (CS) 1
IOError: [Errno 2] No such file or directory
```

答：`raspi-config` 进入树莓派设置，然后进入 `Interfacing Options` ，开启 SPI ，以支持控制 LED 灯。

## 更新报错

`git pull` 更新的时候提示类似如下错误：

```
error： Your local changes to the following files would be overwritten by merge:
    XXXX.py
Please, commit your changes or stash them before you can merge.
Aborting
```

出这个问题的原因是你已经修改了叮当工程中的文件，而在你提交或者回滚这些改动前，git 不允许你直接更新代码，否则可能会导致冲突。

首先应该先检查下你做了什么东西：

``` sh
git diff
```

如果没有什么重要改动，可以先回滚一下：

``` sh
git reset --hard HEAD
```

如果改动很重要，希望保留，可以提交它：

``` sh
git add XXX.py # 你改动的文件
git commit
```

然后就可以试试 `git pull` 了。如果遇到冲突，可以参考 [这篇教程](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/001375840202368c74be33fbd884e71b570f2cc3c0d1dcf000) 解决下冲突。

## 账户密码

* 叮当镜像的账户和密码是什么？

答：默认的账户和密码和 Raspbian 系统相同。账户名为 pi，密码为 raspberry。

## 使用问题

* 关了终端后叮当就不工作了，怎么办？

答：应该使用 tmux 或 screen 或 nohup 等终端复用工具来挂机。

* 开启微信接入功能后，Ctrl-C 关闭不了叮当，怎么办？

答：Ctrl-C 关闭不了是微信接入模块 wxbot 的问题。解决办法是 Ctrl-Z 退出当前会话，然后执行如下命令：

``` sh
ps auwx | grep dingdang  # 查看dingdang的PID号
kill -9 PID号
```

* 和叮当交互时报如下错误：

```
CRITICAL:client.tts:Baidu TTS failed with response: u'authentication failed'.
```

答：请确保您已创建了百度语音的应用，并申请了语音识别和语音合成两个功能（两个都要！），并且准确填写了 API Key 和 API Secret 。

* 微信登录成功了，但发出的指令没有任何响应。

答：发给微信里自己的微信账号，而不是发给文件传输助手。比如，你的微信昵称如果是“赵日天”，那么就找到“赵日天”这个微信号，进去发信息。

* OpenFST 编译好久啊。

答：耐心等待。

* 叮当总是过快结束主动聆听。

答：首先尝试更新到最新版本的 dingdang 。如果问题依然存在，看看是否有报如下错误：

``` 
ERROR:client.mic:read() got an unexpected keyword argument 'exception_on_overflow'
ERROR:client.mic:read() got an unexpected keyword argument 'exception_on_overflow'
ERROR:client.mic:read() got an unexpected keyword argument 'exception_on_overflow'
ERROR:client.mic:read() got an unexpected keyword argument 'exception_on_overflow'
```

如果有这种错误，那么请去掉 [dingdang/client/mic.py 中第 295 行](https://github.com/wzpan/dingdang-robot/blob/master/client/mic.py#L295) 附近的 `, exception_on_overflow=False` 变量设置：

``` py
data = stream.read(CHUNK, exception_on_overflow=False)
```

改成：

``` py
data = stream.read(CHUNK)
```

这个问题是因为老版本的 PyAudio 并没有 exception_on_overflow 参数导致。

如果没有解决问题，试试将 [dingdang/client/mic.py 第272行](https://github.com/wzpan/dingdang-robot/blob/master/client/mic.py#L272) 附近的 CHUNK 的值设大一点，例如 4096 ，看看能否解决问题。

当使用较差的麦克风时，麦克风听到的声音小，容易判断为没说话而过快结束聆听。可以试试将 [dingdang/client/mic.py](https://github.com/wzpan/dingdang-robot/blob/master/client/mic.py#L305) 里的 0.8 这个值设置改小一些，使结束聆听的条件变得更苛刻一点，从而延长聆听时间。如果没有这个问题，则不建议修改本值，以避免说完话后还要等一段时间才能结束聆听。

如果换了各种值都还不行，说明麦克风质量太差。建议更换为阵列麦克风。

* 叮当结束主动聆听很慢。

可以试试将 [dingdang/client/mic.py](https://github.com/wzpan/dingdang-robot/blob/master/client/mic.py#L305) 里的 0.8 这个值设置改大一些，使结束聆听的条件变得更容易一点，从而缩短聆听时间。

* 叮当的唤醒词误判率很高。

答：使用长一点的唤醒词可以减少误判。例如，我亲测 PocketSphinx + 唤醒词 “HEYDINGDANG” 的误判率就比较低。另外，如果使用 ReSpeaker 2-Mics Pi HAT开发板，可以利用开发板上的开关，在不需要交互时临时禁用麦克风。方法见 [ReSpeaker-Switcher](https://github.com/wzpan/ReSpeaker-Switcher)。

* PocketSphinx 和 snowboy 该选哪个？

PocketSphinx 是基于统计模型生成唤醒词的language model的。lmtool 已经预先训练好了这个统计模型，可以将任一给出的单词得到 languamodel 。好处是不用训练，坏处是对中文支持不好，因为预训练的模型是针对英文的。对于很多中文单词，如果发音习惯和英文不同，则识别效果会大打折扣。例如 “小白”（xiaobai），得到的 language model 的英文发音其实是 "交贝"（ZIAO BAY） 。也有些词，例如 “叮当” ，得到的 language model 的英文发音 （DING DUNG） 中英文类似，识别效果也比较不错，这也是取名叮当的重要原因; 

snowboy 则是基于平均语音模型来做识别的，越多人训练同个唤醒词，识别效果越好，误识别率越低。优点是语言无关。缺点是唤醒词需要多一点人贡献语音，才会得到比较平均的声学模型。否则识别的准确率和误识别率都会比较不理想。

综上所述，个人建议：

1. 如果你想的唤醒词中英文发音都相似，那么推荐使用 PocketSphinx ；
2. 如果唤醒次中英文发音差别较大，则建议使用 snowboy ，同时建议尽可能让多一点人贡献声音，参与训练。