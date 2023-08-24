import cv2
import HandTrackingModule as htm
import numpy as np


#basic webcam access commend
cap = cv2.VideoCapture(0)

detector=htm.handDetector()

draw_color=(0,0,255)

img_canvas=np.zeros((720,1260,3),np.uint8) #3 means channels such as RGB

while True:

    sucess,img=cap.read()
    img=cv2.resize(img,(1260,720))

#draw color rectangle
    cv2.rectangle(img,(20,10),(230,100),(0,0,255),-5)
    cv2.rectangle(img,(250,10),(460,100),(0,255,0),-5)
    cv2.rectangle(img,(480,10),(690,100),(255,0,0),-5)
    cv2.rectangle(img,(710,10),(920,100),(0,255,255),-5)
    cv2.rectangle(img,(940,10),(1240,100),(255,255,255),-5)
    cv2.putText(img,text="ERASER",org=(1050,60),fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=1,color=(0,0,0))

#find hands and find land mark location
    lmlist=detector.findPosition(img)
    img=detector.findHands(img)
    print(lmlist)

    if len(lmlist)!=0:
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]

        #print(x1,y1)
        #print(x2,y2)

#check if finger is up
        fingers=detector.fingersUp()
        print(fingers)

#selection mode- index and middle finger is 

        if fingers[1] and fingers[2]:
            print('selection mode')

            xp,yp=0,0

            if y1<100:

                if 20<x1<230:
                    print("red")
                    draw_color=(0,0,255)

                elif 250<x1<460:
                    print("green")
                    draw_color=(0,255,0)

                elif 480<x1<690:
                    print("blue")
                    draw_color=(255,0,0)

                elif 710<x<920:
                    print("yellow")
                    draw_color=(0,255,255)

                elif 940<x1<1240:
                    print("eraser")
                    draw_color=(0,0,0)
                    
            cv2.rectangle(img,(x1,y1),(x2,y2),draw_color,cv2.FILLED)



#drawing mode - only index finger is up
       
        if fingers[1] and not fingers[2]:
            print('drawing mode')

            if xp==0 and yp==0:

                xp=x1
                yp=y1
            if draw_color==(0,0,0): 
               #eraser
               cv2.line(img_,(xp,yp),(x1,y1),color=draw_color,thickness=50)         #for webcam
               cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=50)   #for canvas
            else:
                 #drawing
                 cv2.line(img,(xp,yp),(x1,y1),color=draw_color,thickness=10)
                 cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=10)

            xp,yp=x1,y1

    #frame joing or image blanding
    img_gray=cv2.cvtColor(img_canvas,cv2.COLOR_RGBA2GRAY)             #convert gray scale
    _,img_inv=cv2.threshold(img_gray,20,255,cv2.THRESH_BINARY_INV)    #convert image gray to image inverse
    img_inv=cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR)                  #convert gray to RGB 
    
    img=cv2.bitwise_and(img,img_inv)       
    img=cv2.bitwise_or(img,img_canvas)

    img=cv2.addWeighted(img,1,img_canvas,0.5,0)  #means(img-frist img ,1-alpha value,img_canvas-frame,0-betta value)

    cv2.imshow('virtual painter',img)
    #cv2.imshow('canvas',img_canvas)

    if cv2.waitKey(1) & 0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()

