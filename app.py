import pyautogui
import os 
import time
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import threading
import shutil

def stop():
	global stopt
	stopt = True


def start(lbFile):

	global stopt
	stopt = False
	with open('temp.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(["xloc", "yloc"])
		while True:
			loca = [pyautogui.position()[0], pyautogui.position()[1]]	
			writer.writerow(loca)
			f.flush()
			time.sleep(0.01)
			if stopt == True:
				break	

	original = r'temp.csv'
	timestr = time.strftime("%Y%m%d-%H%M%S")
	target = os.getcwd() + '\data' + '\data'+ timestr +'.csv'
	shutil.move(original,target)

	lbFile.delete(0, lbFile.size())
	for index, file in enumerate(os.listdir('data/')):
		lbFile.insert(index, file)		
	


def graph(lbFile):
	col_list = ["xloc", "yloc"]
	df = pd.read_csv("data/{}".format(lbFile.get(lbFile.curselection())), usecols=col_list)

	x = df["xloc"]
	y = df["yloc"]
	w, h = pyautogui.size()

	plt.hist2d(x,y, bins=[np.arange(0,w,20),np.arange(0,h,20)])
	plt.gca().invert_yaxis()

	plt.show()



def tkinter():
	global stopt
	stopt = False

	font = ("Roboto", 10, 'bold')
	m=tk.Tk(className='MouseMonitoring')
	m.minsize(600, 380)

	frame = tk.Frame(m)

	text = tk.Text(m, wrap='word', height = 5, width = 50, font=font)
	text.insert(tk.END, "Press the START button to start the mouse monitoring. Press the STOP button to end it. \nThe CSV files containing the recordings (in form of x and y cooridnates) are stored in " + os.getcwd() + '\data')

	scrl = tk.Scrollbar(frame) 
	lbFile = tk.Listbox(frame, font=("Roboto", 11, 'underline'), yscrollcommand = scrl.set, selectmode='multiple')

	btnStart = tk.Button(m, text='Start', width=25, font=font, command=lambda: [threading.Thread(target=start, args=(lbFile,)).start(), btnStart.config(state=tk.DISABLED), btnStop.config(state=tk.NORMAL)])
	btnStop = tk.Button(m, text='Stop', width=25, font=font, command=lambda: [stop(), btnStart.config(state=tk.NORMAL), btnStop.config(state=tk.DISABLED), btnResult.config(state=tk.DISABLED)], state = 'disabled')
	btnResult = tk.Button(m, text='Show heatmap', width=25, font=font, command=lambda: graph(lbFile), state = 'disabled')
	

	def callback(event):
		selection = event.widget.curselection()
		if selection:
			btnResult.config(state=tk.NORMAL)
		else:
			btnResult.config(state=tk.DISABLED)


	lbFile.bind("<<ListboxSelect>>", callback)

	try:
		for index, file in enumerate(os.listdir('data/')):
			lbFile.insert(index, file)
	except:
		os.mkdir(os.getcwd() + '\data')
		for index, file in enumerate(os.listdir('data/')):
			lbFile.insert(index, file)



	
	btnStart.pack(side = 'top', fill = 'x')
	btnStop.pack(side = 'top', fill = 'x')
	text.pack(side = 'top', fill = 'x')
	text.config(state=tk.DISABLED)

	frame.pack(expand='yes', side = 'left', fill = 'both')
	scrl.pack(side = 'right', fill = 'y')
	lbFile.pack(expand='yes', side = 'left', fill = 'both')
	

	
	btnResult.pack(side = 'bottom', fill = 'y')
	

	m.mainloop( )


def main():
	tkinter()


if __name__ == '__main__':
	main()
	






