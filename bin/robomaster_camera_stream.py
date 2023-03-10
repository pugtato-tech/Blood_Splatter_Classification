import cv2
import robomaster.exceptions
from robomaster import robot
from robomaster import chassis

retry_time = 0.5

def send_command(command, *args, **kwargs):
    try:
        command(*args, **kwargs)
    except Exception as e:
        if "Robot is already performing" in str(e):
            print("Maxed out command limit!")


def ipgrab():

    if __name__ == '__main__':
        ep_robot = robot.Robot()

        ep_robot.initialize(conn_type='ap', proto_type="udp")

        version = ep_robot.get_version()
        print("Robot version: {0}".format(version))
        ep_robot.close()

def stream_robomaster_video():
    ep_robot = robot.Robot()
    move_speed = 2.0

    try:

        ep_robot.initialize(conn_type="ap", proto_type="udp")

        ep_chassis = ep_robot.chassis
        ep_camera = ep_robot.camera

        ep_camera.start_video_stream(display=False)

        while True:
            img = ep_camera.read_cv2_image()
            img = cv2.resize(img, (600, 400))

            cv2.imshow("Camera Stream", img)
            key = cv2.waitKey(1)

            if key in {27, 113}:
                break

            if key in {97, 17}:
                print("Left")
                send_command(ep_chassis.move, y=-1, xy_speed=move_speed)
                print("HELP")
            elif key in {100, 16}:
                print("Right")
                send_command(ep_chassis.move, y=1, xy_speed=move_speed)
                print("HELP")
            if key in {119, 30}:
                print("Forward")
                send_command(ep_chassis.move, x=1, xy_speed=move_speed)
                print("HELP")
            elif key in {115, 31}:
                print("Backwards")
                send_command(ep_chassis.move, x=-1, xy_speed=move_speed)
                print("HELP")

            batch += 1

    except Exception as e:
        print(f"Main Loop Error: {e}")

    finally:
        cv2.destroyAllWindows()

        ep_robot.close()

if __name__ == "__main__":
    # ipgrab()
    stream_robomaster_video()

