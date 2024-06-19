import json
from pathlib import Path
import warnings
import random
from copy import deepcopy


class COCO:
    def __init__(self, anno_file):
        with open(anno_file) as f:
            data = json.load(f)

        self.anno_file = Path(anno_file)

        self._categories = data["categories"]
        self._info = data["info"]
        self._license = data["license"]
        self._images = data["images"]
        self._annotations = data["annotations"]

        self.build_image_annotation_dict()

    def build_image_annotation_dict(self):
        image_anno_dict = {}
        for x in self._annotations:
            if x["image_id"] in image_anno_dict:
                image_anno_dict[x['image_id']].append(x)
            else:
                image_anno_dict[x['image_id']] = [x, ]

        image_dict = {x["id"]: x for x in self._images}
        cate_dict = {x['id']: x for x in self._categories}

        self._image_anno_dict = image_anno_dict
        self._image_id_dict = image_dict
        self._cate_dict = cate_dict

    @property
    def images(self):
        return [(x["id"], x["file_name"]) for x in self._images]

    @property
    def categories(self):
        return [(x["id"], x["name"]) for x in self._categories]

    def __repr__(self):
        return f"COCO Data of {self.anno_file}, with image size {len(self._images)} and annotation size {len(self._annotations)}"

    def __iter__(self):
        for im_id, name in self.images:
            yield self.sample(im_id)
    
    def __len__(self):
        return len(self._images)

    def sample(self, idx):
        return deepcopy(self._image_id_dict[idx]), \
            deepcopy(self._image_anno_dict[idx]) if idx in self._image_anno_dict else []

    def clear_no_instance_image(self):
        new_images = []
        source_size = len(self._images)
        for x in self._images:
            im_id = x["id"]
            if im_id in self._image_anno_dict:
                new_images.append(x)
        self.update(images=new_images)

        print(f"clear no instance images, clear size {source_size} to {len(self._images)}")

    def random_sample(self, k):
        images = self.images
        if k > len(images):
            warnings.warn(f"try to sample {k} from {len(images)} number data")
            k = len(images)

        images = random.sample(images, k=k)
        for im_id, im_name in images:
            yield self.sample(im_id)

    def update(self, categories=None, images=None, annotations=None):
        if categories is not None:
            self._categories = categories
        if images is not None:
            self._images = images
        if annotations is not None:
            self._annotations = annotations

        self.build_image_annotation_dict()

    def save(self,save_dir,override=False):
        save_path = Path(save_dir)
        save_path = save_path / self.anno_file.name if save_path.is_dir() else save_path

        if save_path.exists():
            raise FileExistsError(f"{save_path} exists!")
        
        save_path.parent.mkdir(parents=True,exist_ok=True)
        
        with open(save_path,"w") as f:
            json.dump({
                "info":self._info,
                "license":self._license,
                "categories":self._categories,
                "images":self._images,
                "annotations":self._annotations,
            },f)
    
    def save2yolo(self,save_dir,use_kpts=False,use_segment=False):
        pass