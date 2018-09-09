# -*- coding: utf-8 -*-
import os
import cv2
import sys
import time
import urllib
import logging
import tarfile
import numpy as np
import tensorflow as tf
import pygame.camera
from pygame.locals import *
import six.moves.urllib as urllib

sys.path.append("/usr/local/lib/python2.7/dist-packages/tensorflow/models/research/")
from object_detection.utils import label_map_util

WORDS = ["MUBIAOSHIBIE"]
SLUG = "object_detection"


class PygameStream(object):
    def __init__(self):
        self.frame = None
        self.image_np = None
        self.size = (320, 240)
        self.display = pygame.display.set_mode(self.size, 0)  # create a display surface. standard pygame stuff
        pygame.camera.init()
        self.clist = pygame.camera.list_cameras()  # this is the same as what we saw before
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()

        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_image_and_flip(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0, 0))
        pygame.display.flip()

    def image_data_transform(self):
        image_string = pygame.image.tostring(self.snapshot, 'RGB')
        # Convert the picture into a numpy array
        self.image_np = np.fromstring(image_string, dtype=np.uint8).reshape(240, 320, 3)
        # self.frame = cv2.cvtColor(self.image_np, cv2.COLOR_BGR2GRAY)  # Covert to grayscale

    def face_detection(self):
        self.image_data_transform()
        face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(self.frame, 1.1, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(self.image_np, (x, y), (x + w, y + h), (255, 255, 0), 2)
        if len(faces) > 0:
            print("Found face(s)")
            cv2.imwrite('result.jpg', self.image_np)
            return True

    def handle(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False
            self.get_image_and_flip()
            self.image_data_transform()
            self.cam.stop()
            return self.image_np


class TensorflowDetection(object):
    def __init__(self,
                 config_path,
                 mic,
                 url='http://download.tensorflow.org/models/object_detection/',
                 model_name='ssd_mobilenet_v1_coco_2017_11_17',
                 path_to_ckpt='frozen_inference_graph.pb',
                 path_to_label='mscoco_label_map.pbtxt',
                 num_classes=80):

        self._logger = logging.getLogger(__name__)
        self.config_path = config_path
        self.mic = mic
        self.url = url
        self.model_name = self.config_path + '/' + model_name
        if not os.path.exists(self.model_name):
            self.get_detection_model()
        self.path_to_ckpt = os.path.join(self.model_name, path_to_ckpt)
        self.path_to_label = os.path.join(self.config_path + '/' + 'label', path_to_label)
        self.num_classes = num_classes
        self.detection_graph = self.load_detection_graph()
        self.category_index = self.load_category_index()

        self._logger.info("model_name:%s" % self.model_name)
        self._logger.info("path_to_ckpt:%s" % self.path_to_ckpt)
        self._logger.info("path_to_label:%s" % self.path_to_label)

    def get_detection_model(self):
        model_file = self.model_name + '.tar.gz'
        opener = urllib.request.URLopener()
        opener.retrieve(self.url + model_file, model_file)
        tar_file = tarfile.open(model_file)
        for t_f in tar_file.getmembers():
            file_name = os.path.basename(t_f.name)
            if 'frozen_inference_graph.pb' in file_name:
                tar_file.extract(t_f, os.getcwd())

    def load_detection_graph(self):
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return detection_graph

    def load_category_index(self):
        label_map = label_map_util.load_labelmap(self.path_to_label)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.num_classes,
                                                                    use_display_name=True)
        return label_map_util.create_category_index(categories)

    @staticmethod
    def load_image_into_numpy_array(img):
        (im_width, im_height) = img.size
        return np.array(img.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

    def handle_forever(self):
        try:
            with self.detection_graph.as_default():
                with tf.Session() as sess:
                    # Get handles to input and output tensors
                    ops = tf.get_default_graph().get_operations()
                    all_tensor_names = {output.name for op in ops for output in op.outputs}
                    tensor_dict = {}
                    for key in ['num_detections', 'detection_boxes', 'detection_scores', 'detection_classes',
                                'detection_masks']:
                        tensor_name = key + ':0'
                        if tensor_name in all_tensor_names:
                            tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

                    image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                    while True:
                        try:
                            self._logger.info('离线唤醒监听中')
                            threshold, transcribed = self.mic.passive_listen('ALIADA')
                        except Exception, e:
                            self._logger.debug(e)
                            threshold, transcribed = (None, None)

                        if not transcribed or not threshold:
                            self._logger.info("Nothing has been said or transcribed.")
                            continue

                        order = self.mic.active_listen(MUSIC=True)
                        if order:
                            if any(ext in order for ext in [u"结束", u"退出", u"停止"]):
                                self.mic.say(u"退出目标识别模式")
                                return
                            if any(ext in order for ext in [u"识别", u"检测"]):
                                start_time = time.time()
                                ps = PygameStream()
                                time.sleep(1)
                                image = ps.handle()

                                output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(image, 0)})

                                classes = output_dict['detection_classes'][0].astype(np.uint8)
                                boxes = output_dict['detection_boxes'][0]
                                scores = output_dict['detection_scores'][0]

                                class_name_list = list()

                                for i in range(min(20, boxes.shape[0])):
                                    if scores is None or scores[i] > .5:
                                        if classes[i] in self.category_index.keys():
                                            class_name = self.category_index[classes[i]]['name']
                                        else:
                                            class_name = u'未知物品'
                                        class_name_list.append(class_name)
                                if class_name_list:
                                    class_name = list(set(class_name_list))
                                    class_name = u'和'.join(class_name)
                                    self.mic.say(u'这是%s' % class_name)
                                else:
                                    self.mic.say(u'抱歉，这些我都不认识！')
                                self._logger.info(u"识别耗时:%s" % (time.time() - start_time))
                        else:
                            self.mic.say(u"什么？")
        except Exception as e:
            self._logger.info("错误：%s" % e)
            self.mic.say(u'抱歉，我的眼睛出毛病了！')


def handle(text, mic, profile, wxbot=None):
    """
    Responds to user-input, typically speech text

    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        wxbot -- wechat bot instance
    """
    if SLUG not in profile:
        mic.say(u'目标检测插件配置有误，插件使用失败')
        return
    odm = TensorflowDetection(config_path=mic.aliadapath.DATA_PATH, mic=mic)
    mic.say(u"进入目标识别模式，请发出具体语音指令！")
    odm.handle_forever()


def isValid(text):
    """
        Returns True if the input is related to weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text for word in [u"目标检测", u"目标识别"])
