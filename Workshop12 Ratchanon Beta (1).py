import cv2 as cv 
import requests 

camera = cv.VideoCapture(0) 
url = 'https://notify-api.line.me/api/notify'
token = 'hGiaE2lAQ5N8aO3L5FAPhSnj5jN28JLnSvTUBCPS7iM'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer ' + token 
}

msg = 'ตรวจพบความเคลื่อนไหวของกล้อง'

first_frame = None

while camera.isOpened():
    retry, frame = camera.read()
    
    if not retry:
        break

    if first_frame is None: # กำหนด first_frame 
        first_frame = frame
        continue

    difference = cv.absdiff(first_frame, frame)
    gray = cv.cvtColor(difference, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)#
    _, threshold = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dilation = cv.dilate(threshold, None, iterations=5)
    contours, _ = cv.findContours(dilation, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #cv.drawContours(screen1, contours, -1, (0, 255, 0),2)

    for movement in contours:
        if cv.contourArea(movement) < 8000:
            continue
        x, y, w, h = cv.boundingRect(movement)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        notify = requests.post(url, headers=headers, data={'message': msg}) 

    cv.imshow('pyCCTV ของPoomys', frame)

    if cv.waitKey(10) == ord('q'):
        break#หยุดการทำงานหากผู้ใช้กดปุ่ม 'q' 

camera.release() 
cv.destroyAllWindows()
