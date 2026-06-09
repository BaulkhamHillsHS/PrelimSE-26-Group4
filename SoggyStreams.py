import customtkinter as ctk
import tkinter as tk
import os
import csv

class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SoggyStreams")
        self.geometry("600x600")
        self.resizable(True, True)
        self._build_ui()
        self.minsize(400, 300)

    def _build_ui(self):
        self._build_frame()
    
    def _build_frame(self):
        # self.configure(fg_color = "dark blue") #configures background colour
        self.frame_input = ctk.CTkFrame(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)  
        
        ctk.CTkLabel(self.frame_input, text="SoggyStreams", font=("Arial", 24, "bold")).grid(row=0, column=1, padx=10, pady=10, sticky="n")
        ctk.CTkLabel(self.frame_input, text="Login to your SoggyStreams account:", font=("Arial", 14, "bold")).grid(row=1, column=1, padx=10, pady=10, sticky="n")

        self.entry_username = ctk.CTkEntry(self.frame_input, width = 300, placeholder_text="Username")
        self.entry_username.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.entry_password = ctk.CTkEntry(self.frame_input, placeholder_text="Password", show="*")
        self.entry_password.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.btn_create = ctk.CTkButton(self.frame_input,
                                        text="Login", 
                                        command = self._verif
                                        )
        self.btn_create.grid(row=4, column=1, padx=10, pady=10, sticky="ew") #change weighting to allow this button to move independently  
    def _verif(self):
        with open('data.csv', 'r') as csv_file:
            pass
        
class UserRecord:
    
    FIELDS = ["username", "password", "profiles", "plan"] #column names used in CSV
    
    # def save_to_csv(self, filepath):
    # amendments to plan and profiles

# make a csv, with the pre defined login details
# then, check against the csv, to confirm details
# then, verify details and let the user in

class HomePage:
    def __init__(self):
        super().__init__()
        self.title("SoggyStreams")
        self.geometry("600x600")
        self.resizable(True, True)
        self._build_ui()
        self.minsize(400, 300)
    
    def _build_ui(self):
        self._build_frame()
        
    def _build_frame(self):
        # self.configure(fg_color = "dark blue") #configures background colour
        self.frame_input = ctk.CTkFrame(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)
        
        ctk.CTkLabel(self.frame_input, text="SoggyStreams", font=("Arial", 24, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="ne")
        
        self.btn_settings = ctk.CTkButton(self.frame_input,
                                        text="My Settings", 
                                        command = self.openSettings
                                        )
        
        self.btn_search = ctk.CTkButton(self.frame_input,
                                        text="Search", 
                                        command = self._openSearch
                                        )
        
        
    def openSearch(self):
        # serach, watchlist
        self.frame_input = ctk.CTkFrame(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)
        self.searchBar = ctk.CTkComboBox(self, values=["Dog", "Cat", "Rabbit"])
    def openSettings(self):
        # profiles, subs, updaet pay info, ?
        pass
    

if __name__ == "__main__":     
    app = Login()
    app.mainloop()








  
"""
class Signup:
    def __init__(self):
        super().__init__()
        self.title("Sign up to SoggyStreams")
        self.geometry("600x600")
        self.resizable(True, True)
    
    def _build_ui(self):
        self._build_frame()
    
    def _build_frame(self):
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkEntry(self.frame_input, placeholder_text="Enter", show="*")
        self.textbox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.textbox.insert("0.0", "Sign up here!\n" * 1)
        """

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
