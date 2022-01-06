from PIL import Image
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def match(piece, whole):
    piece, whole = np.fromfile(piece, np.uint8), np.fromfile(whole, np.uint8)
    piece, whole = cv.imdecode(piece, cv.IMREAD_GRAYSCALE), cv.imdecode(whole, cv.IMREAD_GRAYSCALE)

    #resize the 

    sift = cv.SIFT_create()

    kp1, des1 = sift.detectAndCompute(piece,None)
    kp2, des2 = sift.detectAndCompute(whole,None)

    """
    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m,n in matches:
        if m.distance < .75 * n.distance:
            good.append([m])

    img3 = cv.drawMatchesKnn(piece,kp1,whole,kp2,good,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    """

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in range(len(matches))]
    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]
    draw_params = dict(matchColor = (0,255,0),
                    singlePointColor = (255,0,0),
                    matchesMask = matchesMask,
                    flags = cv.DrawMatchesFlags_DEFAULT)
    img3 = cv.drawMatchesKnn(piece,kp1,whole,kp2,matches,None,**draw_params)

    return img3