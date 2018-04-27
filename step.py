#!/usr/bin/python3
import _thread
import os

# Define a function for the thread
def run_simulation():
    os.system('py runner.py')
def run_visualization( ):
    os.system('py visualization2.py test')

# Create two threads as follows
try:
   _thread.start_new_thread(run_visualization() )
   _thread.start_new_thread(run_simulation())

except:
   print ("Error: unable to start thread")

while 1:
   pass