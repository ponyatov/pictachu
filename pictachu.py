# control keys
KEY_EXIT=27 # esc
KEY_CALIBRATE=241 # 99 # c
KEY_GRAB=239 # g
KEY_FLIP=32 # space

CFG_WIDTH =320#1024#640#320
CFG_HEIGHT=240# 768#480#240
CFG_WIDTH =640#320
CFG_HEIGHT=480#240
CFG_WIDTH =800#320
CFG_HEIGHT=600#240
##CFG_WIDTH =1024#640#320
##CFG_HEIGHT=768#480#240

import cv,numpy as np,time

# windows pool
wnWebCam='webcam'
##wnAffine='affine'
wnGrab='grab'
wnFlip='flip'

# open windows
cv.NamedWindow(wnWebCam,cv.CV_WINDOW_AUTOSIZE)
##cv.NamedWindow(wnAffine,cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow(wnGrab,cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow(wnFlip,cv.CV_WINDOW_AUTOSIZE)

# open camera
cam=cv.CaptureFromCAM(-1)
cv.SetCaptureProperty(cam,cv.CV_CAP_PROP_FRAME_WIDTH,CFG_WIDTH)
cv.SetCaptureProperty(cam,cv.CV_CAP_PROP_FRAME_HEIGHT,CFG_HEIGHT)
CAM_CALIBRATE_DATA=[[1,2],[3,4],[5,6]]
CAM_AFFINE_DATA   =[(CFG_WIDTH,CFG_HEIGHT),(0,CFG_HEIGHT),(0,0)]
CAM_AFFINE_MATRIX=cv.fromarray(np.array(((.1,1.,1.),(1.,1.,0.))))

# mouse procesing
CALIBRATE=3
def onMouse(e,x,y,f,p):
    global CALIBRATE,CAM_CALIBRATE_DATA,CAM_AFFINE_MATRIX
    if CALIBRATE and e == cv.CV_EVENT_LBUTTONDOWN:
        CALIBRATE-=1
        print 'CAL',CALIBRATE,'e',e,'x',x,'y',y,'f',f,'p',p
        CAM_CALIBRATE_DATA[CALIBRATE]=(x,y)
        if CALIBRATE==0:
            print 'cal done'
            cv.GetAffineTransform(CAM_CALIBRATE_DATA,CAM_AFFINE_DATA,CAM_AFFINE_MATRIX)
cv.SetMouseCallback(wnWebCam,onMouse,wnWebCam)

# buffers
A=cv.CreateImage((CFG_WIDTH,CFG_HEIGHT),8,3)
print 'A',A,'w',A.width,'h',A.height,'ch',A.channels,'d',A.depth
J=cv.LoadImage('grab.jpg',True)
print 'J',J,'w',J.width,'h',J.height,'ch',J.channels,'d',J.depth
G=cv.CloneImage(A)
cv.Resize(J,G)
cv.ShowImage(wnGrab,G)
print 'G',G,'w',G.width,'h',G.height,'ch',G.channels,'d',G.depth
F=cv.QueryFrame(cam)
print 'F',F,'w',F.width,'h',F.height,'ch',F.channels,'d',F.depth
FLIP=True
DO_FLIP=False

# main loop
while True:
    # process kbd control
    key=cv.WaitKey(10)
    if key == -1: pass
    elif key == KEY_EXIT: break
    elif key == KEY_CALIBRATE: CALIBRATE=3
    elif key == KEY_GRAB:
        G=cv.CloneImage(A)
        cv.ShowImage(wnGrab,G)
    elif key == KEY_FLIP: DO_FLIP=10
    else:
        print key
        break
    # grab frame from cam
    F=cv.QueryFrame(cam)
    # process cam calibrated converter
    cv.WarpAffine(F,A,CAM_AFFINE_MATRIX)
    # update windows
    cv.ShowImage(wnWebCam,F)
    FLIP=not FLIP
    if FLIP and DO_FLIP:
        cv.ShowImage(wnFlip,G)
        DO_FLIP-=1
    else:
        cv.ShowImage(wnFlip,A)

# release resources
del cam
del A,F,G
cv.DestroyAllWindows()

## mudules
##import os,sys,time,cv
##
### configuration
##
##CFG_WIDTH =320#1024#640#320
##CFG_HEIGHT=240# 768#480#240
####CFG_WIDTH =640#320
####CFG_HEIGHT=480#240
####CFG_WIDTH =800#320
####CFG_HEIGHT=600#240
##VIDEO_CODEC=cv.CV_FOURCC('X','V','I','D')
##VIDEO_FPS=8
##SAVE_AVI=False
####SAVE_AVI=True
##
##KEY_DELTA='d'.zfill
##KEY_GRAB=103 # g
##KEY_FLIP=102 # f
##
### windows pool
##wnMain=sys.argv[0]
##wnGrab='grab'
##wnDelta='delta'
##wnFlip='flip'
##wnAffine='affine'
##
### create openCV windows
####cv.NamedWindow(wnMain,cv.CV_WINDOW_AUTOSIZE)
##cv.NamedWindow(wnGrab,cv.CV_WINDOW_AUTOSIZE)
##cv.NamedWindow(wnDelta,cv.CV_WINDOW_AUTOSIZE)
##cv.NamedWindow(wnFlip,cv.CV_WINDOW_AUTOSIZE)
##cv.NamedWindow(wnAffine,cv.CV_WINDOW_AUTOSIZE)
##
### connect to webcam
##print capture,cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH),cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT)
##print capture,cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH),cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT)
##
### avi rec sample
##avi=cv.CreateVideoWriter('avi.avi',VIDEO_CODEC,VIDEO_FPS,(CFG_WIDTH,CFG_HEIGHT),True)
##
##### callbacks for main window controls
####R_correction=50
####G_correction=50
####B_correction=50
####def chng_R_correction(val):
####    R_correction=val
####def chng_G_correction(val):
####    G_correction=val
####def chng_B_correction(val):
####    B_correction=val
####
##### main window controls
####cv.CreateTrackbar('R',wnMain,R_correction,100,chng_R_correction)
####cv.CreateTrackbar('G',wnMain,G_correction,100,chng_G_correction)
####cv.CreateTrackbar('B',wnMain,B_correction,100,chng_B_correction)
##
### source image
##SRC=cv.QueryFrame(capture)
##AFN=cv.QueryFrame(capture)
### flip flag
##FLIP=True
##
##
##
### main loop
##while True:
##    # query frame from webcam
##    captured=cv.QueryFrame(capture)
##    # update webcam window
##    cv.ShowImage(wnWebCam,captured)
##    # do affine warp
##    cv.WarpAffine(captured,AFN,AFN_MATRIX)
##    cv.ShowImage(wnAffine,AFN)
##    # update flip window
##    if FLIP:
##        cv.ShowImage(wnFlip,captured)
##    else:
##        cv.ShowImage(wnFlip,SRC)
##    # dump to avi
##    if SAVE_AVI: cv.WriteFrame(avi,captured)
##    # get control key
##    cmdkey=cv.WaitKey(1)
##    if cmdkey == KEY_EXIT:
##        # exit program
##        break
##    elif cmdkey == KEY_GRAB:
##        # update grabbed window
##        SRC=cv.CloneImage(captured)
##        cv.ShowImage(wnGrab,SRC)
##        # save to file
##        cv.SaveImage('%.4i%.2i%.2i%.2i%.2i%.2i.png'%time.localtime()[:6],SRC)
##    elif cmdkey == KEY_FLIP:
##        FLIP=not FLIP
##    FLIP=not FLIP
##
##del capture
##del avi
