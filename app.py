import tkinter as tk

from src import login



def main():
	ventana = tk.Tk()
	windowWidth = 1250
	windowHeight = 720
	positionRight = int(ventana.winfo_screenwidth()/2 - windowWidth/2)
	positionDown = int(ventana.winfo_screenheight()/2 - windowHeight/2)
	ventana.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))

	frames = [tk.Frame(ventana) for _ in range(4)]


	log_object = login.LoginPage()
	log_object.LoginPageInit(frames,ventana)
	
	
	ventana.mainloop()




if __name__ == '__main__':
	main()