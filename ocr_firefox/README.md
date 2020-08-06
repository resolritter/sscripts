# Before running

Install the dependencies with Poetry

```
  pip install -r requirements.txt
```

# Requirements

- Linux
- Firefox
- xdotool
- Have Tesseract installed

  - ```
     > pacman -Qs tesseract
    local/python-pytesseract 0.3.2-2
        A Python wrapper for Google Tesseract
    local/tesseract 4.1.1-2
        An OCR program
    ```

- Have OpenCV installed

  - ```
     > pacman -Qs cv
    local/opencv 4.3.0-7
        Open Source Computer Vision Library

    ```

- GDK Pixbuf and GTK

  - ```
     > pacman -Qs gdk
    local/gdk-pixbuf2 2.40.0-2
        An image loading library
    local/gtk2 2.24.32-2
        GObject-based multi-platform GUI toolkit (legacy)
    local/gtk3 1:3.24.21-1
        GObject-based multi-platform GUI toolkit

    ```

# How it works

Firefox has a "Take a screenshot" functionality which is able to detect boxes of
text. The idea is to leverage this by

- Emulating user input using `xdotool`, for taking the screenshot
- Post-process the screenshot using OpenCV for improving Tesseract's accuracy
- Using Tesseract for capturing the text contents from the screenshot
