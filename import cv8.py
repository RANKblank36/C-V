import cv2 
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    mask  = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.dilate(mask, np.ones((3, 3,), np.uint8), iterations=1)
    1
    result = cv2.bitwise_and(frame, frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        max_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(max_contour) > 500:
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            center_x = int(x + w / 2)
            center_y = int(y + h / 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Filtered Frame', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()