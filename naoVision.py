#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys,pickle,time,cv2,openface
import numpy as np
from sklearn.mixture import GMM
def faceRecon(motion):
    pics = motion.takePic()
    cv2.imwrite("./pics/pic.jpg", pics)
    imgs = ['./pics/pic.jpg']
    name = infer(imgs)
    print name
    motion.say(name)



def getRep(imgPath, multiple=False):
    align = openface.AlignDlib('./face/models/dlib/shape_predictor_68_face_landmarks.dat')
    net = openface.TorchNeuralNet('./face/models/openface/nn4.small2.v1.t7', imgDim=96)
    start = time.time()
    bgrImg = cv2.imread(imgPath)
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format(imgPath))

    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    # if args.verbose:
    #     print("  + Original size: {}".format(rgbImg.shape))
    # if args.verbose:
    #     print("Loading the image took {} seconds.".format(time.time() - start))

    start = time.time()

    if multiple:
        bbs = align.getAllFaceBoundingBoxes(rgbImg)
    else:
        bb1 = align.getLargestFaceBoundingBox(rgbImg)
        bbs = [bb1]
    if len(bbs) == 0 or (not multiple and bb1 is None):
        print ("Unable to find a face: {}".format(imgPath))
        return None
    # if args.verbose:
    #     print("Face detection took {} seconds.".format(time.time() - start))

    reps = []
    for bb in bbs:
        start = time.time()
        alignedFace = align.align(
            96,
            rgbImg,
            bb,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            raise Exception("Unable to align image: {}".format(imgPath))
        # if args.verbose:
        #     print("Alignment took {} seconds.".format(time.time() - start))
        #     print("This bbox is centered at {}, {}".format(bb.center().x, bb.center().y))

        start = time.time()
        rep = net.forward(alignedFace)
        # if args.verbose:
        #     print("Neural network forward pass took {} seconds.".format(time.time() - start))
        reps.append((bb.center().x, rep))
    sreps = sorted(reps, key=lambda x: x[0])
    return sreps


def infer( imgs , multiple=False):
    with open('./face/generated-embeddings/classifier.pkl', 'rb') as f:
        if sys.version_info[0] < 3:
                (le, clf) = pickle.load(f)
        else:
                (le, clf) = pickle.load(f, encoding='latin1')

    for img in imgs:
        print("\n=== {} ===".format(img))
        reps = getRep(img, multiple)
        if reps is None:
            return u"未识别出人脸"
        if len(reps) > 1:
            print("List of faces in image from left to right")
        for r in reps:
            rep = r[1].reshape(1, -1)
            bbx = r[0]
            start = time.time()
            predictions = clf.predict_proba(rep).ravel()
            maxI = np.argmax(predictions)
            person = le.inverse_transform(maxI)
            confidence = predictions[maxI]
            # if args.verbose:
            #     print("Prediction took {} seconds.".format(time.time() - start))
            if multiple:
                print("Predict {} @ x={} with {:.2f} confidence.".format(person.decode('utf-8'), bbx,
                                                                         confidence))
            else:
                print("Predict {} with {:.2f} confidence.".format(person.decode('utf-8'), confidence))
            if isinstance(clf, GMM):
                dist = np.linalg.norm(rep - clf.means_[maxI])
                print("  + Distance from the mean: {}".format(dist))
            return person.decode('utf8')