# Setup Guide – Smart AI Glass

This document describes the system setup required to run the Smart AI Glass project on a Raspberry Pi Zero W.

---

## System Requirements

- Raspberry Pi Zero W  
- Raspberry Pi OS (Lite or Desktop)  
- Python 3  

---

## Hardware Connections

### Touch Sensor

| Touch Sensor Pin | Raspberry Pi Pin |
|------------------|------------------|
| VCC              | 3.3V (Pin 1)     |
| GND              | GND (Pin 6)      |
| OUT              | GPIO 17 (Pin 11)|

The touch sensor output is expected to be **active HIGH**.

---

### Camera

- Connect the Raspberry Pi Camera Module to the CSI camera port
- Ensure the ribbon cable orientation is correct
- Enable the camera interface in Raspberry Pi configuration if required

---

### Audio Output

- Bluetooth earbuds **or**
- Wired speaker via 3.5 mm audio jack or USB sound card

---

## System Dependencies

Update the system and install required packages:

```bash
sudo apt update
sudo apt install -y \
  python3-pip \
  python3-picamera2 \
  espeak \
  libatlas-base-dev
