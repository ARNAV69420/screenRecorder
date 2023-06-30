import os
import sys
import signal
import time
import threading
import subprocess


def capture_screenshots():
    # Create the screenshots directory if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # Start the screenshot capture process using ffmpeg
    subprocess.run(["ffmpeg", "-f", "x11grab", "-r", "60", "-i", ":0.0", "-frames", "100000000",
                    "screenshots/screenshot_%04d.png"], check=True)


def create_video(fps):
    # Get the current date and time for the video filename
    timestamp = time.strftime('%Y-%m-%d-%H-%M-%S')

    # Run ffmpeg to create the video from the screenshots
    subprocess.run(["ffmpeg", "-framerate", str(fps), "-pattern_type", "glob", "-i", "screenshots/*.png",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", f"screen_cap_{timestamp}.mp4"], check=True)

    # Remove the captured screenshots
    subprocess.run(["rm", "-r", "screenshots"], check=True)


def signal_handler(signal, frame):
    create_video(fps)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python screenshot_capture.py <fps>")
        sys.exit(1)

    try:
        fps = int(sys.argv[1])
        if fps <= 0:
            raise ValueError
    except ValueError:
        print("Invalid FPS value. Please provide a positive integer.")
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)

    # Launch a separate thread for capturing screenshots
    capture_thread = threading.Thread(target=capture_screenshots)
    capture_thread.start()

    # Keep the main thread running to handle the keyboard interrupt
    while True:
        time.sleep(1)

