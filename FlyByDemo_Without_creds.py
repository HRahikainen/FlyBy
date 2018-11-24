##
# Team FlyBy
# Junction 2018 Data economics track Poplatek's challenge Frictionless urban payments
#
# Demo runs on Raspberry Pi 3
# Peripherals:
#     - 3 Neopixel RGB LEDs
#     - RFID tag reader


import math
import requests
import json
import time
import os

import RPi.GPIO as GPIO
import SimpleMFRC522
import board
import neopixel
from pyfcm import FCMNotification
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

MSG_API_KEY = "<Your Server Key>"
REGISTR_ID = "<Device ID>"
USER1_ID = 358786870188  # Card id
USER2_ID = 167478543204  # Keyfob id
PRICE1 = 5
PRICE2 = 10
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    board.D18, 3, brightness=0.2, auto_write=False, pixel_order=ORDER)
reader = SimpleMFRC522.SimpleMFRC522()

previous_time = time.time()

# Back to black
pixels.fill((0, 0, 0))
pixels.show()
time.sleep(0.5)

# Use a service account
cred = credentials.Certificate('./serviceAccount.json')

firebase_admin.initialize_app(cred)

db = firestore.client()

def writeUser(username, userId, amount):
    doc_ref = db.collection(u'users').document(username)
    doc_ref.set({
        u'userID': userId,
        u'amount': amount
    })

writeUser("John Doe", USER1_ID, 1000)
writeUser("Jane Doe", USER2_ID, 500)
users_ref = db.collection(u'users')
docs = users_ref.get()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))


push_service = FCMNotification(api_key=MSG_API_KEY)

def push_transaction(userId, amount):
    """Send transaction information as push notifications to phone."""
    title = "New Transaction Update"
    body = "User ID: {0}\nAmount: {1}".format(userId, amount)
    data = {
        "userID": userId,
        "amount": amount
    }

    result = push_service.notify_single_device(
    registration_id=REGISTR_ID, message_title=title, message_body=body, data_message=data)

def text_transaction(userId, amount):
    """Send text message to user with 46Elks API."""
    auth = ("46ElksUserName", "46ElksPassword")
    msg = "New Transaction Update\nUser ID: {0}\nAmount: {1}".format(userId, amount)
    fields = {"from":"FlyByBox", "to":"phoneNumber", "message":msg}
    response = requests.post("https://api.46elks.com/a1/SMS", data=fields, auth=auth)

def dim(r, g, b, n):
    """Smooth LED dimming."""
    _r = 0
    _g = 0
    _b = 0

    for i in range(math.floor(n*50)):
        pixels.fill((_r, _g, _b))
        pixels[1] = (128, 128, 128)
        pixels.show()
        time.sleep(0.01)
        _r = math.floor(_r + r/(n*10))
        _g = math.floor(_g + g/(n*10))
        _b = math.floor(_b + b/(n*10))
        if (_r > r): _r = r
        if (_g > g): _g = g
        if (_b > b): _b = b

    _r = r
    _g = g
    _b = b

    pixels.fill((_r, _g, _b))
    pixels[1] = (128, 128, 128)
    pixels.show()
    time.sleep(0.1)

    for i in range(math.floor(n*50)):
        pixels.fill((_r, _g, _b))
        pixels[1] = (128, 128, 128)
        pixels.show()
        time.sleep(0.02)
        _r = math.floor(_r - r/(n*50))
        _g = math.floor(_g - g/(n*50))
        _b = math.floor(_b - b/(n*50))
        if (_r < 0): _r = 0
        if (_g < 0): _g = 0
        if (_b < 0): _b = 0


def blink(r, g, b, n, t):
    """ Blinks leds for n times with t delay. """
    for i in range(n):
        pixels.fill((r, g, b))
        pixels[1] = (128, 128, 128)
        pixels.show()
        time.sleep(t)
        pixels.fill((0, 0, 0))
        pixels[1] = (128, 128, 128)
        pixels.show()
        time.sleep(t)


blink(255, 0, 0, 3, 0.1)

# Main tag read-loop
while True:
    try:
        id, text = reader.read()
        # Get timestamp for debouncing of keyfob swipe
        current_time = time.time()

        if current_time - previous_time > 2:
            if id == USER1_ID:
                print("User with id {0} paid {1}".format(USER1_ID, PRICE1))
                push_transaction(USER1_ID, PRICE1)
                text_transaction(USER1_ID, PRICE1+PRICE2)
                dim(0, 255, 0, 1)

            elif id == USER2_ID:
                print("User with id {0} paid {1}".format(USER2_ID, PRICE2))
                push_transaction(USER2_ID, PRICE2)
                dim(0, 128, 255, 1)
            else:
                raise Exception("Unknown userID")

        previous_time = current_time
    except:
        # Flash NeoPixel three times for error.
        for i in range(3):
            blink(255, 0, 0, 0.5)

else:
    GPIO.cleanup()