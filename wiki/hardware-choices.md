# 硬件选购建议

* [主板](#主板)
* [麦克风](#麦克风)
* [音箱](#音箱)
* [蓝牙耳机](#蓝牙耳机)
* [内存卡](#内存卡)

> 温馨提示：以下的选购建议仅供参考，如对使用效果不满意，本人不承担任何责任。

## 主板

* 树莓派 Raspberry Pi 3

理论上，叮当可以在任何 Linux 系统上执行。如果不想整天开着电脑挂叮当，选购一个低功耗的主板是更好的选择。推荐选择 Raspberry Pi 3 的理由是足够流行和简单，另外可以直接刷叮当的镜像，省去手动安装叮当的麻烦。

另外，不推荐  Pi Zero 系列，性能不如 Pi 3，加上黄牛炒作，算上 HDMI 转接头和 Micro-USB HUB 的价格可能比 Pi 3 还高。

## 麦克风

相比普通麦克风，麦克风阵列的拾音范围更大，允许隔着叮当一段距离依然可以唤醒和交流。因此推荐选购麦克风阵列。而阵列的数量越多，效果会越好，价格也会越高。因此，您可以依据自己的经济能力选择不同阵列数量的麦克风。


### 二阵列

* [ReSpeaker 2 Mics Pi HAT](http://wiki.seeed.cc/Respeaker_2_Mics_Pi_HAT/) - 专门为树莓派打造的 2 阵列开发板，带 2 Mic 阵列，有声卡，支持外接 3.5mm 音频输出。
* [Amazon AVS DS20921](http://conexant.com/amazon-avs/)

### 四阵列

* PS3 Eye - PS3 淘汰的配件，包含四阵列麦克风和摄像头，免驱使用。由于是淘汰下来的配件，价格也比较便宜，可以到淘宝上找找。
* [ReSpeaker 4-Mics Pi HAT](https://github.com/SeeedDocument/ReSpeaker-4-Mics-Pi-HAT/blob/master/4mics_hat.md)
* [Amazon AVS DS20924](http://conexant.com/amazon-avs/)

### 七阵列

* [ReSpeaker Mic Array](https://www.seeedstudio.com/ReSpeaker-Mic-Array-Far-field-w%2F-7-PDM-Microphones-p-2719.html)

## 音箱

音箱的选购比较随意，如果使用树莓派，市面上大部分 3.5mm 音频输出的音箱都能和树莓派搭配工作。而不同价格的音箱，音质也有所不同，因此您可以根据自己的经济能力选购合适的音箱。

比较推荐独立供电的音箱，因为不会有较大电流声。

如果选购的是 USB 音箱，那么建议不要直接把 USB 插入到树莓派上供电，否则会有比较大的电流声干扰，影响音质。可以插到一个单独的 USB 插头上。

不建议使用蓝牙音箱，因为配置比较麻烦。如果依然希望使用蓝牙音箱，建议升级一下 pulseaudio 。参见 <http://youness.net/raspberry-pi/bluetooth-headset-raspberry-pi-3-ad2p-hsp>

关于音箱的接入还有一个建议：和麦克风尽量隔开距离，以免播放音乐的时候误唤醒麦克风。

## 蓝牙耳机

除了麦克风+音箱的外设方案，还可以考虑使用蓝牙耳机。好处是交互范围取决于蓝牙耳机的范围，缺点是配置比较麻烦。

这里提供一篇设置蓝牙耳机的参考教程：<http://youness.net/raspberry-pi/bluetooth-headset-raspberry-pi-3-ad2p-hsp>

## 内存卡

树莓派需使用 Micro-SD 内存卡来刷入系统，而阿里阿达的镜像的解压后大小一般超过 8G ，因此建议选购 16G ，class 10 以上的内存卡（class 太低会影响系统性能）。
