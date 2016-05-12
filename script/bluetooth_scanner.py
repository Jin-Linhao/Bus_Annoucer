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
shareList = tk.StringVar()
shareList.set("")
shareids = tk.StringVar()
shareids.set("")
sharetime = tk.StringVar()
sharetime.set("")


id_dict = {"Linhao's":["179.wav", "Bus179"], 
		   "Edina":["199.wav", "Bus199"],
		   # "Galaxy":["179A.wav", "Bus179A"],
		   "Guoyong's":["02.wav", "Bus123"],
		   "Brian":["02.wav", "Bus1111"],
		   "songcx":["02.wav", "Bus123"]}
		   # "scanning":["", "...."]}




def enter_time():
	bus_enter_time = time.strftime("%H:%M")
	return  bus_enter_time



def scan_id():
	"""Scan nearby bluetooth devices and get all the bluetooth name"""
	while True:
		ids = []
		ids_list = []
		# launch the scanner
		f = os.popen('hcitool scan --length=2')
		# get the output from the scanner utility
		unparsed_data = f.readlines()[:]


		for u in unparsed_data:
			# get the ID of the bluetooth devices
			# print u.split()
			for id in id_dict.keys():

				# print id_dict.keys()
				if id  == u.split()[1]:

					ids.append(id)
			else:
				pass	

		return ids



def show_bus_list():
	bus_ids_list = scan_id()
	bus_name_list = ""


	for bus_ids in bus_ids_list:
		
		bus_dict = id_dict[bus_ids][1]
		bus_name_list += bus_dict + " "
		# print bus_name_list
	if bus_name_list == "":
		pass
	else:
		bus_name_list = bus_name_list
		shareids.set(bus_name_list)
		root.update_idletasks()



def show_id():
	"""print the bluetooth id on screen and broadcast the audio recording"""
	global time_end
	
	ids = scan_id()
	ids.append("scanning")
	# show_whole_list()

	for id in ids :

		
		# print id_dict[id][1]
		if pygame.mixer.get_init() and id_dict.has_key(id):
			audio_record = pygame.mixer.Sound("/home/eee/Documents/Bus_Annoucer/audio/wav/" + id_dict[id][0])
			audio_player = audio_record.play(maxtime=3000) #play the sound for two seconds
			
			shareData.set(id_dict[id][1])
			bus_enter_time = enter_time()
			sharetime.set("arrived at " + bus_enter_time)

			root.update_idletasks()
			time.sleep(4)
			continue
		else:
			shareData.set("...")
			root.update_idletasks()


			break
	


# def show_whole_list():
# 	ids_list = scan_id()
# 	new_id_list = []

# 	for idlist in ids_list:
# 		# print idlist
# 		idlist = idlist + "\n"
# 		continue
# 		# idlist.append("\n")
# 	shareList.set(id_dict[idlist][1])
# 	root.update_idletasks()



def test():
	global app
	while True:

		if (programRunning):
			enter_time()
			show_bus_list()
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
		self.entry1 = Entry(self, textvariable = shareData, fg = "red", font = ("Helvetica", 78), justify = CENTER)
		self.entry1.pack(padx = 0, pady = 150)

		self.entry2 = Entry(self, textvariable = shareids, font = ("Helvetica", 45), width = 35)
		self.entry2.pack(padx = 0, pady = 10)
		self.entry3 = Entry(self, textvariable = sharetime, font = ("Helvetica", 45), width = 35)
		self.entry3.pack(padx = 0, pady = 0)

		self.text = Text(self, width = 88, height = 2, font = ("Helvetica", 18)) 
		self.text.insert(END, 'Buses available :\n')
		self.text.insert(END, 'Bus179 Bus199 Bus179A Bus123')
		self.text.pack(padx = 0, pady = 250)


		self.QUIT = tk.Button(self, text = "QUIT", fg = "red", command = self.exitProgram)
		self.QUIT.pack(padx = 0, pady = 0 )



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




			 	
		


	
