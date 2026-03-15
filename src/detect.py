import cv2
import numpy as np

MIN_AREA = 600
AR_MIN, AR_MAX = 2.0, 8.0

def find_plate_candidates(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    edges = cv2.Canny(blur,100,200)

    contours,_ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    candidates = []

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < MIN_AREA:
            continue

        rect = cv2.minAreaRect(cnt)

        (_, _), (w,h), _ = rect

        if w <= 0 or h <= 0:
            continue

        ar = max(w,h) / max(1.0,min(w,h))

        if AR_MIN <= ar <= AR_MAX:
            candidates.append(rect)

    return candidates


def main():

    cap = cv2.VideoCapture(0)

    while True:

        ok, frame = cap.read()

        if not ok:
            break

        vis = frame.copy()

        candidates = find_plate_candidates(frame)

        if candidates:

            for rect in candidates:

                box = cv2.boxPoints(rect).astype(int)

                cv2.polylines(vis,[box],True,(0,255,0),2)

        cv2.imshow("Plate Detection",vis)

        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()