# -*- coding: utf-8 -*-
from naoqi import ALProxy
import numpy,time,ftplib,globalVar
import vision_definitions


class Motion:
    #constructor
    def __init__(self,ip = 'nao.local',port  = 9559):
        try:
            self.ftp = ftplib.FTP(ip)
            self.ftp.login("nao","nao")
        except Exception, e:
            print "Error when create FTP connection"
        try:
            self.motionProxy = ALProxy('ALMotion',ip,port)
            self.camProxy = ALProxy('ALVideoDevice',ip,port)
            self.tts = ALProxy("ALTextToSpeech",ip,port)
            self.audioDevice = ALProxy('ALAudioDevice',ip,port)
            self.record = ALProxy('ALAudioRecorder',ip,port)
            resolution = vision_definitions.kVGA
            colorSpace = vision_definitions.kRGBColorSpace
            self.fps = 15
            self.videoClient = self.camProxy.subscribeCamera('python_client', 0, resolution, colorSpace, self.fps)
            # print self.videoClient
            # in case of camera subscribe overflow
            assert self.videoClient is not None
        except Exception, e:
            print "Error when creating ALPhotoCapture proxy:"
            print str(e)
            exit(1)

    def __del__(self):
        self.camProxy.unsubscribe(self.videoClient)
        self.camProxy.setAllParametersToDefault(0)
        self.motionProxy.rest()
    #
    def move(self,x,y):
        pass

    #take pictures
    def takePic(self):
        print "take picture!"
        naoImage = self.camProxy.getImageRemote(self.videoClient)
        assert naoImage is not None
        # print naoImage
        width = naoImage[0]
        height = naoImage[1]
        nchanels = naoImage[2]
        array = naoImage[6]
        return self.__str2array(array, (height, width, nchanels))

    def __str2array(self, string, shape):
        assert len(string) == shape[0] * shape[1] * shape[2], len(shape) == 3
        image = numpy.zeros(shape, numpy.uint8)
        for i in range(0, shape[0]):
            p1 = i * shape[1] * shape[2]
            for j in range(0, shape[1]):
                p2 = j * shape[2]
                for c in range(0, shape[2]):
                    p3 = shape[2] - c - 1
                    image[i, j, c] = ord(string[p1 + p2 + p3])
        return image

    #record sound
    def recordSound(self,filename,filePath):
        print 'start recording'
        self.record.startMicrophonesRecording("/home/nao/"+str(filename), 'wav', 16000, (0,0,1,0))
        time.sleep(globalVar.REC_LENGTH)
        self.record.stopMicrophonesRecording()
        print 'end recording'
        self.__getfile(filename,filePath)

    # ftp 获取音频
    def __getfile(self,filename,filepath):
        f = open(filepath,"wb")
        self.ftp.retrbinary("RETR %s" % filename,f.write,8192)
        f.close()


    def getfile(self):
        pass
    #show poses
    def pose(self,mode):
        pass

    def dance(self):
        pass

    def say(self,string):
        # string  = "1+1 = 2"
        self.tts.say(string.encode("utf8"))

    # for switch robot functions: face reconginition, chat(ask question?, follow instructions
    def touchHand(self):
        pass

    # for chat with robot and give orders
    # voice recording lasts only (5) seconds ( for now )
    def touchHead(self):
        pass




