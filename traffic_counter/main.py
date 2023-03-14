import cv2
from datetime import datetime
from traffic_counter import traffic_counter
import requests
from utils import average_calculator

#   How many times should we make decision about traffic before sending it to the server
NUMBER_OF_COUNTS_TO_MAKE_TRAFFIC_DECISION = 5
TRAFFIC_AVERAGE_COUNTS = {
    '0': 0,  # Green
    '1': 0,  # Yellow
    '2': 0,  # Red
}

SERVER_URL = 'http://localhost:5000/update-light-traffic/'

cap = cv2.VideoCapture("../video_samples/video_samples/road8.mp4")
kernel = None
object_detector = cv2.createBackgroundSubtractorMOG2(history=70, varThreshold=40, detectShadows=True)
previous_cars_count = 0
previous_time = datetime.now()
first_frame = True

decision_counter = 0

while 1:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape

    roi = frame[400:height, 0:width]  # region of interest

    # Object Detection
    mask = object_detector.apply(roi)

    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)  # Extract object shadows

    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detections = []  # present detected objects
    for cnt in contours:
        #  Calculate area and remove small elements
        area = cv2.contourArea(cnt)

        if area > 400:  # if area > 400pixels it is probably a vehicle

            x, y, w, h = cv2.boundingRect(cnt)  # get parameters of detected object (coords, width, height)

            if h > 30 and w > 30:
                detections.append([x, y, w, h])  # append params of object to array so we can draw it on screen later on

    present_cars_count = len(detections)  # get how many vehicles we have detected in present frame
    # print("Present", present_cars_count)
    # print("Past", previous_cars_count)
    took_count, traffic_result = traffic_counter(present_cars_count, previous_time, previous_cars_count, first_frame)

    if took_count:

        previous_time = datetime.now()
        # set previous count as the present count, so we can compare in the next frame
        previous_cars_count = present_cars_count

        TRAFFIC_AVERAGE_COUNTS[str(traffic_result)] += 1
        print(TRAFFIC_AVERAGE_COUNTS)
        decision_counter += 1
        #   if we have made as many decisions as we have specified… send traffic decision to the server
        #   and then decision_counter = 0

        if decision_counter == NUMBER_OF_COUNTS_TO_MAKE_TRAFFIC_DECISION:

            # Sends average traffic number to server
            post_data = {
                'traffic': average_calculator(TRAFFIC_AVERAGE_COUNTS)
            }
            # requests.post(SERVER_URL, post_data)  # This needs to become non-blocking later on!!!!
            print("FINAL RESULT", average_calculator(TRAFFIC_AVERAGE_COUNTS))
            decision_counter = 0
            TRAFFIC_AVERAGE_COUNTS = {'0': 0, '1': 0, '2': 0}

    # print("Detected Objects", len(detections))
    for detection in detections:
        x, y, w, h = detection
        # x = detection[0]
        # y = detection[1]
        # w = detection[2]
        # h = detection[3]
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(30)

    if key == 27:
        break
    first_frame = False
cap.release()
cv2.destroyAllWindows()
