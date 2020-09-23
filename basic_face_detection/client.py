#!/usr/bin/env python
# -*- coding: utf-8 -*-
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2, time
from websocket import create_connection


# フレームサイズ
FRAME_W = 320
FRAME_H = 240
# 正面顔検出データ
cascPath = 'lbpcascade_frontalface.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
camera = PiCamera()
camera.resolution = (FRAME_W, FRAME_H)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(FRAME_W, FRAME_H))
time.sleep(0.1)
# メインループ
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = image.array
    # 顔検出
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist( gray )
    faces = faceCascade.detectMultiScale(gray, 1.1, 3, 0, (10, 10))
    # 検出時の処理
    for (x, y, w, h) in faces:
        # websocket送信
        ws = create_connection("ws://192.168.1.222:1880/ws/light")
        ws.send("Hello,World")
        # 見つけた顔を矩形で囲む
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    frame = cv2.resize(frame, (540,300))
    # ビデオに表示 
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
ws.close()
cv2.destroyAllWindows()