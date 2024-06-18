import numpy as np
import cv2

coco_pose17_mapping = [(0,1),(0,2),(1,3),(2,4),(3,5),(4,6),(6,5),
                       (5,7),(7,9),(6,8),(8,10),(6,12),(12,14),
                       (14,16),(5,11),(11,13),(13,15)]

def plot_bbox(image,bbox,color=(0, 0, 255)):
    image = np.copy(image)

    bbox = np.array(bbox).reshape(4).astype(np.int32)
    cv2.rectangle(image, bbox[:2], bbox[2:], color=color)
    return image

def plot_points(image,pts,color=(0, 0, 255)):
    image = np.copy(image)

    if pts is not None:
        pts = np.array(pts).reshape(-1, 2).astype(np.int32)
        for pt in pts:
            cv2.circle(image, pt, radius=2, color=color, thickness=-1)
    return image

def plot_label(image,label,org=None,color=(0, 0, 255)):
    image = np.copy(image)

    h, w = image.shape[:2]
    x1, y1 = org if org is not None else (5, h - 5)
    if isinstance(label, (list, tuple)):
        text = ";".join(label)
    else:
        text = str(label)

    retval, baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
    x1 -= 2
    y1 -= 2
    topleft = (x1, y1 - retval[1])
    bottomright = (topleft[0] + retval[0], topleft[1] + retval[1])
    cv2.rectangle(image, (topleft[0], topleft[1] - baseline), bottomright, thickness=-1, color=(0, 0, 0))
    cv2.putText(image, text, (x1 - 2, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=color, thickness=2)
    return image

def plot_pose(image,pts,color=(0,255,0),fmt="coco17"):
    image = np.copy(image)
    if fmt=="coco17":
        assert len(pts)>=17
        for i,j in coco_pose17_mapping:
            pt1 = pts[i].astype(np.int32)
            pt2 = pts[j].astype(np.int32)
            cv2.line(image,pt1,pt2,color=color)
    else:
        raise f"Invalid pose format {fmt}"

    return image
    

def plot_image(image, bbox=None, pts=None, label=None, color=(0, 0, 255)):
    image = np.copy(image)

    if bbox is not None:
        image = plot_bbox(image,bbox,color)

    if pts is not None:
        image = plot_points(image,pts,color)

    if label is not None:
        if bbox is None:
            image = plot_label(image,label,color)
        else:
            image = plot_label(image,label,bbox[:2],color)

    return image
