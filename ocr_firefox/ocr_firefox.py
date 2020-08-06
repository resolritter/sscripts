#!/usr/bin/python3
import cv2
import numpy as np
import pytesseract
import gi
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

if __name__ == "__main__":
    try:
        # Triggers screenshot action on Firefox
        # - Right click brings the context menu (xdotool click 3)
        # - Presses "T" to **T**ake a screenshot (xdotool key T)
        # - Waits for the screenshot UI to come up (sleep 0.2s)
        # - Nudges the cursor just a little bit, so that the area under it is captured (mousemove_relative)
        # - Clicks to take a screenshot (click 1)
        # - Waits for the selected area UI to come up (sleep 0.2s)
        # - Copies the screenshot to the system's clipboard (xdotool key ctrl+c)
        subprocess.run(
            "xdotool click 3; xdotool key T; sleep 0.2s; xdotool mousemove_relative 1 0 click 1; sleep 0.5s; xdotool key ctrl+c;",
            shell=True,
        )

        pixbuf = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).wait_for_image()
        w = pixbuf.get_width()
        h = pixbuf.get_height()
        data = pixbuf.read_pixel_bytes().get_data()
        #                       png image so R, G, B, A = 4
        img = np.frombuffer(data, np.uint8).reshape(h, w, 4)

        # push the pixel's colors to either black or white (notice cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(
            cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1]
        )

        # puts the text into the clipboard
        p1 = subprocess.Popen(
            ["xclip", "-selection", "clipboard", "-f"], stdin=subprocess.PIPE
        )
        p1.communicate(input=(text.encode()))
    except:
        exit(0)
