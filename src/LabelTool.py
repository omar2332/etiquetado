from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

import json
import csv


class LabelTool():
	"""docstring for LabelTool"""
	def __init__(self):
		self.path = "imagen.jpg"
		self.data = {}

	def LabelToolInit(self,data,frames,my_bucket,ventana):
		self.ventana= ventana
		self.frames = frames
		self.frame = frames[2]
		self.my_bucket =my_bucket
		self.data = data
		self.lista = self.data['lista_direcciones']
		self.indice = self.data['index']
		self.lista_etiquetas = self.data['lista_etiquetas']
		self.total = self.data['length']
		self.save_dir = "CSVs/"+self.data['archive'].split('/')[1]+'.csv'

		self.my_bucket.download_file(Key=self.lista[self.indice], Filename=self.path)

		print("Actual",self.lista_etiquetas[self.indice])
		print('indice: ', self.indice+1 , " de ", self.total)
		#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
		self.img = ImageTk.PhotoImage(Image.open(self.path))

		#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
		self.panel = tk.Label(self.frame, image = self.img)

		#The Pack geometry manager packs widgets in rows or columns.
		self.panel.pack(side = "top", fill = "both", expand = "yes")

		self.ventana.bind('<Left>', self.back_event)
		self.ventana.bind('<Right>', self.next_event)
		self.ventana.bind('<space>', self.marcar)


		self.back  = tk.Button(self.frame,text="back",bg="salmon",command=self.back_event)
		self.back.pack(side='left')
		self.checkbox_value = tk.BooleanVar(self.frame)
		self.cambia  = tk.Checkbutton(self.frame,text="¿Torre?",variable=self.checkbox_value)
		self.cambia.pack(side='bottom')
		self.next  = tk.Button(self.frame,text="next",bg="salmon",command=self.next_event)
		self.next.pack(side='left')
		self.btnguardar  = tk.Button(self.frame,text="guardar",bg="salmon",command=self.guardar)
		self.btnguardar.pack(side='right')
		self.frame.pack()



	def next_event(self,event = None):
		if self.checkbox_value.get():
			self.lista_etiquetas[self.indice][1] = 1
			print("Marcado",self.lista_etiquetas[self.indice])
			self.cambia.invoke()
		else:
			self.lista_etiquetas[self.indice][1] = 0

		self.indice +=1
		
		if self.indice < self.total:
			print("Actual",self.lista_etiquetas[self.indice])
			self.my_bucket.download_file(Key=self.lista[self.indice], Filename=self.path)
			self.img2 = ImageTk.PhotoImage(Image.open(self.path))
			self.panel.configure(image=self.img2)
			self.panel.image = self.img2

			
			print('indice: ', self.indice+1 , " de ", self.total)
		else:

			if self.indice ==self.total:
				self.Terminar  = tk.Button(self.frame,text="Finalizar y Guardar",bg="green",command=self.reset)
				self.Terminar.pack(side='bottom')

			self.indice = len(self.lista)-1


	def back_event(self,event = None):
		self.indice -=1

	
		if self.indice > -1:
			self.my_bucket.download_file(Key=self.lista[self.indice], Filename=self.path)
			self.img2 = ImageTk.PhotoImage(Image.open(self.path))
			self.panel.configure(image=self.img2)
			self.panel.image = self.img2
			if self.checkbox_value.get():
				self.cambia.invoke()
			print("Actual",self.lista_etiquetas[self.indice])
			print('indice: ', self.indice+1 , " de ", self.total)
				

		else:
			self.indice =0


	def marcar(self,event = None):
		self.cambia.invoke()
			
	def reset(self):
		self.guardar()
		self.data['index'] = 0
		self.data['length'] = 0
		self.data['continue']=True
		self.data['isCsv']=False
		self.data['bucket']=""
		self.data['archive']=""
		self.data['lista_etiquetas']=[]
		self.data['lista_direcciones']= []
		with open('src/jsons/data.json', 'w') as file:
				json.dump(self.data, file, indent=4)

		self.ventana.destroy()


	def guardar(self):
		self.data['index'] = self.indice

		with open('src/jsons/data.json', 'w') as file:
				json.dump(self.data, file, indent=4)

		with open( self.save_dir, 'w', encoding='UTF8') as f:
				writer = csv.writer(f)
				writer.writerows(self.lista_etiquetas)
		messagebox.showinfo(message="Guardado Correctamente", title="Guardar")
