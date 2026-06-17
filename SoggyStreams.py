import customtkinter as ctk
import tkinter as tk
import os
import csv
import smtplib
from smtplib import SMTP
from email.message import EmailMessage
import random
from PIL import Image # may need to pip install pillow for this to wrok (its for images)

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
        self.configure(fg_color = "#0A4163") #configures background colour
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
                                        command = self.openSearch,
                                        fg_color="#CC5404",
                                        hover_color="#853601"
                                        )
        self.btn_create.grid(row=4, column=1, padx=10, pady=10, sticky="ew") #change weighting to allow this button to move independently  
        
    def _verif(self):
        with open('userdata.csv', 'r') as csv_file:
            data = csv.DictReader(csv_file)
            # for row in data:
            #     if 
            pass
        
class UserRecord:
    
    FIELDS = ["username", "password", "profiles", "plan"] #column names used in CSV
    
    def __init__(self):
        self._users = [] # private - encapsulation
    



# def save_to_csv(self, filepath):
# amendments to plan and profiles

# make a csv, with the pre defined login details
# then, check against the csv, to confirm details
# then, verify details and let the user in

class HomePage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SoggyStreams")
        self.geometry("800x800")
        self.resizable(True, True)
        self._build_ui()
        self.minsize(400, 300)
        self.configure(fg_color="#9C9C9C")
    def _build_ui(self):
        self._build_frame()
        
    def _build_frame(self):
        # self.configure(fg_color = "dark blue") #configures background colour
        self.frame_input = ctk.CTkFrame(self, fg_color="#707070")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)
        
        ctk.CTkLabel(self.frame_input, text="SoggyStreams", text_color="#12173B", font=("Comic Sans MS", 24, "bold")).grid(row=0, column=0, padx=100, pady=100, sticky="ne")
        
        self.btn_settings = ctk.CTkButton(self.frame_input,
                                        text="My Settings", 
                                        text_color= "#1B2258",
                                        font = ("Comic Sans MS", 12),
                                        fg_color="#777A8C",
                                        hover_color = "#1B2258",
                                        command = self.openSettings
                                        )
        self.btn_settings.grid(row=1, column=0, padx=100, pady=10, sticky="n")
        
        self.btn_settings.bind(
        "<Enter>",
        lambda e: self.btn_settings.configure(text_color="#777A8C", fg_color = "#1B2258"))
        
        
        self.btn_settings.bind(
        "<Leave>",
        lambda e: self.btn_settings.configure(text_color="#1B2258", fg_color="#777A8C"))
        
        self.btn_search = ctk.CTkButton(self.frame_input,
                                        text="Search", 
                                        text_color= "#1B2258",
                                        font = ("Comic Sans MS", 12,),
                                        fg_color="#777A8C",
                                        hover_color = "#1B2258",
                                        command = self.openSearch
                                        )
        self.btn_search.bind(
        "<Enter>",
        lambda e: self.btn_search.configure(text_color="#777A8C", fg_color = "#1B2258"))
        
        self.btn_search.bind(
        "<Leave>",
        lambda e: self.btn_search.configure(text_color="#1B2258", fg_color = "#777A8C"))
        
        self.btn_search.grid(row=2, column=0, padx=100, pady=(10, 100), sticky="n")
    
    def openSearch(self):  
        # serach, watchlist
        for widget in self.winfo_children():
            widget.destroy()

        # Build new screen
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        
        #self.searchBar = ctk.CTkComboBox(self, values=["Zootopia [G]", "Frozen [PG]", "Spider-Man: No Way Home [M]", "Deadpool [MA15+]", "Titanic [M]", "Wolf on Wall Street [R]", "Ninjago [PG]", "Pokemon [PG]", "The Umbrella Academy [MA15+]"])
        #self.searchBar.grid(row=0, column=0, padx=20, pady=20)
        
        home_btn = ctk.CTkButton(self.frame_input, 
                                text="SoggyStreams", 
                                font = ("Comic Sans MS", 24, "bold"), 
                                fg_color="#000000",
                                hover_color="#000000",
                                command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw") # return home button
        
        ctk.CTkLabel(self.frame_input, text="Search for a movie or TV show:", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.search_entry = ctk.CTkEntry(self.frame_input, width=300, placeholder_text="Search...")
        self.search_entry.grid(row=2, column=0, padx=20, pady=20) # search

        self.search_button = ctk.CTkButton(self.frame_input, 
                                           text="Go", 
                                           text_color= "#1B2258",
                                            font = ("Comic Sans MS", 12,),
                                            fg_color="#777A8C",
                                            hover_color = "#1B2258",
                                           command=self.run_search)
        self.search_button.grid(row=2, column=1, padx=10, pady=20)
    def run_search(self):
        query = self.search_entry.get()
        watches = ["Zootopia [G]", "Frozen [PG]", "Spider-Man: No Way Home [M]", "Deadpool [MA15+]", "Titanic [M]", "Wolf on Wall Street [R]", "Ninjago [PG]", "Pokemon [PG]", "The Umbrella Academy [MA15+]"]
        watches2 = ["zootopia", "frozen", "spidermannowayhome", "deadpool", "titanic", "wolfonwallstreet", "ninjago", "pokemon", "theumbrellaacademy"]
        searchMatches = 3
        for i, watch in enumerate(watches2):
            if query.lower().replace(" ", "").replace("-", "") in watch: #eliminating spaces for ease of search and ignoring typos (with spaces) etc.
                self.search_results_button = ctk.CTkButton(self.frame_input, text=watches[i], command=lambda m=watches[i]: self.play_movie(m))
                self.search_results_button.grid(row=searchMatches, column=0, padx=10, pady=20)
                searchMatches += 1 # for the column of the search resutlts to stack down properly
    
    def play_movie(self, movie):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.frame_input, text=f"Now playing: {movie}", font=("Arial", 18)).grid(row=0, column=0, padx=20, pady=20) 
        #placeholder
        ctk.CTkButton(self.frame_input, text="Return Home", command=self.return_home).grid(row=1, column=0, padx=10, pady=20)
        
    def return_home(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._build_frame()
    
    def openSettings(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="#CC5404",
                                 hover_color="#853601",
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Settings", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Manage Profiles", fg_color="#CC5404", hover_color="#853601", command=self.manage_profiles).grid(row=2, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Subscription Details", fg_color="#CC5404", hover_color="#853601", command=self.subscription_details).grid(row=3, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Update Payment Information", fg_color="#CC5404", hover_color="#853601", command=self.update_payment_info).grid(row=4, column=0, padx=10, pady=10)
        
        # profiles, subs, updaet pay info, ?
    def subscription_details(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, text="SoggyStreams", font = ("Comic Sans MS", 24, "bold"), fg_color="#000000", hover_color="#000000", command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Subscription Details", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        # HI BRYAN you need to load details from csv and display here    
    def update_payment_info(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="#CC5404",
                                 hover_color="#853601",
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Update Payment Information", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        # HI BRYAN you need to load current payment details from csv and display here, with the option to update them and save to csv
    
    def manage_profiles(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="#CC5404",
                                 hover_color="#853601",
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Select a profile:", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        # HI BRYAN - you needa load profiles from csv and display them here, with the option to select one and then move to the home screen with that profile's details (plan, watchlist etc.)
        #ALSO - needa able to delete profiles and edit accordingly
        
        create_profile_btn = ctk.CTkButton(self.frame_input, text="Create New Profile",  fg_color="#CC5404",
                                        hover_color="#853601", command=self.create_profile)
        create_profile_btn.grid(row=2, column=0, padx=10, pady=10)
    def create_profile(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, text="SoggyStreams", font = ("Comic Sans MS", 24, "bold"), fg_color="#CC5404",
                                        hover_color="#853601", command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Create a new profile:", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkEntry(self.frame_input, width=300, placeholder_text="Profile Name").grid(row=2, column=0, padx=20, pady=20)
        ctk.CTkComboBox(self.frame_input, values=["Adult", "Child"]).grid(row=3, column=0, padx=20, pady=10)
        ctk.CTkButton(self.frame_input, text="Create Profile", fg_color="#CC5404",
                                        hover_color="#853601").grid(row=4, column=0, padx=10, pady=10)
        # need to add a command to actually craete proifle to csv

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()






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
            self.configure(fg_color = "#0A4163") #configures background colour
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
                                            command = self.openSearch,
                                            fg_color="#CC5404",
                                            hover_color="#853601"
                                            )
            self.btn_create.grid(row=4, column=1, padx=10, pady=10, sticky="ew") #change weighting to allow this button to move independently  
            
        def _verif(self):
            with open('userdata.csv', 'r') as csv_file:
                data = csv.DictReader(csv_file)
                # for row in data:
                #     if 
                pass
            
    class UserRecord(ctk.CTk):
        
        FIELDS = ["username", "password", "profiles", "plan"] #column names used in CSV
        
        def __init__(self):
            self._users = [] # private - encapsulation
            ctk.CTkLabel(self.frame_input, text="SoggyStreams", font=("Arial", 24, "bold")).grid(row=0, column=1, padx=10, pady=10, sticky="n")
            ctk.CTkLabel(self.frame_input, text="Login to your SoggyStreams account:", font=("Arial", 14, "bold")).grid(row=1, column=1, padx=10, pady=10, sticky="n")

            self.entry_username = ctk.CTkEntry(self.frame_input, width = 300, placeholder_text="Username")
            self.entry_username.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

            self.entry_password = ctk.CTkEntry(self.frame_input, placeholder_text="Password", show="*")
            self.entry_password.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
            
            self.btn_create = ctk.CTkButton(self.frame_input,
                                            text="Login", 
                                            command = self._verif,
                                            fg_color="#CC5404",
                                            hover_color="#853601"
                                            )
            self.btn_create.grid(row=4, column=1, padx=10, pady=10, sticky="ew") #change weighting to allow this button to move independently  
    
    def _verif(self): #add reveal password feature?
        username = self.entry_username.get() #takes username from user input into username box
        password = self.entry_password.get() #takes password from password input

        with open('userdata.csv', 'r') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                if username == row['username'] and password == row['password']:
                    print('Login Successful')
                    return True
                else:
                    print('Invalid credentials')
                    return False
    
        

        
    
    
    
    
    def _twofactorsend(self, recipients): 
        six_int_code = random.randint(100000,999999)
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465) #establishes sending connection on SMTP's port 465
        email = 'your_email@example.com' #sender email (make a new gmail)
        app_password = 'your_app_password'  #sender 2FA password (obtain from new gmail)
        s.login(email, app_password) 
        
        for recipient in recipients:
            msg = EmailMessage()
            msg.set_content(f'Your SoggyStreams 2FA code is: {six_int_code}')
            msg['Subject'] = 'SoggyStreams Verification Code' 
            msg['From'] = email 
            msg['To'] = recipient
            s.send_message(msg)
    
        s.quit()
        recipients = ['recipient1@example.com', 'recipient2@example.com'] #Recipients of the 2FA, need to change to verifier email/username
        self._twofactorsend(recipients)



    # def save_to_csv(self, filepath):
    # amendments to plan and profiles

    # make a csv, with the pre defined login details
    # then, check against the csv, to confirm details
    # then, verify details and let the user in

    class HomePage(ctk.CTk):
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
                                            command = self.openSearch
                                            )
        
        def openSearch(self):  
            # serach, watchlist
            for widget in self.winfo_children():
                widget.destroy()

            # Build new screen
            self.frame_input = ctk.CTkFrame(self)
            self.frame_input.grid(row=0, column=0, sticky="nsew")
            
            #self.searchBar = ctk.CTkComboBox(self, values=["Zootopia [G]", "Frozen [PG]", "Spider-Man: No Way Home [M]", "Deadpool [MA15+]", "Titanic [M]", "Wolf on Wall Street [R]", "Ninjago [PG]", "Pokemon [PG]", "The Umbrella Academy [MA15+]"])
            #self.searchBar.grid(row=0, column=0, padx=20, pady=20)
            
            self.search_entry = ctk.CTkEntry(self.frame_input, width=300, placeholder_text="Search...")
            self.search_entry.grid(row=0, column=0, padx=20, pady=20)

            self.search_button = ctk.CTkButton(self.frame_input, text="Go", command=self.run_search)
            self.search_button.grid(row=0, column=1, padx=10, pady=20)
        def run_search(self):
            query = self.search_entry.get()
            watches = ["Zootopia [G]", "Frozen [PG]", "Spider-Man: No Way Home [M]", "Deadpool [MA15+]", "Titanic [M]", "Wolf on Wall Street [R]", "Ninjago [PG]", "Pokemon [PG]", "The Umbrella Academy [MA15+]"]
            watches2 = ["zootopia", "frozen", "spidermannowayhome", "deadpool", "titanic", "wolfonwallstreet", "ninjago", "pokemon", "theumbrellaacademy"]
            searchMatches = 1
            for i, watch in enumerate(watches2):
                if query.lower().replace(" ", "").replace("-", "") in watch:
                    self.search_results_button = ctk.CTkButton(self.frame_input, text=watches[i], command=lambda m=watches[i]: self.play_movie(m))
                    self.search_results_button.grid(row=searchMatches, column=0, padx=10, pady=20)
                    searchMatches += 1
        
        def play_movie(self, movie):
            for widget in self.winfo_children():
                widget.destroy()
            self.frame_input = ctk.CTkFrame(self)
            self.frame_input.grid(row=0, column=0, sticky="nsew")
            ctk.CTkLabel(self.frame_input, text=f"Now playing: {movie}", font=("Arial", 18)).grid(row=0, column=0, padx=20, pady=20)
            ctk.CTkButton(self.frame_input, text="Return Home", command=self.return_home).grid(row=1, column=0, padx=10, pady=20)
            
        def return_home(self):
            for widget in self.winfo_children():
                widget.destroy()
            self._build_frame()
        
            
        def openSearch(self):
            # serach, watchlist
            for widget in self.winfo_children():
                widget.destroy()

            # Build new screen
            self.frame_input = ctk.CTkFrame(self)
            self.frame_input.grid(row=0, column=0, sticky="nsew")
            self.searchBar = ctk.CTkComboBox(self, values=["Zootopia [G]", "Frozen [PG]", "Spider-Man: No Way Home [M]", "Deadpool [MA15+]", "Titanic [M]", "Wolf on Wall Street [R]", "Ninjago [PG]", "Pokemon [PG]", "The Umbrella Academy [MA15+]"])
            self.searchBar.grid(row=0, column=0, padx=20, pady=20)
        
        def openSettings(self):
            for widget in self.winfo_children():
                widget.destroy()
            self.frame_input = ctk.CTkFrame(self)
            self.frame_input.grid(row=0, column=0, sticky="nsew")
            # profiles, subs, updaet pay info, ?
        

if __name__ == "__main__":
    def openSearch(self):
        # serach, watchlist
        self.frame_input = ctk.CTkFrame(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)
        self.searchBar = ctk.CTkComboBox(self, values=["Zootopia [G]", "Frozen [PG]", "Spider-Man: No Way Home [M]", "Deadpool [MA15+]", "Titanic [M]", "Wolf on Wall Street [R]", "Ninjago [PG]", "Pokemon [PG]", "The Umbrella Academy [MA15+]"])
        # profiles, subs, updaet pay info, ?


#if __name__ == "__main__":     
#    app = SoggyStreams()
#    app.mainloop()
  
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