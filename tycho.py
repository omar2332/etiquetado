from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import boto3
import json
import csv




	
class programa():

	
	def __init__(self):

		self.data = {}
		with open('info.json') as file:
			self.data = json.load(file)


		
		s3 = boto3.resource(
			service_name='s3',
			region_name='us-east-1',
			aws_access_key_id=self.data['awsaccesskeyid'],
			aws_secret_access_key=self.data['awssecretaccesskey'])

		
		self.my_bucket = s3.Bucket(self.data['bucket'])
		self.lista = self.data['lista']
		self.indice = self.data['indice']
		self.lista_etiquetas = self.data['lista_etiquetas']
		self.total = len(self.lista_etiquetas)
	

		if self.data['existe']==False:
			self.lista = []
			self.lista_etiquetas = []
			for my_bucket_object in self.my_bucket.objects.all():
				temp = my_bucket_object.key
				temp2 = temp.split('/')
				if temp2[0]=='central-occidental': 
					if temp2[1] == self.data['archivo']: #aqui cambia
						temp2 = temp.split('.') 
						try:
							if temp2[1]=='jpg':
								self.lista.append(temp)
								self.lista_etiquetas.append( [ temp.split('/')[-1]  ,0] )
						except:
							print('no paso')
				
			list_temp = []
			for l in self.lista:
					list_temp.append([l.split('/')[-1],0])
			with open( self.data['archivo']+'.csv', 'w') as f:
				writer = csv.writer(f)
				writer.writerows(list_temp)

			self.data['existe']=True

			with open('info.json', 'w') as file:
				json.dump(self.data, file)
				

		print("Actual",self.lista_etiquetas[self.indice])
		print('indice: ', self.indice , " de ", self.total)



		self.directorio = ""
		self.directorio_guardar  =""
		self.ventana = tk.Tk()
		windowWidth = 1250
		windowHeight = 720
		positionRight = int(self.ventana.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(self.ventana.winfo_screenheight()/2 - windowHeight/2)
		self.path = "imagen.jpg"

		self.my_bucket.download_file(Key=self.lista[self.indice], Filename=self.path)
		#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
		self.img = ImageTk.PhotoImage(Image.open(self.path))

		#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
		self.panel = tk.Label(self.ventana, image = self.img)

		#The Pack geometry manager packs widgets in rows or columns.
		self.panel.pack(side = "top", fill = "both", expand = "yes")

		self.ventana.bind('<Left>', self.back_event)
		self.ventana.bind('<Right>', self.next_event)
		self.ventana.bind('<space>', self.marcar)



		self.back  = tk.Button(self.ventana,text="back",bg="salmon",command=self.back_event)
		self.back.pack(side='left')

		self.checkbox_value = tk.BooleanVar(self.ventana)
		self.cambia  = tk.Checkbutton(self.ventana,text="¿Torre?",variable=self.checkbox_value)



		self.cambia.pack(side='bottom')

		self.next  = tk.Button(self.ventana,text="next",bg="salmon",command=self.next_event)
		self.next.pack(side='left')

		

		self.guardar  = tk.Button(self.ventana,text="guardar",bg="salmon",command=self.guardar)
		self.guardar.pack(side='right')
		


		self.ventana.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))
		self.ventana.mainloop()

	def next_event(self,event = None):
		self.indice +=1

		if self.indice < len(self.lista):
			self.my_bucket.download_file(Key=self.lista[self.indice], Filename=self.path)
			self.img2 = ImageTk.PhotoImage(Image.open(self.path))
			self.panel.configure(image=self.img2)
			self.panel.image = self.img2

			if self.checkbox_value.get():
				self.lista_etiquetas[self.indice-1][1] = 1
				print("Marcado",self.lista_etiquetas[self.indice-1])
				self.cambia.invoke()
			else:
				self.lista_etiquetas[self.indice-1][1] = 0

			print("Actual",self.lista_etiquetas[self.indice])
			print('indice: ', self.indice , " de ", self.total)




		else:
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
			print('indice: ', self.indice , " de ", self.total)
				

		else:
			self.indice =0


	def marcar(self,event = None):
		self.cambia.invoke()
			

	def guardar(self):
		self.data['indice'] = self.indice

		with open('info.json', 'w') as file:
				json.dump(self.data, file, indent=4)

		with open( self.data['archivo']+'.csv', 'w', encoding='UTF8') as f:
				writer = csv.writer(f)
				writer.writerows(self.lista_etiquetas)
		messagebox.showinfo(message="Guardado Correctamente", title="Guardar")


if __name__ == '__main__':
	programa()
