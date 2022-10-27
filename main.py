from time import sleep
import os

WAIT_TIME = os.environ['WAIT_TIME']

while True:
    sleep(WAIT_TIME)
