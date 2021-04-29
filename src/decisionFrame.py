import tkinter as tk


from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


import json
import csv
from tqdm import tqdm

from src import LabelTool

class DecisionFrame():
	"""docstring for DecisionFrame"""
	def __init__(self):
		self.lista_buckets = []


	def showLabelTool(self):
		self.frame1.pack_forget()
		Ltool=LabelTool.LabelTool()
		Ltool.LabelToolInit(self.data,self.frames,self.my_bucket,self.ventana)

	def create_env(self):
		self.name_selected_bucket = self.combo.get().split("'")[1]
		self.my_bucket = self.s3.Bucket(self.name_selected_bucket)
		self.lista = self.data['lista_direcciones']
		self.indice = self.data['index']
		self.lista_etiquetas = self.data['lista_etiquetas']
		self.total = self.data['length']
		self.dir_archive = self.dir.get().split("/")

		if self.data['isCSV']==False:
			self.lista = []
			self.lista_etiquetas = []
			for my_bucket_object in tqdm(self.my_bucket.objects.all()):
				temp = my_bucket_object.key
				temp2 = temp.split('/')
				if temp2[0]==self.dir_archive[0]: 
					if temp2[1] == self.dir_archive[1]:
						temp2 = temp.split('.') 
						try:
							if temp2[1]=='jpg':
								self.lista.append(temp)
								self.lista_etiquetas.append( [ temp.split('/')[-1]  ,0] )
						except:
							print('no paso')
				
			list_temp = []
			for l in tqdm(self.lista):
					list_temp.append([l.split('/')[-1],0])
			with open( "CSVs/"+self.dir_archive[1]+'.csv', 'w') as f:
				writer = csv.writer(f)
				writer.writerows(list_temp)

			self.data['isCSV']=True
			self.data['lista_etiquetas']=self.lista_etiquetas
			self.data['lista_direcciones']=self.lista 
			self.data['archive'] = self.dir.get()
			self.data['continue']=False
			self.data['length'] = len(self.lista_etiquetas)
			self.data['bucket'] = self.name_selected_bucket
			

			with open('src/jsons/data.json', 'w') as file:
				json.dump(self.data, file,indent=4)
		messagebox.showinfo(message="Charged correctly", title="Guardar")
		self.showLabelTool()

	def carpeta(self):
		self.directorio = filedialog.askdirectory()
		if self.directorio!="":
			self.button1["bg"]="green"
		
		self.carpta1['text'] = self.directorio
		
		


	def carpeta_guardar(self):
		self.directorio_abrir = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = (("csv files","*.csv"),("all files","*.*")))
		if self.directorio_abrir!="":
			print(self.directorio_abrir)
			self.button2["bg"]="green"
		
		self.carpta2['text'] = self.directorio_abrir
		
	def procesar(self):
		import pandas as pd
		self.lista_direcciones = []
		self.archivo = self.dir.get().split("/")
		temp_selected_bucket = self.combo.get().split("'")[1]
		temp_bucket = self.s3.Bucket(temp_selected_bucket)

		if self.directorio != "" and self.directorio_abrir != "":
			temp = pd.read_csv(self.directorio_abrir,header=None) #aqui coloca el nombre del archivo

			etiquetas = temp[temp[1]==1]
			print(etiquetas)
			lista_etiquetas = etiquetas[0].values.tolist()
			print(lista_etiquetas)
			for my_bucket_object in temp_bucket.objects.all():
				temp = my_bucket_object.key
				temp2 = temp.split('/')
				if temp2[0]==self.archivo[0]:
					try:
						i = lista_etiquetas.index(temp2[-1])
						#print('Encontro:',temp)
						self.lista_direcciones.append(temp)
					except:
						pass
			
			#print(self.lista_direcciones)
			for dire in self.lista_direcciones:
				temp_bucket.download_file(Key=dire, Filename=self.directorio+"/"+dire.split("/")[-1])
			self.button3["bg"]="green"


	def DecisionFrameInit(self,frames,bucket,s3,data,ventana):
		self.data=data
		self.s3 = s3
		self.ventana = ventana
		self.lista_buckets = bucket
		self.frames = frames
		self.frame1 = frames[1]
		self.directorio_abrir = ""
		self.directorio = ""

		tk.Label(self.frame1, text="Please select S3 Buckets").pack()
		self.combo = ttk.Combobox(self.frame1,values=self.lista_buckets,width=50)
		self.combo.pack()
		tk.Label(self.frame1, text="Write the folder where the images are located").pack()
		self.dir = tk.Entry(self.frame1, width=50)
		self.dir.pack()
		tk.Label(self.frame1, text="").pack()
		tk.Button(self.frame1, text="Login", width=10, height=1,command=self.create_env).pack()
		self.frame1.pack()

		tk.Label(self.frame1, text="To download images, continue filling").pack()
		tk.Label(self.frame1, text="").pack()

		self.button1 = tk.Button(self.frame1,text="Select directory to save images",bg="salmon",command=self.carpeta)
		self.button1.pack()
		self.carpta1  = tk.Label(self.frame1, text = self.directorio)
		self.carpta1.pack()
		self.button2  = tk.Button(self.frame1,text="Select directory to csv files",bg="salmon",command=self.carpeta_guardar)
		self.button2.pack()
		self.carpta2  = tk.Label(self.frame1, text = self.directorio_abrir)
		self.carpta2.pack()

		self.button3  = tk.Button(self.frame1,text="Start",bg="salmon",command=self.procesar)
		self.button3.pack()


		