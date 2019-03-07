import tkinter as tk
import time
import platform


class Gui(tk.Frame):

	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		self.row_top = tk.Frame(master)
		self.row_bot = tk.Frame(master)
		self.row_top.grid(row=0, column=0)
		self.row_bot.grid(row=1, column=0, sticky='ew', padx=(10,0))
		self.add_elements()
		self.set_time()

	# draw/create gui elements
	def add_elements(self):
		# directory label and entry (aren't packed currently)
		self.label_dir = tk.Label(self.row_top, text=strings('label_dir'), state='disabled')
		self.entry_dir = tk.Entry(self.row_top, width=10)
		self.entry_dir.insert(tk.END, strings('path_dir'))
		# self.entry_dir.configure(state='disabled')

		# filename label and entry (aren't packed currently)
		self.label_filename = tk.Label(self.row_top, text=strings('label_filename'), state='disabled')
		self.entry_filename = tk.Entry(self.row_top, width=10)
		self.entry_filename.insert(tk.END, strings('name_filename'))
		# self.entry_filename.configure(state='disabled')

		# text area input and y-scrollbar
		# bind RETURN to text area input
		self.text_entry = tk.Text(self.row_bot, width=50, height=4, wrap='word')
		self.text_entry.bind('<Return>', self.log_entry_event)
		self.scrolly = tk.Scrollbar(self.row_bot, orient='vertical', command=self.text_entry.yview)
		self.text_entry.configure(yscrollcommand=self.scrolly.set)

		# enter button
		self.button_enter = tk.Button(self.row_top, text=strings('button_enter'), command=self.log_entry)

		# time and message labels
		self.label_time = tk.Label(self.row_top, text='')
		self.label_message = tk.Label(self.row_top, text='')

		# pack time, message, text area input and enter button
		# don't pack directory and filename label/entries
		# pack y-scrollbar separately
		self.elements = [self.label_time, self.label_message, self.text_entry, self.button_enter]
		for el in self.elements:
			el.pack(side='left', pady=2, padx=1)
		self.scrolly.pack(side='left', fill='y')

		# focus text area input on launch
		self.text_entry.focus()

	# entry event bound to RETURN key press on text area input
	# return 'break' prevents the logging of a new line character born from RETURN key press
	def log_entry_event(self, event):
		self.log_entry()
		return 'break'

	# logging/appending to file function
	def log_entry(self):
		try:
			# get path and filename from their respective entries
			# currently the static values in the strings dictionary
			path = str(self.entry_dir.get())
			file = str(self.entry_filename.get())

			# if filename doesn't end in .txt append it
			# if path ends in backward or forward slash append filename to path
			# else add a forward slash between them
			if file[len(file)-4:len(file)] != '.txt':
				file += '.txt'
			if path[len(path)-1:len(path)] == '\\' or path[len(path)-1:len(path)] == '/':
				log_path = path + file
			else:
				log_path = path + '/' + file

			# format the log output
			# 2019.03.07 20:30:05| this is a test log.
			# append it to the log file and clear the text area input
			log = self.get_time() + '| ' + str(self.text_entry.get('1.0', 'end'))
			with open(log_path, 'a') as f:
				f.write(log)
			self.text_entry.delete('1.0', 'end')
			self.label_message.config(text='')
		except IOError:
			self.label_message.config(text=strings('err_io'))

	# get time in the most logical fashion ever invented by men
	# YYYY.MM.DD HH:MM:SS ex. 2019.03.07 20:30:05
	# month, day, hour, minute and seconds are with leading zeroes
	# 24 hour formatting to not lose much more space in time
	def get_time(self):
		return time.strftime('%Y.%m.%d %H:%M:%S')

	# reset gui date/time display every .3 seconds
	def set_time(self):
		self.label_time.config(text=self.get_time())
		self.after(333, self.set_time)


# a dictionary of strings to hold everything in one place
dict_strings = {
	# static
	'title': 'Log Recorder',
	'label_dir': 'Dir:',
	'label_filename': 'Name:',
	'button_enter': 'Enter',
	# messages
	'err_io': '|| Error. Directory does not exist.',
	# configurable
	'path_dir': 'Other',
	'name_filename': 'myLogs',
}

# returns the string value with given key
def strings(s):
	return dict_strings.get(s)

# if on Windows spawns the window to the upper left of the screen
# else top of the middle
# note: I don't have access to OS X to see if it looks good or if it works
# FIXME: assumes 1920 screen width for other OSes
def get_geometry():
	if platform.system() == 'Windows':
		return '435x115+94+0'
	# elif os == 'Linux'
	# might as well use else to include OS X
	else:
		screen_width = 1920
		program_width = 390
		x_position = (screen_width - program_width) / 2
		return ('%dx115+%d+30' % (program_width, x_position))


if __name__ == '__main__':
	root = tk.Tk()
	# Linux scaling problem fix
	# needs testing on Windows
	# might add an if platform.system() == 'Linux':
	root.tk.call('tk', 'scaling', 1.3)
	root.title(strings('title'))
	root.geometry(get_geometry())
	app = Gui(master=root)
	app.mainloop()
