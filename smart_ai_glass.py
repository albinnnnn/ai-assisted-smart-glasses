# smart_ai_glass.py
import time
import cv2
import easyocr
import pyttsx3
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import subprocess

# ==========================
# CONFIGURATION
# ==========================
TOUCH_PIN = 17
OCR_CONFIDENCE_THRESHOLD = 0.45

# Optional: auto-connect Bluetooth device
BT_DEVICE_MAC = None  # Set to MAC address or leave as None


# ==========================
# BLUETOOTH (OPTIONAL)
# ==========================
def connect_bluetooth():
    if not BT_DEVICE_MAC:
        return

    try:
        subprocess.run(
            ["bluetoothctl", "connect", BT_DEVICE_MAC],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        time.sleep(2)
    except subprocess.CalledProcessError:
        pass


# ==========================
# GPIO SETUP
# ==========================
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ==========================
# CAMERA SETUP
# ==========================
camera = Picamera2()
camera.configure(
    camera.create_still_configuration(
        main={"size": (640, 480)}
    )
)
camera.start()

# ==========================
# OCR SETUP
# ==========================
reader = easyocr.Reader(
    ['en'],
    gpu=False,
    quantize=True
)

# ==========================
# TTS SETUP
# ==========================
connect_bluetooth()

engine = pyttsx3.init()
engine.setProperty('rate', 145)

# ==========================
# STATE VARIABLES
# ==========================
ocr_active = True
last_touch_state = False

# ==========================
# FUNCTIONS
# ==========================
def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=1.2, fy=1.2)
    return gray


def run_ocr(img):
    results = reader.readtext(img)
    text = " ".join(
        t for (_, t, c) in results if c > OCR_CONFIDENCE_THRESHOLD
    )
    return text


def speak(text):
    if not text.strip():
        return
    engine.say(text)
    engine.runAndWait()


# ==========================
# MAIN LOOP
# ==========================
print("Smart AI Glass running")
print("Tap: Pause / Resume OCR")
print("Hold: Capture and read text")

try:
    while True:
        touch_state = GPIO.input(TOUCH_PIN)

        # Detect tap (edge)
        if touch_state and not last_touch_state:
            ocr_active = not ocr_active
            time.sleep(0.3)  # debounce

        last_touch_state = touch_state

        # OCR only while held
        if ocr_active and touch_state:
            frame = camera.capture_array()
            frame = preprocess(frame)

            text = run_ocr(frame)
            speak(text)

            time.sleep(1)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    camera.stop()
    GPIO.cleanup()
