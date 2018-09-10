# 配置

## Table of Contents

* [配置文件](#配置文件)
* [配置USB麦克风](#配置usb麦克风)
* [修改唤醒词](#修改唤醒词)
* [优化百度语音识别准确度](#优化百度语音识别准确度)
* [讯飞语音合成音色修改](#讯飞语音合成音色修改)
* [网易邮箱说明](#网易邮箱说明)
* [设置开机启动](#设置开机启动)
* [设置摄像头](#设置摄像头)
* [其他常见问题](#其他常见问题)

## 配置文件

配置文件位于 /home/robot/aliada-robot/.aliada/profile.yml 下（注意是加了点的 .aliada ）。每次修改，需重启阿里阿达生效。

> 注意注意注意注意：如果使用网易邮箱，注意阅读 [网易邮箱说明](#网易邮箱说明) 。另外不建议使用 QQ 邮箱。

``` yml
robot_name: 'ALIADA'  # 必须使用大写
robot_name_cn: '阿里阿达'
first_name: '主人'
last_name: 'Qi'
timezone: CST
location: '上海'

# 是否接入微信
wechat: true

# 当微信发送语音时，是直接播放语音还是执行语音命令？
# true：直接播放
# false：执行语音命令（只支持百度STT，其他两种STT识别不准）
wechat_echo: false

# 除了自己之外，还能响应 echo 指令的好友微信名单
# 如果填写 ['ALL'] 表示响应所有微信好友
# 如果填写 [] 表示不响应任何好友
wechat_echo_text_friends: ['小Q', 'HaHack']

# 除了自己之外，还能直接播放语音的好友微信名单
# 如果填写 ['ALL'] 表示播放所有微信好友的语音
# 如果填写 [] 表示不播放任何好友的语音
wechat_echo_voice_friends: ['小Q']

# 当有邮件时，是否朗读邮件标题
read_email_title: true

# 当内容过长（> 200个字）时，是否继续朗读
# true：读
# false：改为发送内容
read_long_content: false

# 最长朗读内容（仅当 read_long_content 为 false 时有效）
max_length: 200

# 是否使用邮箱发送长内容而不是微信
prefers_email: false

# 勿扰模式，该时间段内不执行通知检查
do_not_bother:
    enable: true # 开启勿扰模式
    since: 23    # 开始时间
    till: 9      # 结束时间，如果比 since 小表示第二天

# wav声音播放配置
# 可选值：
# aplay         - 子进程aplay播放
# pyaudio       - pyaudio模块播放
sound_engine: pyaudio

# mp3文件播放配置
# 可选值：
# play          - 子进程play播放
# pygame        - pygame库播放(树莓派python默认自带，推荐配置)
# vlc           - vlc库播放(短音频可能播放有问题)
music_engine: pygame

# 语音合成服务配置
# 可选值：
# baidu-tts     - 百度语音识别
# iflytek-tts   - 讯飞语音合成
# ali-tts       - 阿里语音合成
# google-tts    - 谷歌语音合成
tts_engine: ali-tts

# STT 服务配置
# 可选值：
# sphinx        - pocketsphinx离线识别引擎（需训练，参考修改唤醒词教程）
# baidu-stt     - 百度在线语音识别
# iflytek-stt   - 讯飞语音识别
# ali-stt       - 阿里语音识别
# google-stt    - 谷歌语音合成
stt_engine: ali-stt

# 离线唤醒 SST 引擎
# 可选值：
# sphinx        - pocketspinx离线唤醒                                                                                                                                           
# snowboy-stt   - snowboy离线唤醒
stt_passive_engine: sphinx

# pocketsphinx 唤醒SST引擎（默认）
pocketsphinx:
    fst_model: '/home/pi/g014b2b/g014b2b.fst'
    hmm_dir: '/usr/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k'

# snowboy 唤醒SST引擎（可选）
# https://snowboy.kitt.ai/dashboard
snowboy:
    model: '/home/robot/aliada-robot/aliada/client/snowboy/aliada.pmdl'  # 唤醒词模型
    sensitivity: "0.5"  # 敏感度

# 百度语音服务
# http://yuyin.baidu.com/
baidu_yuyin:
    api_key: '填写你的百度应用的API Key'
    secret_key: '填写你的百度应用的Secret Key'
    per: 0  # 发音人选择 0：女生；1：男生；3：度逍遥；4：度丫丫

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

# 阿里云语音
# ak_id及ak_secret需前往
# https://data.aliyun.com/product/nls
# 注册获取
ali_yuyin:
    ak_id: '填写你的阿里云应用的AcessKey ID'
    ak_secret: '填写你的阿里云应用的AcessKey Secret'
    voice_name: 'xiaoyun' #xiaoyun为女生，xiaogang为男生

# 谷歌语音
# api_key 的获取方式：
# 1. Join the Chromium Dev group:
#     https://groups.google.com/a/chromium.org/forum/?fromgroups#!forum/chromium-dev
# 2. Create a project through the Google Developers console:
#     https://console.developers.google.com/project
# 3. Select your project. In the sidebar, navigate to "APIs & Auth." Activate
#     the Speech API.
# 4. Under "APIs & Auth," navigate to "Credentials." Create a new key for
#     public API access.
google_yuyin:
    language: 'zh-CN'
    api_key: ''

# 聊天机器人
# 可选值：
# tuling    - 图灵机器人
# emotibot  - 小影机器人
robot: tuling

# 图灵机器人
# http://www.tuling123.com
tuling:
    tuling_key: '填写你的图灵机器人API Key'

# 小影机器人
# http://botfactory.emotibot.com/
emotibot:
    appid: '填写你的 emotibot appid'
    active_mode: true  # 是否主动说更多点话

# 信号灯(可选)
# 将普通led接入树莓派GPIO， 唤醒后常亮，思考及说话时闪亮
signal_led:
    enable: false
    gpio_mode: "bcm" # "bcm" 或 "board"
    pin: 24 # led 正极接脚， 负极接GND

# 邮箱
# 如果使用网易邮箱，还需设置允许第三方客户端收发邮件
email:
    enable: true
    address: '你的邮箱地址'
    password: '你的邮箱密码'  # 如果是网易邮箱，须填写应用授权密码而不是登录密码！
    smtp_server: 'smtp.163.com'
    smtp_port: '25'  # 这里填写非SSL协议端口号
    imap_server: 'imap.163.com'
    imap_port: '143'  # 这里填写非SSL协议端口号


# 拍照
# 需接入摄像头才能使用
camera:
    enable: false
    dest_path: "/home/pi/camera" # 保存目录
    quality: 5            # 成像质量（0~100）
    vertical_flip: true     # 竖直翻转
    horizontal_flip: false  # 水平翻转
    count_down: 3           # 倒计时（秒），仅当开启倒计时时有效
    sendToUser: true        # 拍完照是否发送到邮箱/微信    
    sound: true             # 是否有拍照音效
    usb_camera: false       # 是否使用USB摄像头（默认是树莓派5MP摄像头）


#######################
# 插件配置
#######################

## 配置USB麦克风

> 坚持住！配置麦克风和音响是新用户使用阿里阿达过程中最容易卡住的环节。只要完成这一步，后面就没什么难题啦。

> 如果您使用的是 ReSpeaker 2 Mic HAT，则请参见 [ReSpeaker 2-Mics Pi HAT 配置教程](respeaker-2-mics-pi-hat)，无需阅读本节设置。

建议通过 .asoundrc 文件来配置麦克风和音响。

首先确保已接好麦克风和音响。

### 获得声卡编号和设备编号

之后查看当前已接入的所有录音设备：

``` sh
arecord -l
```

得到的结果类似这样：

```
pi@raspberrypi:~$ arecord -l
**** List of CAPTURE Hardware Devices ****
card 1: Set [C-Media USB Headphone Set], device 0: USB Audio [USB Audio]
  Subdevices: 0/1
  Subdevice #0: subdevice #0
card 2: Device [USB PnP Sound Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

上面的结果说明当前接入了两个录音设备，选择你要使用的录音设备，并记下声卡编号（或名字）和设备编号。例如，我希望使用 USB PnP Sound Device 这个设备，则声卡编号为 2 （声卡名为 `Device`），设备编号为 0 。

类似的方法获取音响的声卡编号和设备编号：

``` sh
aplay -l
```

结果类似这样：

```
pi@raspberrypi:~$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: ALSA [bcm2835 ALSA], device 0: bcm2835 ALSA [bcm2835 ALSA]
  Subdevices: 8/8
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
  Subdevice #4: subdevice #4
  Subdevice #5: subdevice #5
  Subdevice #6: subdevice #6
  Subdevice #7: subdevice #7
card 0: ALSA [bcm2835 ALSA], device 1: bcm2835 ALSA [bcm2835 IEC958/HDMI]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: Set [C-Media USB Headphone Set], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 2: Device [USB PnP Sound Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

上面的结果说明当前接入了三个播放设备，其中 card 0 是树莓派自带的声卡，如果您是使用 AUX 3.5 口外接的音响/或耳机，那么应该使用 card 0；card 1 和 card 2 则是其他的设备。记下您要使用的声卡编号和设备编号。

### 配置 .asoundrc

首先创建 /home/pi/.asoundrc ：

``` sh
touch /home/pi/.asoundrc
```

之后添加您选择的声卡编号和设备。这里举两种常见的配置。

- 第一种：您使用的是一个自带音响和录音的组合设备（例如会议麦克风喇叭，或者一块连接了麦克风和音响的独立USB声卡），那么只需设置 pcm 为该组合设备的编号即可。示例：

```
pcm.!default {
        type plug slave {
                pcm "hw:1,0"
        }
}

ctl.!default {
        type hw
        card 1
}
```

上面的 `hw:1,0` 表示使用 card 1，设备 0。即 C-Media USB Headphone Set 。如果配成 `hw:Set,0` ，效果相同（个人更推荐使用声卡名字）。

- 第二种：您使用的是一个单独的 USB 麦克风，并直接通过树莓派的 AUX 3.5 口外接一个音响。那么可以参考如下配置：

```
pcm.!default {
        type asym
            playback.pcm {
                type plug
                slave.pcm "hw:0,0"
            }
            capture.pcm {
                type plug
                slave.pcm "hw:2,0"
            }        
}

ctl.!default {
        type hw
        card 2
}
```

由于播放设备（playback）和录音设备（capture）是独立的，所以需要各自配置。

完成后可以测试下命令行录音和播放，看看是否能正常工作。

录音：

``` sh
arecord -d 3 temp.wav
```

回放录音：

``` sh
aplay temp.wav
```

如果还有问题，可以参见 [Unable to set default input and output audio device on Raspberry jessie](https://raspberrypi.stackexchange.com/questions/39928/unable-to-set-default-input-and-output-audio-device-on-raspberry-jessie)

## 修改唤醒词

> 在确认Aliada完全工作之前，建议不要急着修改唤醒词。等完全可用了再尝试修改唤醒词。

阿里阿达默认的唤醒词是“阿里阿达”，如果需要换成其他唤醒词，根据你选用的 STT 引擎，有不同的方法。

### 如果使用的是 PocketSphinx

* 在 profile.yml 配置文件中修改 `robot_name` 和 `robot_name_cn` 配置项；
* 编写一个 keyword.txt 文件，包含至少两个名字的全拼：

```
DINGDANG
ROBOT
```

其中 `ROBOT` 替换为你需要的机器人名字的全拼。

* 到 [lmtool](http://www.speech.cs.cmu.edu/tools/lmtool-new.html) 里上传你刚刚创建的 keyword.txt 并编译成模型。
* 把得到的 `.dic` 文件和 `.lm` 文件分别重命名为 `dictionary` 和 `languagemodel`，替换 /home/robot/aliada-robot/.aliada/vocabularies/pocketsphinx-vocabulary/keyword 下的同名文件。
* 重新运行 Aliada ，看看新的唤醒词灵敏度如何。如果不理想，换成别的唤醒词。

### 如果使用的是 snowboy

* 到 https://snowboy.kitt.ai/ ，训练你自己的模型；
* 下载模型并上传到树莓派中，存放的路径可以随意，比如 /home/.aliada/snowboy/my-model.pmdl ；
* 修改 profile.yml 中 `snowboy` 的 `model` 的路径为你训练好的模型的路径。

要注意的是，snowboy 的唤醒词最好选择更多人贡献的语音，这样可以得到更为平均的唤醒模型。成熟的商业音箱的唤醒，是针对某个唤醒词，同样的麦克风环境，录入成百上千个语料，进行训练的结果。所以效果会好很多。如果只用自己录制的几个样本作为训练样本，识别率和唤醒率都不会很理想。

## 优化百度语音识别准确度

可以将常用的指令写成一个 command.txt 文件，然后登录您的百度语音应用管理页面，在 【自定义设置】 的 【语音识别词库设置】 项目中，点击
 【进行设置】 按钮，上传该指令文件即可。文件内容示例：

```
音乐
下一首歌
下首歌
切歌
上一首歌
上首歌
停止
停止播放
暂停
暂停播放
重新播放
随机播放
单曲循环
大声
小声
大点声
小点声
大声点
小声点
歌单
榜单
几点
时间
邮件
邮箱
绕口令
笑话
搜索
别听我的
听我的
```

有用户反映换成自己的百度语音识别 API Key 和 API Secret 后，即使上传了 command.txt ，识别效果好像依然不如镜像自带的 API Key 和 API Secret 的效果。我不是百度语音的开发者，但大致猜测这个 command.txt 主要是取到提高被识别的权重的作用，当你坚持使用上一段时间，效果应该会逐步提升。

## 讯飞语音合成音色修改

将 `iflytek_yuyin` 里的 `vid` 编号替换成下文所附编号可更换发音人

建议先去配音配音阁 <http://www.peiyinge.com/anchor?speakerType=1> 测试后再进行更换

附文：

```
中文主播
65070 //小俊
65090 //彬哥
65080 //程程
65320 //小薛
65040 //小英
65010 //小洋
65110 //小光
65340 //小南
64010 //坤叔
65360 //瑶瑶
15675 //小宇
60100 //小媛
62020 //小芳
62060 //百合仙子
65310 //飞飞
62070 //韦香主
60150 //老马
65250 //大灰狼
62010 //小华
65270 //原野

特色语音合成
67230 //葛二爷
60170 //萌小新
60120 //小桃丸
67100 //颖儿

方言主播
68060 //小蓉
10003 //小梅
68030 //小坤
68010 //小强
68040 //晓倩
68120 //玉儿
68080 //小莹

英文主播
69055 //Mr.奥
69020 //凯瑟琳
69010 //John
69030 //Steve

童声主播
60130 //楠楠
```

## 网易邮箱说明

如果使用网易邮箱服务，需要访问如下页面，允许使用第三方客户端收发邮件：

http://config.mail.163.com/settings/imap/index.jsp?uid=您的邮箱地址

注意把链接中 `您的邮箱地址` 改为您真实的网易邮箱地址（带邮箱后缀）。

## 设置开机启动

如果希望开机启动阿里阿达，可以参考 [小技巧：设置开机启动](http://bbs.hahack.com/t/topic/43)。

启动后如需登录微信，可以使用SendQR插件，叫阿里阿达“发送微信二维码”，将发送二维码图片到您邮箱用，再拿手机扫码。也可以使用webserver插件，叫阿里阿达 “启动Web服务器”，然后访问 http://阿里阿达的ip:8080， 里头找到 wxqr.png ，再拿手机扫码。

## 设置摄像头

阿里阿达支持使用树莓派的 5MP 摄像头（CSI接口）或者普通 USB 摄像头（USB接口）进行拍照。

其中，5MP 摄像头是 Raspbian 系统自带支持的。设置方法可参考[这篇文章](http://shumeipai.nxez.com/2013/10/07/raspberry-pi-to-install-the-camera-module.html)。

对于普通 USB 摄像头，首先需要安装一个 fswebcam 拍摄软件：

``` sh
sudo apt-get install fswebcam
```

然后在 ~/.aliada/profile.yml 中将 `camera` 里的 `usb_camera` 选项打开：

``` yml
camera:
    ...
    usb_camera: true
```

## 其他常见问题

请参见 [常见问题自助](https://github.com/wzpan/aliada-robot/wiki/troubleshooting)
