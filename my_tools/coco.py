import json
from pathlib import Path


class Coco:
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
        return f"CoCoData of {self.anno_file}, with image size {len(self.images)} and annotation size {len(self.annotations)}"

    def __iter__(self):
        for im_id, name in self.images:
            yield self.sample(im_id)

    def sample(self, id):
        return self._image_id_dict[id], self._image_anno_dict[id] if id in self._image_anno_dict else []

    def update(self, categories=None, images=None, annotations=None):
        if categories is not None:
            self._categories = categories
        if images is not None:
            self._images = images
        if annotations is not None:
            self._annotations = annotations

        self.build_image_annotation_dict()
