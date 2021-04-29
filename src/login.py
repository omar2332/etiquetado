from tkinter import *


import boto3
from tkinter import messagebox
import json


from src import decisionFrame
from src import LabelTool



class LoginPage():
    """docstring for LoginPage"""
    def __init__(self):
        self.aws_access_key_id=""
        self.aws_secret_access_key=""
        self.aws_access_key_id_login_entry = None
        self.aws_secret_access_key__login_entry=None
        self.list_buckets = []
        self.frame1 = None

        self.data = {}
        with open('src/jsons/data.json') as file:
            self.data = json.load(file)

    def validation_credentials(self):
        s3=None
        try:
            s3 = boto3.resource(
            service_name='s3',
            region_name='us-east-1',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key)
            self.list_buckets = list(s3.buckets.all())
        except Exception as e:
            s3=None
            self.list_buckets = []
        return s3

    def get_data(self):
        self.aws_access_key_id = self.aws_access_key_id_login_entry.get()
        self.aws_secret_access_key = self.aws_secret_access_key__login_entry.get()
        self.s3 = self.validation_credentials()
        if self.s3 is None:
            messagebox.showinfo(message="No se pudo iniciar sesion, intente de nuevo", title="Guardar")
        else:
            if self.data['continue'] == True:
                self.showDecisionFrame()
            else:
                self.showLabelTool()

    def LoginPageInit(self,frames,ventana):
        self.frames = frames
        self.frame1 = frames[0]
        self.ventana = ventana
        Label(self.frame1, text="Please enter aws access keys").pack()
        Label(self.frame1, text="").pack()
        Label(self.frame1, text="aws_access_key_id").pack()
        self.aws_access_key_id_login_entry = Entry(self.frame1, width=100)
        self.aws_access_key_id_login_entry.pack()
        Label(self.frame1, text="").pack()
        Label(self.frame1, text="aws_secret_access_key").pack()
        self.aws_secret_access_key__login_entry = Entry(self.frame1, width=100)
        self.aws_secret_access_key__login_entry.pack()
        Label(self.frame1, text="").pack()
        Button(self.frame1, text="Login", width=10, height=1,command=self.get_data).pack()
        self.frame1.pack()

    def showDecisionFrame(self):
        self.frame1.pack_forget()
        decframe = decisionFrame.DecisionFrame()
        decframe.DecisionFrameInit(self.frames,self.list_buckets,self.s3,self.data,self.ventana)

    def showLabelTool(self):
        self.frame1.pack_forget()
        self.my_bucket = self.s3.Bucket(self.data['bucket'])
        Ltool=LabelTool.LabelTool()
        Ltool.LabelToolInit(self.data,self.frames,self.my_bucket,self.ventana)

        


