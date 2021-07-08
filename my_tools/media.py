# -*- coding: utf-8 -*-
# File  : media.py
# Author: huwei
# Date  : 2021/6/1

import cv2
from moviepy.editor import *

class Media:

    def __init__(self, media_path):
        self.cap = cv2.VideoCapture(media_path)
        if not os.path.exists(media_path):
            raise RuntimeError("Video meida path:{} not exists".format(media_path))

        self.video_path = media_path
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if self.frame_length == 0:
            raise RuntimeError("Video meida path:{} is empty".format(media_path))

        self.duration = self.frame_length / self.fps  # duration of seconds
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    def __repr__(self):
        return "Video media path:{},fps:{},frame count:{},resolution:{}x{}".format(self.video_path, self.fps,
                                                                                   self.frame_length, self.width,
                                                                                   self.height)
    def __del__(self):
        self.cap.release()
        print("Video cap release")

    def frame(self, idx):
        if idx < 0 or idx > self.frame_length:
            raise IndexError("idx out of range")

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = self.cap.read()
        if not ret:
            raise BrokenPipeError
        return frame

    def all_frames(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        while True:
            idx = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            ret, frame = self.cap.read()
            if not ret:
                break
            else:
                yield frame, int(idx)

    def part_frames(self, index_range, step=1):
        start_index = index_range[0]
        end_index = index_range[1]

        if start_index > end_index or start_index < 0 or end_index > self.frame_length:
            raise ValueError("index range out of video frames")

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_index)
        nums = 0
        while True:
            idx = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            ret, frame = self.cap.read()
            nums += 1
            if (nums - 1) % step != 0:
                continue

            if not ret or idx > end_index:
                break
            else:
                yield frame, int(idx)

    def write_part(self, save_path, index_range=None):
        if index_range is None:
            index_range = (0, self.frame_length)

        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'MJPG'), self.fps,
                                 (int(self.width), int(self.height)))

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index_range[0])
        for idx in range(index_range[0], index_range[1] + 1, 1):
            save_path = os.path.join(save_dir, "{}.jpg".format(idx))
            vidx = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            if vidx != idx:
                raise IndexError(f"None equal video index {idx}!={vidx}")
            ret, frame = self.cap.read()
            writer.write(frame)

    def write_part_with_audio(self, save_path, index_range=None):
        if index_range is None:
            index_range = (0, self.frame_length)

        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        cliper = VideoFileClip(self.video_path)
        start_time = index_range[0] / self.fps
        end_time = index_range[1] / self.fps

        part = cliper.subclip(start_time, end_time)
        part.write_videofile(save_path)