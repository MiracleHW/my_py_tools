import json
from pathlib import Path
import warnings
import random
from copy import deepcopy
import glob
import cv2

def img2label_paths(img_paths):
    """Define label paths as a function of image paths."""
    sa, sb = f"{os.sep}images{os.sep}", f"{os.sep}labels{os.sep}"  # /images/, /labels/ substrings
    return [sb.join(x.rsplit(sa, 1)).rsplit(".", 1)[0] + ".txt" for x in img_paths]

class YOLO:
    def __init__(self,img_path) -> None:
        f = []  # image files
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
    
    def __len__(self):
        return len(self._images)

    def __iter__(self):
        for i in range(len(self._images)):
            yield self._images[i],self._labels[i]

    def decode(self,img,label_file):
        img = cv2.imread(img) if isinstance(img,str) else img

        pass