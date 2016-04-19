import pycurl, json
import io
import argparse
import re
from bs4 import BeautifulSoup
import requests
import RPi.GPIO as GPIO
import time
import socket
import tweepy
import subprocess

def main():
  #setting the Board
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(18, GPIO.IN, GPIO.PUD_UP)

  # Check the connection
  while is_disconnected('www.google.com'):
    time.sleep(5)

  # Main loop
  while True:
    try:
      waitButton() 
    except:
      detect_dongle(10)

def detect_dongle(wait_time):
  call = subprocess.check_output('lsusb')
  if 'Broadcom' not in str(call):
    print('Restarting after {} seconds'.format(wait_time))
    time.sleep(wait_time)
    command= '/usr/bin/sudo /sbin/shutdown now'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate[0]
    print(output)

def is_disconnected(REMOTE_SERVER):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return False 
    # No connection so the result is False
  except:
     return True



def sendMessage(message, user):

  # Send a private twitter message to the user
  consumer_key = '0Omhyk50WW7q1PNUlNZbjaelf'
  consumer_secret = 'FRUxyM3gnXRM1cjdDmMUj5cGCZEOGH2FUPoJafg19VjuVd3G8w'

  access_token = '705390766139514880-TdUonzscZ2Y7jesE3PxXcaY8gdayy3L'
  access_token_secret = 'TWVm3c8ItcpPXgyMnmNzh2xrOEtu1NVC9a9hg8G6YLDiW'
  

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  api = tweepy.API(auth)

  api.send_direct_message(screen_name=user, text=message)

  return 'Message sent!'

def nextBus(busNum):
  
  # Parsing the ZTM site, finding next departure and composing a message
  r = requests.get("http://www.ztm.waw.pl/rozklad_nowy.php?c=182&l=1&a={}&n=3333&o=04&k=B".format(busNum))
  html_doc = r.text
  soup = BeautifulSoup(html_doc, 'html.parser')
  ztm_html = soup.find(id="RozkladContent")

  nbusreg = re.compile(r'(odjazd za\s)(.*\d+\smin)')
  next_bus = nbusreg.search(str(ztm_html))

  return "Najbliższy odjazd {} za {}".format(busNum,next_bus.group(2))

def waitButton():

  # When button is pressed

  GPIO.wait_for_edge(18, GPIO.RISING)
  print("Button pressed")
  sendMessage(nextBus("185"), '@Sedov00')
  sendMessage(nextBus("179"), '@Sedov00')

  sendMessage(nextBus("185"), '@JusPiTr')
  sendMessage(nextBus("179"), '@JusPiTr')

if __name__ == '__main__':
  main()
