# How to install chundesy on raspberry pie?

## Table of Contents

* [Install Manually](#Manually Installation)
* [安装后续](#安装后续)

## Manually Installation

The user directories mentioned below are all "/home/robot".If you are installing on another system, the user directory should be changed to your corresponding directory.For example, "/home/myname".

### Install Raspbian 

Firstly, you need to goto http://downloads.raspberrypi.org/raspbian_latest to download the latest Raspbian systems, brush into the SD card.

### Configure Raspbian

Enter the Raspbian os to configurate

``` sh
sudo raspi-config
```

Then, in the advanced options, select ` Expand Filesystem ` option. Reboot Raspberry Pi to make it work.

Execute the following command, update the system, and install several tools:

``` sh
sudo apt-get install -y debian-keyring debian-archive-keyring
sudo apt-get update
sudo apt-get upgrade --yes
sudo apt-get install git-core python-dev bison python-pymad cmake uuid-dev fswebcam --yes --allow-unauthenticated

emacs libatlas-base-dev libav-tools

sudo apt-get install libportaudio-dev python-pyaudio --yes

libasound2-dev ->libasound-dev?

sudo easy_install pip
```

之后[配置下你的麦克风和音响](https://github.com/wzpan/dingdang-robot/wiki/configuration#%E9%85%8D%E7%BD%AE%E9%BA%A6%E5%85%8B%E9%A3%8E)确保能正常工作。

### Install Aliada

firstly, git clone Chundesy clone to your "/home/robot":

``` sh
git clone https://github.com/rocskyfly/aliada-car-robot.git
cd aliada-car-robot
```

Then install the required pypi libraries:

``` sh
sudo pip install --upgrade setuptools
sudo pip install -r client/requirements.txt
```

接下来创建一个 **.aliada** 目录，该目录用于维护你的个人数据（注意是带了点的 `.aliada` 目录）：
Next create a **.aliada** directory under "/home/robot/aliada-car-robot", the directory is used to maintain your personal data.

``` sh
mkdir /home/robot/aliada-car-robot/.aliada
```

Copy [叮当配置文件](https://github.com/wzpan/dingdang-robot/wiki/configuration#%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6) to "/home/robot/chundesy-car-robot/.chundesy" as a file named "profile.yml".

### Install Sox

百度的语音合成结果返回的是 mp3 格式的音频，因此需要安装一个 mp3 播放器播放合成结果：

``` sh
sudo apt-get install sox  # 用于播放音乐
sudo apt-get install libsox-fmt-mp3 # 添加 sox 的 mp3 格式支持
```

### Install TaskWarrior

用于日程提醒。软件源自带的版本较老，不支持时间粒度的提醒。因此需编译安装较新的 2.5.1 版本：

``` sh
cd $HOME
wget https://taskwarrior.org/download/task-2.5.1.tar.gz
tar xzvf task-2.5.1.tar.gz
cd task-2.5.1
cmake -DCMAKE_BUILD_TYPE=release . -DENABLE_SYNC=OFF
make
sudo make install
```

如果提示找不到 `cmake` 或者 `uuid`，则需要安装一下：

``` sh
sudo apt-get install cmake uuid-dev
```

完成后创建一个 .taskrc 文件用来记录日程：

```
touch /home/pi/.taskrc
```

### Install PocketSphinx offline STT engine

PocketSphinx 是叮当所使用的离线STT引擎，用于离线唤醒。要使用它总共需要安装如下一些程序：

* sphinxbase & pocketsphinx
* CMUCLMTK
* MIT Language Modeling Toolkit
* m2m-aligner
* Phonetisaurus

#### 安装 Sphinxbase/Pocketsphinx

Stretch 已经包含了 PocketSphinx 的源，可以先装预编译的版本：

``` sh
sudo apt-get install pocketsphinx  # for stretch
```

如果是 Ubuntu 系统，则应该安装另一个包：

``` sh
apt-get install pocketsphinx-hmm-en-hub4wsj
```

预编译的版本包含了 hmm 库 `pocketsphinx-hmm-en-hub4wsj` ，省去自己编译的麻烦。但这个版本没有包含 Python 的接口，所以还得拉源码构建一次。

```
wget http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz
tar -zxvf sphinxbase-0.8.tar.gz
cd sphinxbase-0.8/
./configure --enable-fixed
make
sudo make install
wget http://downloads.sourceforge.net/project/cmusphinx/pocketsphinx/0.8/pocketsphinx-0.8.tar.gz
tar -zxvf pocketsphinx-0.8.tar.gz
cd pocketsphinx-0.8/
./configure
make
sudo make install
```

#### 安装 CMUCLMTK

``` sh
sudo apt-get install subversion autoconf libtool automake gfortran g++ --yes
svn co https://svn.code.sf.net/p/cmusphinx/code/trunk/cmuclmtk/
cd cmuclmtk/
./autogen.sh && make && sudo make install
cd ..
```

#### 安装 Phonetisaurus， m2m-aligner 以及 MITLM

先下载源码：

``` sh
wget http://distfiles.macports.org/openfst/openfst-1.4.1.tar.gz
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/m2m-aligner/m2m-aligner-1.2.tar.gz
wget https://github.com/mitlm/mitlm/releases/download/v0.4.1/mitlm_0.4.1.tar.gz
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/phonetisaurus/is2013-conversion.tgz
```

解压：

``` sh
tar -xvf openfst-1.4.1.tar.gz
tar -xvf m2m-aligner-1.2.tar.gz
tar -xvf mitlm_0.4.1.tar.gz
tar -xvf is2013-conversion.tgz
```

编译安装 OpenFST：

``` sh
cd openfst-1.4.1/
sudo ./configure --enable-compact-fsts --enable-const-fsts --enable-far --enable-lookahead-fsts --enable-pdt
sudo make install # come back after a really long time
```

编译安装 M2M：

``` sh
cd m2m-aligner-1.2/
sudo make
sudo cp m2m-aligner /usr/local/bin/m2m-aligner
```

编译安装 MITLMT：

``` sh
cd mitlm-0.4.1/
sudo ./configure
sudo make install
```

编译安装 Phonetisaurus：

```
cd is2013-conversion/phonetisaurus/src
sudo make
sudo cp ../../bin/phonetisaurus-g2p /usr/local/bin/phonetisaurus-g2p
```

然后需要下载已编译好的 Phonetisaurus FST 模型以及叮当内置的词汇模型：

* g014b2b.zip：https://pan.baidu.com/s/1o7MrWIA 下载完后放在 /home/pi/ 目录下执行 `unzip` 命令解压。
* vocabularies.zip：https://pan.baidu.com/s/1kWfqP3x （[备选下载地址](https://share.weiyun.com/a7d78e697fb684af048229e9d531ba80)）下载完后放在 /home/pi/**.dingdang**/ 目录下执行 `unzip` 命令解压。注意是带了点的
 `.dingdang` 目录。

注意如果你是在另外一台机上下载这两个文件，你可能需要使用 [fstp](http://www.cnblogs.com/chen1987lei/archive/2010/11/26/1888391.html) 命令来发送文件至叮当的主机上。

### 配置叮当

根据你的实际情况和需求[配置叮当](https://github.com/wzpan/dingdang-robot/wiki/configuration) 。

### 运行叮当

最后，运行叮当，看看有没有提示缺少什么库，根据提示安装一下即可。

``` python
cd dingdang
python dingdang.py
```

然后查看 [安装后续](#安装后续)。

注意：启动时如果遇到这个错误信息，是 PyAudio 的提醒，不影响工作，不用管：

```
Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
```

## 安装后续

1. 让树莓派连接网络及开启 SSH ：参考 [这篇文章](http://shumeipai.nxez.com/2017/09/13/raspberry-pi-network-configuration-before-boot.html) ，让树莓派连接网络并开启 SSH 。

2. 终端执行 `raspi-config` 进入树莓派命令，进入 Advanced Options ，开启 Expand File System，扩展您的 Micro-SD 卡空间（否则刷完只有 8G 容量）。使用 Respeaker 2-Mics Pi HAT 的用户，还推荐进入 Interfacing Options ，开启 SPI ，以支持控制 LED 灯。
3. 参考 [配置](https://github.com/wzpan/dingdang-robot/wiki/configuration) 一节，完成配置。
4. 进入 dingdang 的目录，更新一下 dingdang ：

``` sh
cd ~/dingdang
git pull
```

5. 如果安装了第三方插件 dingdang-contrib，进入 .dingdang/contrib，更新下第三方插件：

``` sh
cd /home/pi/.dingdang/contrib
git pull
pip install --upgrade -r requirements.txt
```

6. 运行叮当：

``` sh
python dingdang.py
```

如果设置开启了微信，会出现一个二维码，用微信扫一扫登录即可完成微信接入（相当于登录了一个微信客户端）。