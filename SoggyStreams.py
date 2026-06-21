import customtkinter as ctk
import tkinter as tk
import os
import csv
import smtplib
from smtplib import SMTP
from email.message import EmailMessage
import random
import bcrypt
from datetime import datetime
# from PIL import Image # may need to pip install pillow for this to wrok (its for images)

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
        self.configure(fg_color = "#072E46") #configures background colour 
        self.frame_input = ctk.CTkFrame(self) #configures frame colour
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)  
        
        ctk.CTkLabel(self.frame_input, text="SoggyStreams", font=("Arial", 24, "bold")).grid(row=0, column=1, padx=10, pady=10, sticky="n")
        ctk.CTkLabel(self.frame_input, text="Login to your SoggyStreams account:", font=("Arial", 14, "bold")).grid(row=1, column=1, padx=10, pady=10, sticky="n")

        self.entry_username = ctk.CTkEntry(self.frame_input, width = 300, placeholder_text="Username or email")
        self.entry_username.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.entry_password = ctk.CTkEntry(self.frame_input, placeholder_text="Password", show="*")
        self.entry_password.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.btn_create = ctk.CTkButton(self.frame_input,
                                        text="Login", 
                                        command = self._verif,
                                        fg_color="#CC5404",
                                        hover_color="#853601"
                                        )
        self.btn_create.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        
    def _verif(self):
        username = self.entry_username.get() #takes username from user input into username box
        password = self.entry_password.get() #takes password from password input
        email = self.entry_username.get()
        
        with open('userdata.csv', 'r') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                if username == row['username'] or email == row['email']:
                    stored_hash = row['password'].encode('utf-8') #encrypt using bcrypt
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                        self.destroy()
                        app = HomePage(user_logged_in=username, email_logged_in=email, password_logged_in=password)
                        app.mainloop()
                        return 
                    
            print('Invalid credentials')
            return False
        
    
class twofactorpage(ctk.CTk): 
    def __init__(self):
        super().__init__()
        self.title("SoggyStreams")
        self.geometry("600x600")
        self.resizable(True, True)
        self._build_ui()
        self.minsize(400, 300)
        self.configure(fg_color="#0A4163")
    def _build_ui(self):
        self._build_frame()
    
    def _build_frame(self):
        self.configure(fg_color = "#0A4163") #configures background colour
        self.frame_input = ctk.CTkFrame(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)  
        
        ctk.CTkLabel(self.frame_input, text="Verify your SoggyStreams account:", font=("Arial", 24, "bold")).grid(row=0, column=1, padx=10, pady=10, sticky="n")
        
        self.entry_username = ctk.CTkEntry(self.frame_input, width = 300, placeholder_text="2FA code")
        self.entry_username.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.btn_create = ctk.CTkButton(self.frame_input,
                                        text="Verify", 
                                        # command = self._verif, # link
                                        fg_color="#CC5404",
                                        hover_color="#853601"
                                        )
        self.btn_create.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    def _twofactorsend(self, recipients): 
        six_int_code = random.randint(100000,999999)
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465) #establishes sending connection on SMTP's port 465
        email = 'soggystreamsofficial@gmail.com' #sender email
        app_password = 'ykax vdnb trqu wmhc'  #sender 2FA password
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

class HomePage(ctk.CTk):
    def __init__(self,user_logged_in,email_logged_in,password_logged_in):
        super().__init__()
        self.title("SoggyStreams")
        self.geometry("1200x1000")
        self.resizable(True, True)
        self._build_ui()
        self.minsize(1000, 600)
        self.configure(fg_color="#41190D")
        self.user_logged_in = user_logged_in
        self.email_logged_in = email_logged_in
        self.password_logged_in = password_logged_in
    def _build_ui(self):
        self._build_frame()
        
    def _build_frame(self):
        self.frame_input = ctk.CTkFrame(self, fg_color="transparent") #240E07 #9C9C9C
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)
        
        ctk.CTkLabel(self.frame_input, text="SoggyStreams", text_color="#9C9C9C", font=("Comic Sans MS", 24, "bold")).grid(row=0, column=0, padx=125, pady=100, sticky="n")
        
        self.btn_settings = ctk.CTkButton(self.frame_input,
                                        text="My Settings", 
                                        text_color= "#1B2258",
                                        font = ("Comic Sans MS", 12),
                                        fg_color="#777A8C",
                                        hover_color = "#1B2258",
                                        command = self.openSettings
                                        )
        self.btn_settings.grid(row=1, column=0, padx=125, pady=10, sticky="n")
        
        self.btn_settings.bind(
        "<Enter>",
        lambda e: self.btn_settings.configure(text_color="#777A8C", fg_color = "#1B2258"))
        
        self.btn_settings.bind(
        "<Leave>",
        lambda e: self.btn_settings.configure(text_color="#1B2258", fg_color="#777A8C"))
        
        self.btn_profiles = ctk.CTkButton(self.frame_input,
                                        text="Choose a profile", 
                                        text_color= "#1B2258",
                                        font = ("Comic Sans MS", 12),
                                        fg_color="#777A8C",
                                        hover_color = "#1B2258",
                                        command = self.openProfiles
                                        )
        self.btn_profiles.grid(row=2, column=0, padx=125, pady=10, sticky="n")
        
        self.btn_profiles.bind(
        "<Enter>",
        lambda e: self.btn_profiles.configure(text_color="#777A8C", fg_color = "#1B2258"))
        
        self.btn_profiles.bind(
        "<Leave>",
        lambda e: self.btn_profiles.configure(text_color="#1B2258", fg_color="#777A8C"))
        
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
        
        self.btn_search.grid(row=3, column=0, padx=125, pady=10, sticky="n")
        
        self.btn_logout = ctk.CTkButton(self.frame_input,
                                        text="Log Out", 
                                        text_color= "#1B2258",
                                        font = ("Comic Sans MS", 12,),
                                        fg_color="#777A8C",
                                        hover_color = "#1B2258",
                                        command = self.logout
                                        )
        self.btn_logout.bind(
        "<Enter>",
        lambda e: self.btn_logout.configure(text_color="#777A8C", fg_color = "#1B2258"))
        
        self.btn_logout.bind(
        "<Leave>",
        lambda e: self.btn_logout.configure(text_color="#1B2258", fg_color = "#777A8C"))
        
        self.btn_logout.grid(row=4, column=0, padx=125, pady=10, sticky="n")
        
        self.btn_quit = ctk.CTkButton(self.frame_input,
                                        text="Quit", 
                                        text_color= "#1B2258",
                                        font = ("Comic Sans MS", 12,),
                                        fg_color="#777A8C",
                                        hover_color = "#1B2258",
                                        command = self.openExit
                                        )
        self.btn_quit.bind(
        "<Enter>",
        lambda e: self.btn_quit.configure(text_color="#777A8C", fg_color = "#1B2258"))
        
        self.btn_quit.bind(
        "<Leave>",
        lambda e: self.btn_quit.configure(text_color="#1B2258", fg_color = "#777A8C"))
        
        self.btn_quit.grid(row=5, column=0, padx=125, pady=(10, 100), sticky="n")
    
    def openExit(self):
        self.destroy()
    
    def openProfiles(self):
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
        
        self.backsearch_button = ctk.CTkButton(self.frame_input, 
                                           text="Back", 
                                           text_color= "#1B2258",
                                            font = ("Comic Sans MS", 12,),
                                            fg_color="#1A65CD",
                                            hover_color = "#0D598F",
                                           command=self.exit_search)
        self.backsearch_button.grid(row=4, column=0, padx=10, pady=20)
    
    def exit_search(self):
        self.return_home()
        
    def run_search(self):
        query = self.search_entry.get()
        if query.strip() == "": #makes sure there are no results for an empty search
            return
        self.search_entry.delete(0, 'end') #clears searches
        
        for widget in self.frame_input.winfo_children():
            if widget.grid_info().get('row', 0) >= 3 and widget != self.backsearch_button: #destroys widget between searches, except back button
                widget.destroy()
        watches = ["Zootopia [G]", "Frozen [PG]", "Spider-Man: No Way Home [M]", "Deadpool [MA15+]", "Titanic [M]", "Wolf on Wall Street [R]", "Ninjago [PG]", "Pokemon [PG]", "The Umbrella Academy [MA15+]"]
        watches2 = ["zootopia", "frozen", "spidermannowayhome", "deadpool", "titanic", "wolfonwallstreet", "ninjago", "pokemon", "theumbrellaacademy"]
        searchMatches = 3
        for i, watch in enumerate(watches2):
            if query.lower().replace(" ", "").replace("-", "") in watch: #eliminating spaces for ease of search and ignoring typos (with spaces) etc.
                self.search_results_button = ctk.CTkButton(self.frame_input, text=watches[i], command=lambda m=watches[i]: self.play_movie(m))
                self.search_results_button.grid(row=searchMatches, column=0, padx=10, pady=20)
                searchMatches += 1 # for the column of the search resutlts to stack down properly
        if searchMatches == 3:
            ctk.CTkLabel(self.frame_input, text="No results found.").grid(row=3, column=0, padx=20, pady=10)
            
    def play_movie(self, movie):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.frame_input, text=f"Now playing: {movie}", font=("Arial", 18)).grid(row=0, column=0, padx=20, pady=20) 
        #placeholder
        newviewdict = [] #new list to append
        with open('viewinghistory.csv', 'r') as csv_file:
            csvview = csv.DictReader(csv_file)
            fieldnames = csvview.fieldnames #extract column headers
            for row in csvview:
                if self.user_logged_in == row['username']:
                    row['viewed_movie'] = movie
                newviewdict.append(row) #append all other rows to temporary dict
        with open('viewinghistory.csv', 'w', newline='') as change_csv_file:
            writer = csv.DictWriter(change_csv_file, fieldnames=fieldnames) #passes column names
            writer.writeheader()
            writer.writerows(newviewdict) #copies new information into csv from list
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
        ctk.CTkButton(self.frame_input, text="Back to Home", fg_color="#2B5BC3", hover_color="#2C4EAA", command=self.exit_search).grid(row=5, column=0, padx=10, pady=10)
    
    def subscription_details(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, text="SoggyStreams", font = ("Comic Sans MS", 24, "bold"), fg_color="#000000", hover_color="#000000", command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Subscription Details", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        with open('userdata.csv', 'r') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                if row ["username"] == self.user_logged_in or row ["email"] == self.email_logged_in:
                    self.user_details = dict(row)
                    
        ctk.CTkLabel(self.frame_input, text="Username:", font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text=f"{self.user_details['username']}", font=("Comic Sans MS", 14)).grid(row=2, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Email:", font=("Comic Sans MS", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text=f"{self.user_details['email']}", font=("Comic Sans MS", 14)).grid(row=3, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Password:", font=("Comic Sans MS", 14)).grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.password_label = ctk.CTkLabel(self.frame_input, text="**********", font=("Comic Sans MS", 14))
        self.password_label.grid(row=4, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Reveal Password", font=("Comic Sans MS", 14),command=self.decrypt_password).grid(row=4, column=2, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Change Password", font=("Comic Sans MS", 14),command=self.change_password_page).grid(row=4, column=3, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Current Plan:", font=("Comic Sans MS", 14)).grid(row=5, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text=f"{self.user_details['subscription_plan']}", font=("Comic Sans MS", 14)).grid(row=5, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Change Plan", font=("Comic Sans MS", 14),command=self.change_plan_page).grid(row=5, column=2, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color="#2B5BC3", hover_color="#2C4EAA", command=self.backsettings).grid(row=7, column=0, padx=10, pady=10)
    
    def change_plan_page(self):
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
        ctk.CTkLabel(self.frame_input, text="Current Plan:", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text=f"{self.user_details['subscription_plan']}", font=("Comic Sans MS", 14)).grid(row=1, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Change your plan to:", font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        all_plans = ["Standard", "Premium", "Ultra Premium"]
        available_plans = [plan for plan in all_plans if plan != self.user_details['subscription_plan']]
        self.plan_type = ctk.CTkComboBox(self.frame_input, values=available_plans)
        self.plan_type.grid(row=2, column=1, padx=20, pady=10)
        ctk.CTkLabel(self.frame_input, text="Your card will be automatically billed.", font=("Comic Sans MS", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Save", fg_color="#D46C22", hover_color="#B06714", command=self.save_plan).grid(row=4, column=0, padx=10, pady=10) 
        ctk.CTkButton(self.frame_input, text="Back", fg_color="#2B5BC3", hover_color="#2C4EAA", command=self.subscription_details).grid(row=5, column=0, padx=10, pady=10) 

    def save_plan(self):
        new_plan = self.plan_type.get()
        print('Success! Plan changed.')
        newplandict = [] #new list to append
        with open('userdata.csv', 'r') as csv_file:
            csvplan = csv.DictReader(csv_file)
            fieldnames = csvplan.fieldnames #extract column headers
            for row in csvplan:
                if self.user_logged_in == row['username'] or self.email_logged_in == row['email']:
                    row['subscription_plan'] = new_plan
                newplandict.append(row) #append all other rows to temporary dict
        with open('userdata.csv', 'w', newline='') as change_csv_file:
            writer = csv.DictWriter(change_csv_file, fieldnames=fieldnames) #passes column names
            writer.writeheader()
            writer.writerows(newplandict) #copies new information into csv from list
        self.subscription_details()
    
    def decrypt_password(self):
        self.password_label.configure(text=self.user_details['original_password'])
    
    def change_password_page(self):
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
        ctk.CTkLabel(self.frame_input, text="Enter your old password:", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Enter your new password:", font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Confirm your new password:", font=("Comic Sans MS", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.oldpasswordinput = ctk.CTkEntry(self.frame_input, placeholder_text="Old password", font=("Comic Sans MS", 14), width= 300)
        self.oldpasswordinput.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.newpasswordinput1 = ctk.CTkEntry(self.frame_input, placeholder_text="New password", font=("Comic Sans MS", 14), width= 300)
        self.newpasswordinput1.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        self.newpasswordinput2 = ctk.CTkEntry(self.frame_input, placeholder_text="New password", font=("Comic Sans MS", 14), width= 300)
        self.newpasswordinput2.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        self.confirmnumberchange = ctk.CTkButton(self.frame_input, text="Confirm",font=("Comic Sans MS", 14), command=self.checkpasswords)
        self.confirmnumberchange.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color="#2B5BC3", hover_color="#2C4EAA", command=self.subscription_details).grid(row=5, column=0, padx=20, pady=10, sticky="w")

    def checkpasswords(self):
        textboxoldpassword = self.oldpasswordinput.get() #takes the input of the first box
        newpasswordinput1 = self.newpasswordinput1.get() #takes the input of the second box
        newpasswordinput2 = self.newpasswordinput2.get() #takes the input of the third box
        textboxoldpassword = textboxoldpassword.replace(" ", "")
        newpasswordinput1 = newpasswordinput1.replace(" ", "")
        newpasswordinput2 = newpasswordinput2.replace(" ", "")
        if textboxoldpassword == self.password_logged_in and newpasswordinput1 == newpasswordinput2:
            print('Success! Password changed.')
            hashedpassword = bcrypt.hashpw(newpasswordinput1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            newpassworddict = [] #new list to append
            with open('userdata.csv', 'r') as csv_file:
                csvpassword = csv.DictReader(csv_file)
                fieldnames = csvpassword.fieldnames #extract column headers
                for row in csvpassword:
                    if self.user_logged_in == row['username'] or self.email_logged_in == row['email']:
                        row['password'] = hashedpassword #find and replace old password.
                        row['original_password'] = newpasswordinput1  
                    newpassworddict.append(row) #append all other rows to temporary dict
            with open('userdata.csv', 'w', newline='') as change_csv_file:
                writer = csv.DictWriter(change_csv_file, fieldnames=fieldnames) #passes column names
                writer.writeheader()
                writer.writerows(newpassworddict) #copies new information into csv from list
            self.password_logged_in = newpasswordinput1    
            self.subscription_details()
        else:
            print('Invalid input.')
    
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
        with open('userdata.csv', 'r') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                if row ["username"] == self.user_logged_in or row ["email"] == self.email_logged_in:
                    self.user_details = dict(row)
        ctk.CTkLabel(self.frame_input, text="Current Payment Information:", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Card Number:", font=("Comic Sans MS", 14))
        self.cardno_label = ctk.CTkLabel(self.frame_input, text="****************", font=("Comic Sans MS", 14))
        self.cardno_label.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.updatecard_no = ctk.CTkButton(self.frame_input, text="Update Card Number", font=("Comic Sans MS", 14), command=self.updatecardnumber)
        self.updatecard_no.grid(row=1, column=2, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Card Expiry:", font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.cardexp_label = ctk.CTkLabel(self.frame_input, text="****", font=("Comic Sans MS", 14))
        self.cardexp_label.grid(row=2, column=1, padx=20, pady=10, sticky="w")  
        self.updateexp_no = ctk.CTkButton(self.frame_input, text="Update Card Expiry", font=("Comic Sans MS", 14), command=self.updatecardexpiry)
        self.updateexp_no.grid(row=2, column=2, padx=20, pady=10, sticky="w")      
        ctk.CTkLabel(self.frame_input, text="Card CVV:", font=("Comic Sans MS", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.cardcvv_label = ctk.CTkLabel(self.frame_input, text="***", font=("Comic Sans MS", 14))
        self.cardcvv_label.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        self.updatecvv_no = ctk.CTkButton(self.frame_input, text="Update CVV", font=("Comic Sans MS", 14), command=self.updatecardcvv)
        self.updatecvv_no.grid(row=3, column=2, padx=20, pady=10, sticky="w")  
        self.revealpay_label = ctk.CTkButton(self.frame_input, text="Reveal all payment information",font=("Comic Sans MS", 14),command=self.revealpay)
        self.revealpay_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color="#2B5BC3", hover_color="#2C4EAA", command=self.backsettings).grid(row=5, column=0, padx=10, pady=10)
    
    def backsettings(self):
        self.openSettings()
    
    def revealpay(self): 
        self.cardno_label.configure(text=self.user_details['card_number']) 
        self.cardexp_label.configure(text=self.user_details['card_exp'])
        self.cardcvv_label.configure(text=self.user_details['card_cvv'])
    
    def updatecardnumber(self):
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
        ctk.CTkLabel(self.frame_input, text="Enter your new card number:", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Confirm card number:", font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.newcardnumber1 = ctk.CTkEntry(self.frame_input, placeholder_text="New card number", font=("Comic Sans MS", 14), width= 300)
        self.newcardnumber1.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.newcardnumber2 = ctk.CTkEntry(self.frame_input, placeholder_text="Confirm new card number", font=("Comic Sans MS", 14), width= 300)
        self.newcardnumber2.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        self.confirmnumberchange = ctk.CTkButton(self.frame_input, text="Confirm",font=("Comic Sans MS", 14), command=self.checkcardnumbers)
        self.confirmnumberchange.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color="#2B5BC3", hover_color="#2C4EAA", command=self.backpayment).grid(row=4, column=0, padx=20, pady=10, sticky="w")
    
    def backpayment(self):
        self.update_payment_info()
        
    def checkcardnumbers(self):
        textboxcardno1 = self.newcardnumber1.get() #takes the input of the first card number box
        textboxcardno2 = self.newcardnumber2.get() #takes the input of the second card number box
        textboxcardno1 = textboxcardno1.replace(" ", "")
        textboxcardno2 = textboxcardno2.replace(" ", "")
        if len(textboxcardno1) == 16 and len(textboxcardno2) == 16 and textboxcardno1.isdigit() and textboxcardno2.isdigit() and textboxcardno1 == textboxcardno2:
            print('Success! Card number changed.')
            newcardnodict = [] #new list to append
            with open('userdata.csv', 'r') as csv_file:
                csvcardno = csv.DictReader(csv_file)
                fieldnames = csvcardno.fieldnames #extract column headers
                for row in csvcardno:
                    if self.user_logged_in == row['username'] or self.email_logged_in == row['email']:
                        row['card_number'] = textboxcardno1 #find and replace old card no.
                    newcardnodict.append(row) #append all other rows to temporary dict
            with open('userdata.csv', 'w', newline='') as change_csv_file:
                writer = csv.DictWriter(change_csv_file, fieldnames=fieldnames) #passes column names
                writer.writeheader()
                writer.writerows(newcardnodict) #copies new information into csv from list
                    
            self.update_payment_info()
        else:
            print('Invalid input.')

    def updatecardexpiry(self):
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
        ctk.CTkLabel(self.frame_input, text="Enter your new card expiry date:", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Confirm card expiry:", font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.newcardexpiry1 = ctk.CTkEntry(self.frame_input, placeholder_text="New card expiry", font=("Comic Sans MS", 14), width= 300)
        self.newcardexpiry1.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.newcardexpiry2 = ctk.CTkEntry(self.frame_input, placeholder_text="Confirm new card expiry", font=("Comic Sans MS", 14), width= 300)
        self.newcardexpiry2.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Note: Please enter your card expiry as a four digit number, without spaces or slashes. Enter in MM/YY format.", font=("Comic Sans MS", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.confirmexpirychange = ctk.CTkButton(self.frame_input, text="Confirm",font=("Comic Sans MS", 14), command=self.checkcardexpiry)
        self.confirmexpirychange.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color="#2B5BC3", hover_color="#2C4EAA", command=self.backpayment).grid(row=5, column=0, padx=20, pady=10, sticky="w")

    def checkcardexpiry(self):
        textboxcardexp1 = self.newcardexpiry1.get() #takes the input of the first card expiry box
        textboxcardexp2 = self.newcardexpiry2.get() #takes the input of the second card expiry box
        textboxcardexp1 = textboxcardexp1.replace(" ", "")
        textboxcardexp2 = textboxcardexp2.replace(" ", "")
        if len(textboxcardexp1) == 4 and len(textboxcardexp2) == 4 and textboxcardexp1.isdigit() and textboxcardexp2.isdigit() and textboxcardexp1 == textboxcardexp2:
            month = textboxcardexp1[:2] #splits first two integers into months
            year = textboxcardexp1[2:] #splits second two integers into years
            month = int(month)
            year = int("20" + textboxcardexp1[2:]) #makes year valid
            now = datetime.now() #import current date
            if month < 1 or month > 12: #impossible month case
                print('Invalid month.')
            elif year < now.year or (year == now.year and month < now.month): #past date
                print('Card is expired.')
            else:
                print('Success! Card expiry changed.')
                slashed_expiry = textboxcardexp1[:2] + "/" + textboxcardexp1[2:]
                newcardexpdict = [] #new list to append
                with open('userdata.csv', 'r') as csv_file:
                    csvcardexp = csv.DictReader(csv_file)
                    fieldnames = csvcardexp.fieldnames #extract column headers
                    for row in csvcardexp:
                        if self.user_logged_in == row['username'] or self.email_logged_in == row['email']:
                            row['card_exp'] = slashed_expiry #find and replace old exp no.
                        newcardexpdict.append(row) #append all other rows to temporary dict
                with open('userdata.csv', 'w', newline='') as change_csv_file:
                    writer = csv.DictWriter(change_csv_file, fieldnames=fieldnames) #passes column names
                    writer.writeheader()
                    writer.writerows(newcardexpdict) #copies new information into csv from list
                self.update_payment_info()
        else:
            print('Invalid input.')
    
    def updatecardcvv(self):
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
        ctk.CTkLabel(self.frame_input, text="Enter your new CVV", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Confirm CVV:", font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.newcvvnumber1 = ctk.CTkEntry(self.frame_input, placeholder_text="New CVV", font=("Comic Sans MS", 14), width= 300)
        self.newcvvnumber1.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.newcvvnumber2 = ctk.CTkEntry(self.frame_input, placeholder_text="Confirm new CVV", font=("Comic Sans MS", 14), width= 300)
        self.newcvvnumber2.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        self.confirmcvvchange = ctk.CTkButton(self.frame_input, text="Confirm",font=("Comic Sans MS", 14),command=self.checkcardcvv)
        self.confirmcvvchange.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color="#2B5BC3", hover_color="#2C4EAA", command=self.backpayment).grid(row=4, column=0, padx=20, pady=10, sticky="w")

    def checkcardcvv(self):
        textboxcvvno1 = self.newcvvnumber1.get() #takes the input of the first card CVV box
        textboxcvvno2 = self.newcvvnumber2.get() #takes the input of the second card CVV box
        textboxcvvno1 = textboxcvvno1.replace(" ", "")
        textboxcvvno2 = textboxcvvno2.replace(" ", "")
        if len(textboxcvvno1) == 3 and len(textboxcvvno2) == 3 and textboxcvvno1.isdigit() and textboxcvvno2.isdigit() and textboxcvvno1 == textboxcvvno2:
            print('Success! Card CVV changed.')
            newcardcvvdict = [] #new list to append
            with open('userdata.csv', 'r') as csv_file:
                csvcvvno = csv.DictReader(csv_file)
                fieldnames = csvcvvno.fieldnames #extract column headers
                for row in csvcvvno:
                    if self.user_logged_in == row['username'] or self.email_logged_in == row['email']:
                        row['card_cvv'] = textboxcvvno1 #find and replace old cvv no.
                    newcardcvvdict.append(row) #append all other rows to temporary dict
            with open('userdata.csv', 'w', newline='') as change_csv_file:
                writer = csv.DictWriter(change_csv_file, fieldnames=fieldnames) #passes column names
                writer.writeheader()
                writer.writerows(newcardcvvdict) #copies new information into csv from list
                
            self.update_payment_info()
        else:
            print('Invalid input.')
        
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
        ctk.CTkButton(self.frame_input, text="Edit Profiles", font=("Comic Sans MS", 14), command=self.editprofiles).grid(row=1, column=1, padx=20, pady=10, sticky="w")
        
        self.user_profile_lst = []
        with open('userprofiles.csv', 'r') as csv_file:
            profilereader = csv.DictReader(csv_file)
            for row in profilereader:
                if row ["username"] == self.user_logged_in:
                    self.user_profile_lst.append(row['profile_name'])
        for i, profile in enumerate (self.user_profile_lst):
            ctk.CTkButton(self.frame_input, text=profile, font=("Comic Sans MS", 14), command=self.profileclicked).grid(row=i+2, column=0, padx=10, pady=10)
         
        self.user_proftyp_lst = []
        with open('userprofiles.csv', 'r') as csv_file:
            proftypreader = csv.DictReader(csv_file)
            for row in proftypreader:
                if row ["username"] == self.user_logged_in:
                    self.user_proftyp_lst.append(row['profile_type'])
        for i, profile_typ in enumerate (self.user_proftyp_lst):
            ctk.CTkLabel(self.frame_input, text=profile_typ, font=("Comic Sans MS", 14)).grid(row=i+2, column=1, padx=10, pady=10)
        
        # BRYAN - needa able to edit name and restriction accordingly
        
        create_profile_btn = ctk.CTkButton(self.frame_input, text="Create New Profile",  fg_color="#CC5404",
                                        hover_color="#853601", command=self.create_profile)
        create_profile_btn.grid(row=99, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Back", fg_color="#2B5BC3", hover_color="#2C4EAA", command=self.backsettings).grid(row=100, column=0, padx=10, pady=10)
    
    def editprofiles(self):
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
        home_btn.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Choose profiles to edit or delete:", font=("Comic Sans MS", 14)).grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="w")
        
        self.user_profile_lst = []
        with open('userprofiles.csv', 'r') as csv_file:
            profilereader = csv.DictReader(csv_file)
            for row in profilereader:
                if row ["username"] == self.user_logged_in:
                    self.user_profile_lst.append(row['profile_name'])
        
        self.check_vars = []
        for i, profile in enumerate (self.user_profile_lst):
            check_var = ctk.StringVar(value="off")
            self.check_vars.append(check_var)
            deletecheckbox = ctk.CTkCheckBox(self.frame_input, text="", width=20,
                         variable=check_var, onvalue="on", offvalue="off")
            deletecheckbox.grid(row=i+2, column=0, padx=10, pady=10, sticky="w")
            ctk.CTkButton(self.frame_input, text=profile, font=("Comic Sans MS", 14), command=self.profileclicked).grid(row=i+2, column=1, padx=10, pady=10)
         
        self.user_proftyp_lst = []
        with open('userprofiles.csv', 'r') as csv_file:
            proftypreader = csv.DictReader(csv_file)
            for row in proftypreader:
                if row ["username"] == self.user_logged_in:
                    self.user_proftyp_lst.append(row['profile_type'])
        for i, profile_typ in enumerate (self.user_proftyp_lst):
            ctk.CTkLabel(self.frame_input, text=profile_typ, font=("Comic Sans MS", 14)).grid(row=i+2, column=2, padx=10, pady=10)
                
        delte_prof_btn = ctk.CTkButton(self.frame_input, text="Delete",  fg_color="#CC5404",
                                        hover_color="#853601", command=self.checkbox_event)
        delte_prof_btn.grid(row=7, column=1, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Back", fg_color="#2B5BC3", hover_color="#2C4EAA", command=self.manage_profiles).grid(row=8, column=1, padx=10, pady=10) 
    
    def checkbox_event(self): 
        to_delete = []
        for i, var in enumerate(self.check_vars):
            if var.get() == "on":
                to_delete.append(self.user_profile_lst[i])
        rows = []
        with open('userprofiles.csv', 'r') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['profile_name'] not in to_delete:
                    rows.append(row)

        with open('userprofiles.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        self.editprofiles()
    
    def profileclicked(self):
        self.destroy()
        app = HomePage(self.user_logged_in,self.email_logged_in,self.password_logged_in)
        app.mainloop()  
    
    def create_profile(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, text="SoggyStreams", font = ("Comic Sans MS", 24, "bold"), fg_color="#CC5404",
                                        hover_color="#853601", command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Create a new profile:", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.prof_name = ctk.CTkEntry(self.frame_input, width=300, placeholder_text="Profile Name")
        self.prof_name.grid(row=2, column=0, padx=20, pady=20)
        self.prof_type = ctk.CTkComboBox(self.frame_input, values=["Adult", "Child"])
        self.prof_type.grid(row=3, column=0, padx=20, pady=10)
        ctk.CTkButton(self.frame_input, text="Create Profile", command=self.save_new_profile, fg_color="#CC5404",
                                        hover_color="#853601").grid(row=4, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Back", fg_color="#2B5BC3", hover_color="#2C4EAA", command=self.backprofile).grid(row=5, column=0, padx=10, pady=10)
    
    def backprofile(self):
        self.manage_profiles()

    
    def save_new_profile(self):
        newprofname = self.prof_name.get()
        newproftype = self.prof_type.get()
        if newprofname == "":
            return
        with open('userprofiles.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([self.user_logged_in, newprofname, newproftype])
        
        self.manage_profiles()
    
    def logout(self):
        self.destroy()
        app = Login()
        app.mainloop()        

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
