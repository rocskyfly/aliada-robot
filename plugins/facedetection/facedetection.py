import cv2
import numpy
import pygame.camera
from pygame.locals import *


class FaceDetection(object):
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
        self.image_np = numpy.fromstring(image_string, dtype=numpy.uint8).reshape(240, 320, 3)
        self.frame = cv2.cvtColor(self.image_np, cv2.COLOR_BGR2GRAY)  # Covert to grayscale

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

            if self.face_detection():
                self.cam.stop()
                going = False


if __name__ == '__main__':
    fd = FaceDetection()
    fd.handle()
