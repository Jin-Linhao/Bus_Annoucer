#!/usr/bin/env python
#coding:utf-8
# program runs in the background, scanning for bluetooth devices 
# at a regular interval. 
# This code is meant to be run in Linux, not in OS or Windows
# For installation pygame in Linux, open a terminal and run sudo apt-get install python-pygame
# For iPad bluetooth, the discover range is less than 15m.

__author__ = 'JIN Linhao'
__date__ = '07/Mar/2016'
__contact__ = 'jin_linhao@hotmail.com'


import os, time, platform
import time, threading
from urllib import urlencode
from urllib2 import urlopen, URLError
import pygame.mixer
from pygame.locals import *
import cv2
import Tkinter as tk
from Tkinter import *



# get the name of this scanner
scanner_id = os.popen('uname -n').readline().strip()
time_end=0
root = tk.Tk()
shareData = tk.StringVar()
shareData.set("...")


id_dict = {"Linhao's":["02.wav", "Bus179"], 
		   "Edina":["02.wav", "Bus199"],
		   "Galaxy":["02.wav", "Bus179A"],
		   "Guoyong's":["02.wav", "Bus123"],
		   "songcx":["02.wav", "Bus123"],
		   "scanning":["02.wav", "...."]}




def scan_id():
	"""Scan nearby bluetooth devices and get all the bluetooth name"""
	while True:
		ids = []

		# launch the scanner
		f = os.popen('hcitool scan --length=2')
		# get the output from the scanner utility
		unparsed_data = f.readlines()[:]


		for u in unparsed_data:
			# get the ID of the bluetooth devices
			test = u.split()[1]
			# print test
			for id in id_dict.keys():
				# print id_dict.keys()
				if id  == u.split()[1]:

					ids.append(id)
			else:
				pass
		ids.append("scanning")
		print ids

		return ids






def show_id():
	"""print the bluetooth id on screen and broadcast the audio recording"""
	global time_end
	# print "..."


	ids = scan_id()
	# print ids

	for id in ids :

		print id_dict[id][1]
		if pygame.mixer.get_init() and time.time()>time_end:
			audio_record = pygame.mixer.Sound("/home/eee/Documents/Bus_Annoucer/audio/" + id_dict[id][0])
			audio_player = audio_record.play(maxtime=2000) #play the sound for two seconds
			time_end = time.time() + 3
			shareData.set(id_dict[id][1])
			# print time.localtime(time.time()), time.localtime(time_end)
	
			root.update_idletasks()
			time.sleep(3)
			continue
		# else:
		# 	continue
			






def test():
	while True:

		if (programRunning):
			show_id()
		else:
			return





		
class Application(tk.Frame):

	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()
		#while initializing the windows, run Test
		test_thread = threading.Thread(target = test)
		test_thread.daemon = True
		test_thread.start()


	def createWidgets(self):
		self.QUIT = tk.Button(self, text = "QUIT", fg = "red", command = self.exitProgram)
		self.QUIT.pack(side = BOTTOM)
		self.entry = Entry(self, textvariable = shareData, font = ("Helvetica", 68), justify = CENTER)
		self.entry.pack(padx = 0, pady = 600)


	def exitProgram(self):
		global programRunning
		programRunning = False
		root.destroy()



	




if __name__ == '__main__':

	pygame.mixer.init()
	
	programRunning = True
	app = Application(master = root)
	root.geometry("2880x1800")
	root.mainloop()




			 	
		


	
