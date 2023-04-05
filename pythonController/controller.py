from datetime import datetime
import cv2
from traffic import traffic_count
from utils import average_calculator
import serial
import numpy as np
import httpx
import requests
import asyncio
import threading


GREEN_TIME_SECONDS = 20
ORANGE_TIME_SECONDS = 5
RED_TIME_SECONDS = 20

LAST_SECONDS_FOR_VEHICLE_DETECTION = 5
SECONDS_AFTER_GREEN_FOR_TRAFFIC_DECISION = 0
NUMBER_OF_COUNTS_TO_MAKE_TRAFFIC_DECISION = 5

ADDITIONAL_TIME_IN_CASE_OF_TRUCK = 10

kernel = None
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40, detectShadows=True)

ROTATIONS = {
    'green': {
        'duration': GREEN_TIME_SECONDS,
        'next': 'orange'
    },
    'orange': {
        'duration': ORANGE_TIME_SECONDS,
        'next': 'red'
    },
    'red': {
        'duration': RED_TIME_SECONDS,
        'next': 'green',
    },
}

arduino = serial.Serial('COM6', 9600, timeout=0.01, write_timeout=0.01)
arduino.flush()
arduino.reset_output_buffer()
arduino.reset_input_buffer()


net = cv2.dnn.readNet("cfg/yolo-fastest-1.1-xl.weights", "cfg/yolo-fastest-1.1-xl.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
# print(layer_names)
# print(net.getUnconnectedOutLayers())
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
font = cv2.FONT_HERSHEY_PLAIN


class TrafficLight:
    def __init__(self):
        self.prev_time = datetime.now()
        self.color = 'green'  # green/orange/red
        self.cap = cv2.VideoCapture('../video_samples/video_samples/traffic8.mp4')

        self.TRAFFIC_AVERAGE_COUNTS = {
            '0': 0,  # Green
            '1': 0,  # Yellow
            '2': 0,  # Red
        }

        # traffic counter specific variables....
        self.previous_cars_count = 0
        self.decision_made_for_traffic = 0
        self.prev_decision_time = datetime.now()
        self.additional_time = 0  # additional time for green light

        # Heavy vehicle approaching...
        self.truck_detected = False

        # Emergency vehicle approaching...
        self.emergency_vehicle = False

    def main(self):
        while 1:
            arduino.flush()
            arduino.reset_input_buffer()
            arduino.reset_output_buffer()
            ard_emerg_line = arduino.readline().decode("utf-8", "ignore").strip()
            if ard_emerg_line:
                # print(ard_emerg_line)
                self.emergency_vehicle = True
            #   Check if light is green and add additional_time for emergency to pass....
            ret, frame = self.cap.read()
            if not ret:
                return None

            height, width, _ = frame.shape

            roi = frame[500:height, 0:width]  # region of interest

            # Object Detection
            mask = object_detector.apply(roi)

            _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)  # Extract object shadows

            # mask = cv2.erode(mask, kernel, iterations=1)
            # mask = cv2.dilate(mask, kernel, iterations=2)


            self.change_color()         # Checks if traffic light should change
            self.traffic_check(mask)    # Checks for traffic
            if self.color == 'green' and not self.truck_detected and (datetime.now() - self.prev_time).seconds >= GREEN_TIME_SECONDS - LAST_SECONDS_FOR_VEHICLE_DETECTION:
                truck_in_frame, frame = self.check_for_heavy_vehicle(frame)
                if truck_in_frame and not self.truck_detected:
                    self.truck_detected = True
                    self.additional_time = ADDITIONAL_TIME_IN_CASE_OF_TRUCK

            # cv2.imshow('mask', mask)
            cv2.imshow("Frame", frame)
            # cv2.imshow("Mask", mask)
            key = cv2.waitKey(30)



    def change_color(self):
        time_now = datetime.now()

        # if emergency vehicle is approaching don't change green light
        if self.color == 'green' and self.emergency_vehicle:
            return

        if not (time_now - self.prev_time).seconds - self.additional_time >= ROTATIONS[self.color]['duration']:
            return False

        self.prev_time = time_now
        self.color = ROTATIONS[self.color]['next']
        print('Changed traffic light color to:', self.color)
        arduino.write(bytes(self.color+'\n', 'utf-8'))
        arduino.flush()
        arduino.reset_output_buffer()
        arduino.reset_input_buffer()

        self.TRAFFIC_AVERAGE_COUNTS = {'0': 0, '1': 0, '2': 0}
        self.decision_made_for_traffic = 0

        self.truck_detected = False
        self.additional_time = 0

        if self.color == 'green':
            self.prev_decision_time = datetime.now()
        return True


    def traffic_check(self, mask):
        if self.color == 'green':
            if self.decision_made_for_traffic == NUMBER_OF_COUNTS_TO_MAKE_TRAFFIC_DECISION:
                average_traffic = average_calculator(self.TRAFFIC_AVERAGE_COUNTS)
                print("DECISION MADE", average_traffic)
                threading.Thread(target=self.update_db_traffic_state, args=[average_traffic]).start()

                # HERE WE SHOULD MAKE AN HTTP POST REQUEST TO THE SERVER
                # IT SHOULD BE ASYNC, OTHERWISE THE VIDEO PAUSES UNTIL POST REQUEST IS FINISHED

                # {
                #  id: objectID, (mongoDB objectID)
                #  traffic_decision: int
                # }



                self.TRAFFIC_AVERAGE_COUNTS = {'0': 0, '1': 0, '2': 0}
                self.decision_made_for_traffic = 0
            self.previous_cars_count, traffic_decision = traffic_count(mask, self.prev_decision_time,
                                                                       self.previous_cars_count)
            if traffic_decision is not None:  # this checks if we actually took a decision
                self.prev_decision_time = datetime.now()
                self.TRAFFIC_AVERAGE_COUNTS[str(traffic_decision)] += 1
                self.decision_made_for_traffic += 1

    def check_for_heavy_vehicle(self, frame):
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                # print(class_id)
                confidence = scores[class_id]
                if confidence > 0.2:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)

        truck_in_frame = False
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                # print(classes)
                label = str(classes[class_ids[i]])
                # print(label)
                confidence = confidences[i]
                color = colors[class_ids[i]]
                if label == 'bus' or label == 'truck' or label == 'train':
                    truck_in_frame = True
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 3)
        return truck_in_frame, frame


    def update_db_traffic_state(self, average_traffic):
        requests.get("https://www.google.com")
        print("Made request")
light = TrafficLight()
light.main()
