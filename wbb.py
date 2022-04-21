import win32gui
import time
import os
import PIL.ImageGrab
from datetime import datetime


def dump_logs(sf, logs):
    """
    Dumps the logs to a file.
    Try/except so you can open the file without crashing.
    """
    try:
        with open(sf, 'a', encoding="utf-8") as f:
            for l in logs:
                f.write(f"{l[0]};{l[1]}\n")
        return 1
    except Exception as e:
        print(f"Error saving logs: {e}")
        return 0


def dump_img(sf):
    """
    Dumps the screencap to a file.
    """
    img = PIL.ImageGrab.grab()
    img.save(f"{sf}{datetime.now().strftime('%H-%M-%S')}.png")


def main():
    # image save period in minutes
    img_save_period = 10
    # activity log period in minutes
    activity_save_period = 1

    # setup directory
    date = datetime.today().strftime('%Y%m%d')
    save_folder = f"activity/{date}/"
    save_folder_imgs = os.path.join(save_folder, "imgs/")
    save_file_logs = os.path.join(save_folder, "logs.csv")
    print(f"{save_folder=}")

    if not os.path.isdir(save_folder):
        os.mkdir(save_folder)
    if not os.path.isdir(save_folder_imgs):
        os.mkdir(save_folder_imgs)

    w=win32gui
    activity = []
    last_saved_img_time = time.time()
    while 1:
        time.sleep(60 * activity_save_period)
        name = w.GetWindowText (w.GetForegroundWindow())
        activity.append((datetime.now().strftime('%H-%M-%S'), name))

        # dump image 
        if time.time() - last_saved_img_time > 60 * img_save_period:
            last_saved_img_time = time.time()
            dump_img(save_folder_imgs)

        # save actvitiy after some has accumilated
        if len(activity) > 3:
            if dump_logs(save_file_logs, activity):
                activity = []


if __name__ == "__main__":
    main()
