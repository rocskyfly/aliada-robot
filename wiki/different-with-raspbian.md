# 叮当镜像文件与 Raspbian 系统的区别

叮当镜像是在 Raspbian 系统的基础上做的定制。目的是提供一个尽可能开箱即用的叮当机器人运行环境。

安装过程中所有的操作都在 `/home/pi/.bash_history` 中记录。

下文将列举主要的定制。

## 中文化设定

* Locale设为中国
* 时区设为中国香港
* Keyboard 设为 Chinese
* WiFi Country设为中国

## 权限开启

如下的权限默认开启，您可以在 raspi-config 中重新关闭：

* 相机
* SSH 
* VNC

## 高级设定

* Memory Split 设置为 16 ，以减少对内存的浪费，提高运行性能。如果需要跑其他需要GPU任务，可以改为 128 。

## 镜像源替换

* 更换apt源为阿里镜像源
* 更换PyPi源为清华大学镜像源

## 软件安装

* emacs - 编辑器
* vim - 编辑器
* sox - 命令行音乐播放器，用于网易云音乐播放
* tmux - 终端复用插件
* pocketsphinx - 离线STT
* cmuclmtk - 离线STT
* m2m-aligner - 离线STT
* MITLM - 离线STT
* Phonetisaurus - 离线STT
* python-pymad - 百度STT
* git-core - 代码拉取
* tightvncserver - VNC 服务器

Python 依赖的若干程序：

* python-dev
* python-pip
* bison
* libasound2-dev
* libportaudio-dev
* python-pyaudio

以及编译用的软件：

* subversion
* autoconf
* libtool
* automake
* gfortran
* g++

## 其他

* 集成了训练好的 FST 模型（/home/pi/g014b2b）