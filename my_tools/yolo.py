import json
import warnings
import random
import glob
import cv2
import numpy as np
from copy import deepcopy
from pathlib import Path

def img2label_paths(img_paths):
    """Define label paths as a function of image paths."""
    sa, sb = f"{os.sep}images{os.sep}", f"{os.sep}labels{os.sep}"  # /images/, /labels/ substrings
    return [sb.join(x.rsplit(sa, 1)).rsplit(".", 1)[0] + ".txt" for x in img_paths]

class YOLO:
    def __init__(self,img_path = None) -> None:
        f = []  # image files
        if img_path is not None:
            for p in img_path if isinstance(img_path, list) else [img_path]:
                p = Path(p)  # os-agnostic
                if p.is_dir():  # dir
                    f += glob.glob(str(p / "**" / "*.*"), recursive=True)
                elif p.is_file():  # file
                    with open(p) as t:
                        t = t.read().strip().splitlines()
                        parent = str(p.parent) + os.sep
                        f += [x.replace("./", parent) if x.startswith("./") else x for x in t]  # local to global path
                else:
                    raise FileNotFoundError(f"{self.prefix}{p} does not exist")
        
        self._images = f
        self._labels = img2label_paths(img_paths=f)
    
    def update_images(self,images):
        self._images = images
        self._labels = img2label_paths(self._images)
    
    def __len__(self):
        return len(self._images)

    def __iter__(self):
        for i in range(len(self._images)):
            yield self._images[i],self._labels[i]

    def decode_label(self,label_file,bbox_fmt="xyxy"):
        label = [x.split() for x in open(label_file).read().strip().splitlines()]
        label = np.array(label,dtype=np.float64)
        if bbox_fmt == "xyxy":
            label[:,[1,2]] = label[:,[1,2]] - label[:,[3,4]]/2
            label[:,[3,4]] = label[:,[1,2]] + label[:,[3,4]]
        elif bbox_fmt == "xyhw":
            label = label
        
        if label.shape[-1] == 5:
            return label[:,0].astype(np.int32),label[:,1:5].reshape(-1,2,2)
        else:
            return label[:,0].astype(np.int32),label[:,1:5].reshape(-1,2,2),label[:,5:]
    
    def save2txt(self,save_path):
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True,exist_ok=True)
        with open(save_path,"w") as f:
            for file in self._images:
                f.writelines(f+"\n")

def merge_yolo(data_1:YOLO,data_2:YOLO,dedup_by_file:bool=True):
    images_1 = data_1._images
    images_2 = data_2._images

    images = images_1 + images_2
    if dedup_by_file:
        images = list(set(images))
    
    yolo = YOLO()
    yolo.update_images(images)
    return yolo
