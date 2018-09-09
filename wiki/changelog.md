# ChangeLog

本镜像适用于树莓派系列的主板。其他主机请参考 [手动安装教程](https://github.com/wzpan/dingdang-robot/wiki/install#%E6%89%8B%E5%8A%A8%E5%AE%89%E8%A3%85)。

为了节省您的下载时间，镜像一律使用最高等级的压缩率压缩。解压需耗时约 5 分钟。请下载完后先验证 MD5 值是否正确，然后耐心等待压缩完成。

镜像安装方法请参见：[镜像安装](https://github.com/wzpan/dingdang-robot/wiki/install#%E9%95%9C%E5%83%8F%E5%AE%89%E8%A3%85)

树莓派 pi 账号的密码默认是 raspberry 。

镜像安装完成后，务必遵循 [安装后续](https://github.com/wzpan/dingdang-robot/wiki/install#%E5%AE%89%E8%A3%85%E5%90%8E%E7%BB%AD) ，完成配置，并升级一下叮当和插件才使用。

## dingdang-respeaker-2017-11-06

- 在 dingdang-2017-10-29 的基础上，加入 ReSpeaker 2mic 和 4mic 的驱动（没有 ReSpeaker 开发板的朋友请下载 [dingdang-2017-10-29](#dingdang-2017-10-29) 版本镜像）；
- 将默认 STT 引擎改回 baidu-stt ，以避免因为中转服务器不可用导致 STT 失败的问题；
- 提供一键切换驱动脚本，可以在 2mic/4mic 间切换。使用方法为：

``` sh
cd $HOME
sudo ./switch.sh 型号  # 型号可以是 2mic 或 4mic
```

|  镜像  |  md5 值 | 说明 |
| ------ |  ---- |  ---- |
| [dingdang-respeaker-2017-11-06.img.gz](https://share.weiyun.com/efc7d7973cd07f04b90d2f3456799d6f) |  32ed3102bfa8f2308c56a42acb6693ac | [备选百度云下载地址](https://pan.baidu.com/s/1kVACxmv) （密码：r3n6） |

## dingdang-2017-10-29

本次版本为预览版。不带 respeaker 驱动。

### 新特性

- 基于目前最新的 Raspbian Stretch 系统；
- 新的自启动方式，无论是 ssh 进系统，还是直接使用系统，均可以在终端中执行 `tmux attach` 命令切换到运行中的 dingdang-robot 的任务；
- 增加科大讯飞和阿里的语音识别和合成（[e3e742a](https://github.com/wzpan/dingdang-robot/commit/e3e742a621ace8588a139649e706e678aae586ea), [8a7e7f6](https://github.com/wzpan/dingdang-robot/commit/8a7e7f6a37912492719f571635cdaef274404c9d)）。默认使用科大讯飞的语音；
- 增加 Emotibot 机器人，并作为默认开启的聊天机器人（[a0cd5a9](https://github.com/wzpan/dingdang-robot/commit/a0cd5a969fc58e70403eb357f6fedf2234320d12)）；
- 增加 HomeAssistant 插件（[d1a34bc](https://github.com/wzpan/dingdang-robot/commit/d1a34bcb2b970463b3b949b0097989f9e2aec726)）；
- 增加任务提醒功能（[77a71e4](https://github.com/wzpan/dingdang-robot/commit/77a71e415027a5c13794b611c511de056126796e)）；
- 增加多轮对话和闲聊插件（[b3250cc4](https://github.com/wzpan/dingdang-robot/commit/b3250cc40a27d527628df370dcd2fe94ca8178a9)，[7ceacd5](https://github.com/wzpan/dingdang-robot/commit/7ceacd5abe86f3cbd47e57651549d3807acb3f1c)）；
- 增加 Google-TTS，支持粤语发音（[899a8d3](https://github.com/wzpan/dingdang-robot/commit/899a8d34ef0b85d8604b572304e241c2e93d79b4)，[a5a0e63](https://github.com/wzpan/dingdang-robot/commit/a5a0e63d48da3c9386230d186c3892494f27bf7b)）；
- 增加 `wechat_echo` 选项，支持将微信语音解析成指令（只支持百度stt）（[115e3fd](https://github.com/wzpan/dingdang-robot/commit/115e3fde2e4796e3c114f7340c12825102f9ecf7)）。
- 支持 USB 摄像头（[3717eb4](https://github.com/wzpan/dingdang-robot/commit/3717eb40e62e542ef7534761210e89fd3cea9534)）。

### 新增第三方插件

- [WOL](WOL) 通过WOL(Wake On Lan)实现语音开机
- [EmailMyPC](EmailMyPC) 以邮件方式实现语音操控电脑
- [ToDo](ToDo) 简单的备忘插件
- [RaspberryPiStatus](RaspberryPiStatus) 简单的树莓派状态查询插件
- [HeadlineNews](HeadlineNews) 新闻头条播报插件
- [Direction](Direction) 出行路线规划插件
- [BaiduFM](BaiduFM) 百度FM音乐播放插件
- [Dictionary](Dictionary) 成语词典插件

### 感谢代码贡献者（排名不分先后）

@musistudio 、@kira8565 、@bubble6 、@Deschanel 、@yunxiyinzhe 、@GoldJohnKing、@BeLittleYang 

### 下载信息

|  镜像  |  对应版本  | md5 值 | 说明 |
| ------ | --------- | ---- |  ---- |
| [dingdang-2017-10-29.img.gz](https://share.weiyun.com/e51d8117d91ffba114a8c05f9faad993) | [0.2.0](https://github.com/wzpan/dingdang-robot/releases/tag/v0.2.0) | 737bfb20c742605b81d1d85f2017bbc9 | [备选百度云下载地址](https://pan.baidu.com/s/1eRJtuqY) （密码：as1a） |

## dingdang-2017-8-13

- **注意啦**：默认唤醒词由“叮当”更换为“嘿叮当”，以降低误识别率；
- 若干 bug 改进；
- 增强了微信控制的能力；
- 提高snowboy识别准确率；
- 增加插件的enable开关，支持通过配置文件开关插件；
- 改用sox播放mp3，缩短语音播放响应时间；
- 更换阿里云镜像源为USTC镜像源，修改raspi源（[#11](https://github.com/wzpan/dingdang-robot/issues/11)）；
- ReSpeaker 2-Mics Pi HAT 版专项优化：
  - 集成 ReSpeaker 2-Mics Pi HAT 驱动；
  - 唤醒、思考和说话时会配合 LED 灯控制（暂不支持音乐模式）；
  - 按钮可开关麦克风，从而开/关语音交互；
  - 开机启动。
- 感谢 @广东-豳默尒潴╮  帮忙上传镜像到百度云。感谢 @SMILEORIGIN 帮忙上传到钉盘。

分为两个版本：

* dingdang-2017-8-13.img：叮当原生镜像；
* dingdang-2017-8-13-respeaker.img：ReSpeaker 2-Mics Pi HAT 版镜像，集成了 ReSpeaker 的驱动支持。

|  镜像  |  对应版本  | md5 值 | 说明 |
| ------ | --------- | ---- |  ---- |
| [dingdang-2017-8-13.img.gz](https://share.weiyun.com/ca5a6c9e8a31ed86dd1ff602e5a1d62b) | [0.1.11](https://github.com/wzpan/dingdang-robot/releases/tag/v0.1.11) | 371ea0f57670c04a39186be45120b02d | [备选百度云下载地址](http://pan.baidu.com/s/1slLQLyd) （密码：23w8） [备选钉盘下载地址](https://space.dingtalk.com/s/gwHN4rkCzhPON_0D2gAgNjMwNTQ2YThjN2U2NGUyZmI3Y2EwMTNlMWExNGM2ODQ) (密码：hhAN)|
| [dingdang-2017-8-13-respeaker.img.gz](https://share.weiyun.com/eebc7fba68875923a683613cdb08bb97) | [respeaker-v0.1.0](https://github.com/wzpan/dingdang-robot/releases/tag/respeaker-v0.1.0) | 8bbae750a18920d2b122da0b0ad2b1b0 | [备选百度云下载地址](http://pan.baidu.com/s/1boR2KDx) （密码：i07y） |

## <del>dingdang-2017-6-11.img（已过时）</del>

- 大幅提升响应速度；
- 新增 SendQR 和天气插件；
- 新增 snowboy 离线唤醒引擎；
- 新增带 `[control]` 标题的邮件识别，支持邮件远程控制叮当；
- 新增带 `[echo]` 标题的邮件识别，直接阅读标题；
- 合成语音播放问题修复；
- 邮件新增 `enable` 开关，允许关闭邮件功能。
- 感谢 @啄木鸟㊣ 帮忙上传镜像到百度云！

|  镜像  |  对应版本  | md5 值 | 说明 |
| ------ | --------- | ---- |  ---- |
| [dingdang-2017-6-11.img.gz](https://share.weiyun.com/3403a509fd64369dd6895679c626a3cb) | [0.1.4](https://github.com/wzpan/dingdang-robot/releases/tag/v0.1.4) | e5ed37d2fea0c591496476c01fd1e7b4 | [备选百度云下载地址](http://pan.baidu.com/s/1boUNvXX) （密码：dwvo） |

## <del>dingdang-2017-5-20.img（已过时）</del>

- First release
- 感谢 @PHP开发者 帮忙上传镜像！

|  镜像  |  对应版本  | md5 值 | 说明 |
| ------ | --------- | ---- |  ---- |
| [dingdang-2017-5-20.img.gz](http://pan.baidu.com/s/1nuTMfax) 密码 vuby| [0.1.0](https://github.com/wzpan/dingdang-robot/releases/tag/0.1.0) | 4844ddbd62f509b063f9ae79404afcb9 | 首次发布 |

