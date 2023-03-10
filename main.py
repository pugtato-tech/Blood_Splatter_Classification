from blob_utils import *
from robomaster import robot, chassis, camera
from tkinter import filedialog, Tk

from datetime import datetime, date
from pdf_utils import PDF
import sys
from time import sleep
import cv2


# Add Driver Code Here
def main():
    # Initialize Variables
    detector = generate_aruco_detector(cv2.aruco.DICT_7X7_100)

    # Initialize Robomaster UDP Stream
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap", proto_type="udp")
    ep_chassis = ep_robot.chassis
    ep_camera = ep_robot.camera
    ep_camera.start_video_stream(display=True)

    # Construct PDF Object
    pdf = PDF(logo="static/images/logo.jpg")

    # Ask For Credentials
    name = input("Enter your operator title >>> ")
    site = input("Enter the name of the site >>> ")
    date = date.strftime(datetime.now(), "%m/%d/%Y")

    # Construct Title Page
    pdf.createTitlePage(site, date, name)

    while True:
        # Ask For Input
        input("Hit Enter To Begin Blood Splatter Analysis")

        while True:
            # Detect Aruco Code + Ratio
            frame = ep_camera.read_cv2_image()

            frame = cv2.GaussianBlur(frame, (5, 5), 0)
            detected, aruco_id, ratio  = aruco_ratio(frame, detector, 100)

            # Signal aruco code detection
            if detected:
                break
            else:
                # Make not detected sound here
                # robot.ep_robot.
                pass

            sleep(1.0)

        # Run detection algorithm
        pdf.generateSplatterAnalysis(ratio, aruco_id, frame, crop=False)


        repeat = input("Run again? (y/n) >>> ").lower()
        if repeat not in {"y", "yes"}:
            break
        else:
            ep_chassis.move(y=(800 / 1000), xy_speed=0.4)
            sleep(5)
            pass

    # Open File Dialog And Grab Path
    root = Tk()
    root.withdraw()
    path = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension=".pdf")

    if path != []:
        pdf.path = path

    # Save Completed PDF (Will Be In Reports Folder)
    pdf.save()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    quit()