import customtkinter as ctk
import tkinter as tk
import os
import csv



class Login:
    def __init__(self):
        super().__init__()
        self.title("SoggyStreams")
        self.geometry("600x600")
        self.resizable(True, True)
        self._build_ui()
        
    def _build_ui(self):
        self._build_frame()
    
    def _build_frame(self):
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.pack(fill=ctk.X, padx=20, pady=(20, 10))
        
        ctk.CTkLabel(self.frame_input, text="Login to your SoggyStreams Account:").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_username = ctk.CTkEntry(self.frame_input, placeholder_text="Username")
        self.entry_username.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.entry_password = ctk.CTkEntry(self.frame_input, placeholder_text="Password", show="*")
        self.entry_password.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.btn_create = ctk.CTkButton(self.frame_input, 
                                        text="Make an account here",
                                        command = self._open_signup)
        self.btn_create.grid(row=3, column=0, padx=10, pady=10, sticky="ew")     
        
        
    

class Signup:
    def __init__(self):
        super().__init__()
        self.title("Sign up to SoggyStreams")
        self.geometry("600x600")
        self.resizable(True, True)
    
    def _build_ui(self):
        self._build_frame()
    
    def _build_frame(self):

""" LOGIN UI"""
## big label "login"
# box for user and pass
# login button - verif load from csv

""" SIGN UP UI """
# sign up button - basic and premium plan - make a profile - option to make more profiles at the home screen
# profile options - adult and child
# prompt for email/username, password and confirm password, and then save to csv
# login UI

"""WHATS NEEDED BACKEND"""
# csv file for saving credentials (username, password, plan, payment, no. and name of profiles)

