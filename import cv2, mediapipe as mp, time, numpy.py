import cv2, mediapipe as mp, time, numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

FILTERS = [None, 'GRAYSCALE', 'SEPIA', 'NEGATIVE', 'BLUR']
current_filter = 0

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the webcam."); exit()

last_action_time = 0; DEBOUNCE_TIME = 1
pinch_in_progress = False; capture_request = False

def apply_filter(frame, ftype):
    """Apply the specified filter to the frame."""
    if ftype == 'GRAYSCALE':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif ftype == 'SEPIA':
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        return np.clip(cv2.transform(frame, sepia_filter), 0, 255).astype(np.uint8)
    elif ftype == 'NEGATIVE':
        return cv2.bitwise_not(frame)
    elif ftype == 'BLUR':
        return cv2.GaussianBlur(frame, (15, 15), 0)
    return frame

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read frame."); break
    img = cv2.flip(img, 1)
    h, w = img.shape[:2]
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    capture_request = False

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
            lm = hand.landmark

            tips = {name: (int(lm[idx].x * w), int(lm[idx].y * h))
                    for name, idx in {
                        'thumb': mp_hands.HandLandmark.THUMB_TIP,
                        'index': mp_hands.HandLandmark.INDEX_FINGER_TIP,
                        'middle': mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                        'ring': mp_hands.HandLandmark.RING_FINGER_TIP,
                        'pinky': mp_hands.HandLandmark.PINKY_TIP
                    }.items()}

            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
            for i, (name, (x, y)) in enumerate(tips.items()):
                cv2.circle(img, (x, y), 10, colors[i], cv2.FILLED)

            thumb_x, thumb_y = tips['thumb']
            index_x, index_y = tips['index']
            current_time = time.time()

            pinch = abs(thumb_x - index_x) < 30 and abs(thumb_y - index_y) < 30
            if pinch and not pinch_in_progress:
                pinch_in_progress = True; capture_request = True
            if not pinch and pinch_in_progress:
                pinch_in_progress = False

            elif any(abs(thumb_x - tips[finger][0]) < 30 and abs(thumb_y - tips[finger][1]) < 30
                     for finger in ['middle', 'ring', 'pinky']):
                if current_time - last_action_time > DEBOUNCE_TIME:
                    current_filter = (current_filter + 1) % len(FILTERS)
                    last_action_time = current_time
                    print("Filter changed to:", FILTERS[current_filter] or "None")
            break  

    filtered_img = apply_filter(img, FILTERS[current_filter])
    display_img = cv2.cvtColor(filtered_img, cv2.COLOR_GRAY2BGR) if FILTERS[current_filter]=='GRAYSCALE' else filtered_img

    if capture_request:
        cv2.putText(display_img, "Picture Captured!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        ts = int(time.time())
        cv2.imwrite(f"picture_{ts}.jpg", display_img)
        print(f"Saved: picture_{ts}.jpg")

    cv2.imshow("Gesture-Controlled Photo App", display_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release(); cv2.destroyAllWindows()

