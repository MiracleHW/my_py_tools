# -*- coding: utf-8 -*-
# File  : image.py
# Author: huwei
# Date  : 2021/3/24

import numpy as np
import cv2
import base64
import requests
import hashlib

__all__ = ["BufferImageDecode","B64ImageDecode","UrlImageDecode","B64ImageEncode"
           "ImageMD5Encode",]

def BufferImageDecode(image_buffer):
    nparr = np.frombuffer(image_buffer, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

def B64ImageDecode(image_b64):
    image_buffer = base64.b64decode(image_b64)
    return BufferImageDecode(image_buffer)

def UrlImageDecode(image_url,timeout=30):
    r = requests.get(image_url,stream=True,timeout=timeout)
    image_buffer=r.content
    return BufferImageDecode(image_buffer)

def ImageMD5Encode(image):
    rect,image_buffer=cv2.imencode(".jpg",image)
    md5_l = hashlib.md5()
    md5_l.update(image_buffer)
    md5 = md5_l.hexdigest()
    return md5

def B64ImageEncode(image):
    rect,image_buffer=cv2.imencode(".jpg",image)
    b64=base64.b64encode(image_buffer)
    return b64