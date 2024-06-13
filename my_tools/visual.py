import numpy as np
import cv2


def plot_image(image, bbox=None, pts=None, label=None, color=(0, 0, 255)):
    image = np.copy(image)

    if bbox is not None:
        bbox = np.array(bbox).reshape(4).astype(np.int32)
        cv2.rectangle(image, bbox[:2], bbox[2:], color=color)

    if pts is not None:
        pts = np.array(pts).reshape(-1, 2).astype(np.int32)
        for pt in pts:
            cv2.circle(image, pt, radius=2, color=color, thickness=-1)

    if label is not None:
        h, w = image.shape[:2]

        x1, y1 = bbox[:2] if bbox is not None else (5, h - 5)
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
