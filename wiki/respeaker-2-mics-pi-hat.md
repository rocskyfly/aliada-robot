# ReSpeaker 2-Mics Pi HAT 配置教程

本教程适用于 [ReSpeaker 2-Mics Pi HAT](http://wiki.seeed.cc/Respeaker_2_Mics_Pi_HAT/) ，使用其他麦克风的朋友请参考其他配置教程。

## 事前准备

如果以前配置过 `.asoundrc` ，需要将之删除：

``` sh
rm /home/pi/.asoundrc
```

## 安装驱动

``` sh
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard 2-mic
sudo ./install.sh
reboot
```

完成后可以使用 `aplay -l` 命令检查一下是否包含 `seeedvoicecard` 的播放设备。

``` sh
pi@raspberrypi:~ $ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: seeedvoicecard [seeed-voicecard], device 0: bcm2835-i2s-wm8960-hifi wm8960-hifi-0 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

## 配置

使用 `alsamixer` 进行调整：

``` sh
alsamixer
```

先重点设置 `Headphone`、`Speaker`、`Playback` 的音量，3D 也可以适当开一些。

![](https://github.com/SeeedDocument/MIC_HATv1.0_for_raspberrypi/blob/master/img/alsamixer.png?raw=true)

之后按 `F4` 键切换到录音设置界面，把 `Capture` 也开大。

完成后可以用如下方法测试下是否 ok ：

``` sh
arecord -d 3 temp.wav  # 测试录音3秒
aplay temp.wav # 播放录音看看效果
```

如果效果理想，此时可以将当前配置保存：

``` sh
sudo alsactl --file=asound.state store
```

为了避免开机音量被重置，可以将 asound.state 文件拷至 /var/lib/alsa 目录下：

``` sh
sudo cp asound.state /var/lib/alsa/
```

如果安装完后 arecord、aplay 不能正常使用，可以编写如下的 `.asoundrc` 文件：

```
pcm.!default {
        type asym
        playback.pcm {
            type plug
            slave.pcm "hw:1,0"
        }
        capture.pcm {
            type plug
            slave.pcm "hw:1,0"
        }
}

ctl.!default {
        type hw
        card 0
}
```


## 其他技巧

1. 如果希望利用开发板上的按钮来实现开关麦克风，可以使用 [ReSpeaker-Switcher](https://github.com/wzpan/ReSpeaker-Switcher)。
