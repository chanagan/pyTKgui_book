from datetime import datetime
import os
import csv

import tkinter as tk
from tkinter import ttk

"""Start coding here"""


class LabelInput(tk.Frame):
	"""A widget containing a label and input together."""

	def __init__(self, parent, label='', input_class=ttk.Entry,
			input_var=None, input_args=None, label_args=None,
			**kwargs):
		super().__init__(parent, **kwargs)
		input_args = input_args or {}
		label_args = label_args or {}
		self.variable = input_var

		if input_class in (ttk.Checkbutton, ttk.Button,
		ttk.Radiobutton):
			input_args["text"] = label
			input_args["variable"] = input_var
		else:
			self.label = ttk.Label(self, text=label, **label_args)
			self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
			input_args["textvariable"] = input_var

		self.input = input_class(self, **input_args)
		self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))

		self.columnconfigure(0, weight=1)

	def grid(self, sticky=(tk.E + tk.W), **kwargs):
		super().grid(sticky=sticky, **kwargs)

	def get(self):
		try:
			if self.variable:
				return self.variable.get()
			elif type(self.input) == tk.Text:
				return self.input.get('1.0', tk.END)
			else:
				return self.input.get()
		except (TypeError, tk.TclError):
			# happens when numeric fields are empty.
			return ''

	def set(self, value, *args, **kwargs):
		if type(self.variable) == tk.BooleanVar:
			self.variable.set(bool(value))
		elif self.variable:
			self.variable.set(value, *args, **kwargs)
		elif type(self.input) in (ttk.Checkbutton,
		ttk.Radiobutton):
			if value:
				self.input.select()
			else:
				self.input.deselect()
		elif type(self.input) == tk.Text:
			self.input.delete('1.0', tk.END)
			self.input.insert('1.0', value)
		else:  # input must be an Entry-type widget with no variable
			self.input.delete(0, tk.END)
			self.input.insert(0, value)


class DataRecordForm(tk.Frame):
	"""The input form for our widgets"""

	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)

		# A dict to keep track of input widgets
		self.inputs = {}

		recordinfo = tk.LabelFrame(self, text="Record Information")

		self.inputs['Date'] = LabelInput(recordinfo, "Date",
			input_var=tk.StringVar())
		self.inputs['Date'].grid(row=0, column=0)

		self.inputs['Time'] = LabelInput(recordinfo, "Time",
			input_class=ttk.Combobox, input_var=tk.StringVar(),
			input_args={"values": ["8:00", "12:00", "16:00", "20:00"]})
		self.inputs['Time'].grid(row=0, column=1)

		self.inputs['Technician'] = LabelInput(recordinfo,
			"Technician",
			input_var=tk.StringVar())
		self.inputs['Technician'].grid(row=0, column=2)

		# line 2
		self.inputs['Lab'] = LabelInput(recordinfo, "Lab",
			input_class=ttk.Combobox, input_var=tk.StringVar(),
			input_args={"values": ["A", "B", "C", "D", "E"]})
		self.inputs['Lab'].grid(row=1, column=0)

		self.inputs['Plot'] = LabelInput(recordinfo, "Plot",
			input_class=ttk.Combobox, input_var=tk.IntVar(),
			input_args={"values": list(range(1, 21))})
		self.inputs['Plot'].grid(row=1, column=1)

		self.inputs['Seed sample'] = LabelInput(
			recordinfo, "Seed sample", input_var=tk.StringVar())
		self.inputs['Seed sample'].grid(row=1, column=2)

		recordinfo.grid(row=0, column=0, sticky=tk.W + tk.E)

		# Environment Data
		environmentinfo = tk.LabelFrame(self, text="Environment Data")
		self.inputs['Humidity'] = LabelInput(
			environmentinfo, "Humidity (g/m³)",
			input_class=tk.Spinbox, input_var=tk.DoubleVar(),
			input_args={"from_": 0.5, "to": 52.0, "increment": .01})
		self.inputs['Humidity'].grid(row=0, column=0)

		self.inputs['Light'] = LabelInput(
			environmentinfo, "Light level (klx)",
			input_class=tk.Spinbox, input_var=tk.DoubleVar(),
			input_args={"from_": 0, "to": 100, "increment": 1})
		self.inputs['Light'].grid(row=0, column=1)

		self.inputs['Temperature'] = LabelInput(
			environmentinfo, "Temp (°C)",
			input_class=tk.Spinbox, input_var=tk.DoubleVar(),
			input_args={"from_": 4, "to": 40, "increment": 1})
		self.inputs['Temperature'].grid(row=0, column=2)

		self.inputs['Equipment Fault'] = LabelInput(
			environmentinfo, "Equipment Fault",
			input_class=ttk.Checkbutton,
			input_var=tk.BooleanVar())
		self.inputs['Equipment Fault'].grid(
			row=1, column=0, columnspan=3)
		environmentinfo.grid(row=1, column=0, sticky=tk.W + tk.E)

		plantinfo = tk.LabelFrame(self, text="Plant Data")

		self.inputs['Plants'] = LabelInput(
			plantinfo, "Plants",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 20})
		self.inputs['Plants'].grid(row=0, column=0)

		self.inputs['Blossoms'] = LabelInput(
			plantinfo, "Blossoms",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 1000})
		self.inputs['Blossoms'].grid(row=0, column=1)

		self.inputs['Fruits'] = LabelInput(
			plantinfo, "Fruits",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 1000})
		self.inputs['Fruits'].grid(row=0, column=2)

		self.inputs['MinHeight'] = LabelInput(
			plantinfo, "Min Height (cm)",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 20})
		self.inputs['MinHeight'].grid(row=1, column=0)

		self.inputs['MaxHeight'] = LabelInput(
			plantinfo, "Max Height (cm)",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 1000})
		self.inputs['MaxHeight'].grid(row=1, column=1)

		self.inputs['MedHeight'] = LabelInput(
			plantinfo, "Median Height (cm)",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 1000})
		self.inputs['MedHeight'].grid(row=1, column=2)

		plantinfo.grid(row=2, column=0, sticky=tk.W + tk.E)

		# Notes section
		self.inputs['Notes'] = LabelInput(
			self, "Notes",
			input_class=tk.Text,
			input_args={"width": 75, "height": 10}
		)
		self.inputs['Notes'].grid(sticky="w", row=3, column=0)

	def get(self):
		data = {}
		for key, widget in self.inputs.items():
			data[key] = widget.get()
		return data

	def reset(self):
		for widget in self.inputs.values():
			widget.set('')
		self.reset()


class ValidatedMixin:
	"""Adds a validation functionality"""

	def __init__(self, *args, error_var=None, **kwargs):
		self.error = error_var or tk.StringVar()
		super().__init__(*args, **kwargs)

		vcmd = self.register(self._validate)
		invcmd = self.register(self._invalid)

		self.config(
			validate='all',
			validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
			invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d')
		)

	def _toggle_error(self, on=False):
		self.config(foreground=('red' if on else 'black'))

	def _validate(self, proposed, current, char, event, index,
			action):
		self._toggle_error(False)
		self.error.set('')
		valid = True
		if event == 'focusout':
			valid = self._focusout_validate(event=event)
		elif event == 'key':
			valid = self._key_validate(proposed=proposed,
				current=current, char=char, event=event,
				index=index, action=action)
		return valid

	def _focusout_validate(self, **kwargs):
		return True

	def _key_validate(self, **kwargs):
		return True

	def trigger_focusout_validation(self):
		valid = self._validate('', '', '', 'focusout', '', '')
		if not valid:
			self._focusout_invalid(event='focusout')
		return valid


class RequiredEntry(ValidatedMixin, ttk.Entry):
	def _focusout_validate(self, event):
		valid = True
		if not self.get():
			valid = False
			self.error.set('A value is required')
		return valid


class DateEntry(ValidatedMixin, ttk.Entry):
	"""An entry for ISO-style dates (year-month-day)"""

	def __init__(self, parent, *args, **kwargs):
		"""Constructor"""
		super().__init__(parent, *args, **kwargs)
		self.config(
			validate='all',
			validatecommand=(
				self.register(self._validate),
				'%S', '%i', '%V', '%d'
			),
			invalidcommand=(self.register(self._on_invalid), '%V')
		)
		self.error = tk.StringVar()

	def _toggle_error(self, error=''):
		""""""
		self.error.set(error)
		if error:
			self.config(foreground='red')
		else:
			self.config(foreground='black')

	def _validate(self, char, index, event, action):
		# reset error state
		self._toggle_error()
		valid = True

		if event == 'key':
			if action == '0':  # a delete event should always validate
				valid = True
			elif index in ('0', '1', '2', '3',
			'5', '6', '8', '9'):
				valid = char.isdigit()
			elif index in ('4', '7'):
				valid = char == '-'
			else:
				valid = False
		elif event == 'focusout':
			try:
				datetime.strptime(self.get(), '%Y-%m-%d')
			except ValueError:
				valid = False

		return valid

	def _on_invalid(self, event):
		if event != 'key':
			self._toggle_error('Not a valid date')

	def _key_validate(self, action, index, char, **kwargs):
		valid = True

		if action == '0':
			valid = True
		elif index in ('0', '1', '2', '3', '5', '6', '8', '9'):
			valid = char.isdigit()
		elif index in ('4', '7'):
			valid = char == '-'
		else:
			valid = False
		return valid

	def _focusout_validate(self, event):
		valid = True
		if not self.get():
			self.error.set('A value is required')
			valid = False
		try:
			datetime.strptime(self.get(), '%Y-%m-%d')
		except ValueError:
			self.error.set('Invalid date')
			valid = False
		return valid


class ValidatedCombobox(ValidatedMixin, ttk.Combobox):

	def _key_validate(self, proposed, action, **kwargs):
		valid = True
		# if the user tries to delete, just clear the field
		if action == '0':
			self.set('')
			return True

		# get our values list
		values = self.cget('values')
		# Do a case-insensitive match against the entered text
		matching = [
			x for x in values
			if x.lower().startswith(proposed.lower())
		]
		if len(matching) == 0:
			valid = False
		elif len(matching) == 1:
			self.set(matching[0])
			self.icursor(tk.END)
			valid = False
		return valid


	def _focusout_validate(self, **kwargs):
		valid = True
		if not self.get():
			valid = False
			self.error.set('A value is required')
		return valid


class Application(tk.Tk):
	"""Application root window"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.title("ABQ Data Entry Application")
		self.resizable(width=False, height=False)

		ttk.Label(
			self,
			text="ABQ Data Entry Application",
			font=("TkDefaultFont", 16)
		).grid(row=0)

		self.recordform = DataRecordForm(self)
		self.recordform.grid(row=1, padx=10)

		self.savebutton = ttk.Button(self, text="Save", command=self.on_save)
		self.savebutton.grid(sticky=tk.E, row=2, padx=10)

		# status bar
		self.status = tk.StringVar()
		self.statusbar = ttk.Label(self, textvariable=self.status)
		self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)

		self.records_saved = 0

	def on_save(self):
		datestring = datetime.today().strftime("%Y-%m-%d")
		filename = "abq_data_record_{}.csv".format(datestring)
		newfile = not os.path.exists(filename)

		data = self.recordform.get()

		with open(filename, 'a') as fh:
			csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
			if newfile:
				csvwriter.writeheader()
			csvwriter.writerow(data)
		# self.recordform.reset()

		self.records_saved += 1
		self.status.set(
			"{} records saved this session".format(self.records_saved)
		)

if __name__ == "__main__":
	app = Application()
	app.mainloop()
