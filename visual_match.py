from PIL import Image
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def apply_mask(piece):
    # Create a mask
    blur = cv.bilateralFilter(piece, 20, 75, 20)
    _, thresh = cv.threshold(piece, 140, 255, cv.THRESH_BINARY_INV)

    return cv.bitwise_and(piece, piece, mask=thresh)

def match(piece, whole):
    piece, whole = np.fromfile(piece, np.uint8), np.fromfile(whole, np.uint8)
    piece, whole = cv.imdecode(piece, cv.IMREAD_GRAYSCALE), cv.imdecode(whole, cv.IMREAD_GRAYSCALE)

    # apply a mask to the puzzle piece
    piece = apply_mask(piece)

    sift = cv.SIFT_create()

    kp1, des1 = sift.detectAndCompute(piece,None)
    kp2, des2 = sift.detectAndCompute(whole,None)

    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m,n in matches:
        if m.distance < .75 * n.distance:
            good.append([m])

    img3 = cv.drawMatchesKnn(piece,kp1,whole,kp2,good,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    return img3