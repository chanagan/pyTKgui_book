import tkinter as tk
from tkinter import ttk
from datetime import datetime
from . import widgets as w


class DataRecordForm(tk.Frame):
	"""The input form for our widgets"""

	def __init__(self, parent, fields, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)

		# A dict to keep track of input widgets
		self.inputs = {}

		recordinfo = tk.LabelFrame(self, text="Record Information")

		self.inputs['Date'] = w.LabelInput(
			recordinfo, "Date",
			field_spec=fields['Date']
		)
		self.inputs['Date'].grid(row=0, column=0)

		self.inputs['Time'] = w.LabelInput(
			recordinfo, "Time",
			field_spec=fields['Time']
		)
		self.inputs['Time'].grid(row=0, column=1)

		self.inputs['Technician'] = w.LabelInput(
			recordinfo, "Technician",
			field_spec=fields['Technician']
		)
		self.inputs['Technician'].grid(row=0, column=2)

		# line 2
		self.inputs['Lab'] = w.LabelInput(
			recordinfo, "Lab",
			field_spec=fields['Lab']
		)
		self.inputs['Lab'].grid(row=1, column=0)

		self.inputs['Plot'] = w.LabelInput(
			recordinfo, "Plot",
			field_spec=fields['Plot']
		)
		self.inputs['Plot'].grid(row=1, column=1)

		self.inputs['Seed sample'] = w.LabelInput(
			recordinfo, "Seed sample",
			field_spec=fields['Seed sample']
		)
		self.inputs['Seed sample'].grid(row=1, column=2)

		recordinfo.grid(row=0, column=0, sticky=tk.W + tk.E)

		# Environment Data
		environmentinfo = tk.LabelFrame(self, text="Environment Data")
		self.inputs['Humidity'] = w.LabelInput(
			environmentinfo, "Humidity (g/m³)",
			input_class=tk.Spinbox, input_var=tk.DoubleVar(),
			input_args={"from_": 0.5, "to": 52.0, "increment": .01})
		self.inputs['Humidity'].grid(row=0, column=0)

		self.inputs['Light'] = w.LabelInput(
			environmentinfo, "Light level (klx)",
			input_class=tk.Spinbox, input_var=tk.DoubleVar(),
			input_args={"from_": 0, "to": 100, "increment": 1})
		self.inputs['Light'].grid(row=0, column=1)

		self.inputs['Temperature'] = w.LabelInput(
			environmentinfo, "Temp (°C)",
			input_class=tk.Spinbox, input_var=tk.DoubleVar(),
			input_args={"from_": 4, "to": 40, "increment": 1})
		self.inputs['Temperature'].grid(row=0, column=2)

		self.inputs['Equipment Fault'] = w.LabelInput(
			environmentinfo, "Equipment Fault",
			input_class=ttk.Checkbutton,
			input_var=tk.BooleanVar())
		self.inputs['Equipment Fault'].grid(
			row=1, column=0, columnspan=3)
		environmentinfo.grid(row=1, column=0, sticky=tk.W + tk.E)

		plantinfo = tk.LabelFrame(self, text="Plant Data")

		self.inputs['Plants'] = w.LabelInput(
			plantinfo, "Plants",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 20})
		self.inputs['Plants'].grid(row=0, column=0)

		self.inputs['Blossoms'] = w.LabelInput(
			plantinfo, "Blossoms",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 1000})
		self.inputs['Blossoms'].grid(row=0, column=1)

		self.inputs['Fruits'] = w.LabelInput(
			plantinfo, "Fruits",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 1000})
		self.inputs['Fruits'].grid(row=0, column=2)

		self.inputs['MinHeight'] = w.LabelInput(
			plantinfo, "Min Height (cm)",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 20})
		self.inputs['MinHeight'].grid(row=1, column=0)

		self.inputs['MaxHeight'] = w.LabelInput(
			plantinfo, "Max Height (cm)",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 1000})
		self.inputs['MaxHeight'].grid(row=1, column=1)

		self.inputs['MedHeight'] = w.LabelInput(
			plantinfo, "Median Height (cm)",
			input_class=tk.Spinbox,
			input_var=tk.IntVar(),
			input_args={"from_": 0, "to": 1000})
		self.inputs['MedHeight'].grid(row=1, column=2)

		plantinfo.grid(row=2, column=0, sticky=tk.W + tk.E)

		# Notes section
		self.inputs['Notes'] = w.LabelInput(
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
