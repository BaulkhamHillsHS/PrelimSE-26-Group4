import customtkinter as ctk
import tkinter as tk
import os
import csv
import smtplib
from smtplib import SMTP
from email.message import EmailMessage
import random
from PIL import ImageTk, Image
import bcrypt
from datetime import datetime

class Content:
    def __init__(self, title, search_key, rating=None, thumbnail=None):
        self.title = title
        self.search_key = search_key
        self.rating = rating
        self.thumbnail = thumbnail

    def get_info(self):
        return self.rating


class Movie(Content):
    def __init__(self, title, search_key, rating=None, length=None, thumbnail=None):
        super().__init__(title, search_key, rating, thumbnail)
        self.length = length

    def get_info(self):
        return f"{self.rating}   {self.length}"


class TVSHOW(Content):
    def __init__(self, title, search_key, rating=None, seasons=0, episodes=0, thumbnail=None):
        super().__init__(title, search_key, rating, thumbnail)
        self.seasons = seasons
        self.episodes = episodes

    def get_info(self):
        return f"{self.rating}   {self.seasons} Seasons   {self.episodes} Episodes"


class Profile:
    def __init__(self, profile_name, profile_type):
        self.profile_name = profile_name
        self.profile_type = profile_type


class Account: #encapsulation of sensitive details (payment)
    def __init__(self, username, email, password, subscription_plan, card_number, card_exp, card_cvv):
        self.username = username
        self.email = email
        self._password = password
        self._card_number = card_number
        self._card_exp = card_exp
        self._card_cvv = card_cvv
        self.subscription_plan = subscription_plan
        self.profiles = []

    def add_profile(self, profile):
        self.profiles.append(profile)

    def get_profile_names(self):
        return [p.profile_name for p in self.profiles]

    def verify_password(self, attempt):
        return bcrypt.checkpw(attempt.encode('utf-8'), self._password.encode('utf-8'))

    def get_masked_card_number(self):
        if not self._card_number or len(self._card_number) < 4:
            return "****"
        return "*" * (len(self._card_number) - 4) + self._card_number[-4:]

    def get_card_number(self):
        return self._card_number

    def get_card_exp(self):
        return self._card_exp

    def get_card_cvv(self):
        return self._card_cvv

    def set_card_number(self, new_number):
        if len(new_number) == 16 and new_number.isdigit():
            self._card_number = new_number
            return True
        return False

    def set_card_exp(self, new_exp):
        self._card_exp = new_exp

    def set_card_cvv(self, new_cvv):
        if len(new_cvv) == 3 and new_cvv.isdigit():
            self._card_cvv = new_cvv
            return True
        return False

# Color scheme
BG = "#05070D"
FRAME = "#0F172A"
PRIMARY = "#1E90FF"
PRIMARY_DARK = "#1565C0"
TEXT = "#E6E6E6"
SUBTEXT = "#AAB4C5"
MID = "#1B2236"
BORDER = "#101A2E"

class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color = BG) #configures background colour 
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME) #configures frame colour
        self.title("SoggyStreams")
        self.geometry("600x600")
        self.resizable(True, True)
        self._build_ui()
        self.minsize(400, 300)

    def _build_ui(self):
        self._build_frame()
    
    def _build_frame(self):
        self.configure(fg_color = BG) #configures background colour 
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME) #configures frame colour
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)  
        
        ctk.CTkLabel(self.frame_input, text="SoggyStreams", text_color=TEXT, font=("Arial", 24, "bold")).grid(row=0, column=1, padx=10, pady=10, sticky="n")
        ctk.CTkLabel(self.frame_input, text="Login to your SoggyStreams account:", text_color=TEXT, font=("Arial", 14, "bold")).grid(row=1, column=1, padx=10, pady=10, sticky="n")

        self.entry_username = ctk.CTkEntry(self.frame_input, width = 300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT, placeholder_text="Username or email")
        self.entry_username.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.entry_password = ctk.CTkEntry(self.frame_input, width=300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT, placeholder_text="Password", show="*")
        self.entry_password.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.btn_create = ctk.CTkButton(self.frame_input,
                                        text="Login", 
                                        command = self._verif,
                                        fg_color=PRIMARY,
                                        hover_color=PRIMARY_DARK,
                                        text_color=TEXT
                                        )
        self.btn_create.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
    
    def show_error_popup(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x200")
        error_window.configure(fg_color=BG)

        ctk.CTkLabel(error_window, text=message, text_color="#E73636",
                    font=("Arial", 14), wraplength=350).pack(expand=True, padx=20, pady=20)

        ctk.CTkButton(error_window, text="OK", fg_color=PRIMARY, hover_color=PRIMARY_DARK,
                    text_color=TEXT, command=error_window.destroy).pack(pady=10)
    
    def show_success_popup(self, message):
        success_window = ctk.CTkToplevel(self)
        success_window.title("Success")
        success_window.geometry("400x200")
        success_window.configure(fg_color=BG)

        ctk.CTkLabel(success_window, text=message, text_color="#32CD6B",
                     font=("Comic Sans MS", 14), wraplength=350).pack(expand=True, padx=20, pady=20)

        ctk.CTkButton(success_window, text="OK", fg_color=PRIMARY, hover_color=PRIMARY_DARK,
                      text_color=TEXT, command=success_window.destroy).pack(pady=10)
        
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
                        app = twofactorpage(user_logged_in=row['username'], email_logged_in=row['email'], password_logged_in=password)
                        app.mainloop()
                        return 
                    
            self.show_error_popup("Incorrect username/email or password.")
            return False
        
    
class twofactorpage(ctk.CTk): 
    def __init__(self, user_logged_in, email_logged_in, password_logged_in):
        super().__init__()
        self.user_logged_in = user_logged_in
        self.email_logged_in = email_logged_in
        self.password_logged_in = password_logged_in
        self.title("SoggyStreams")
        self.geometry("600x600")
        self.resizable(True, True)
        self._build_ui()
        self.minsize(400, 300)
        self.configure(fg_color=BG)
    def _build_ui(self):
        self._build_frame()
    
    def _build_frame(self):
        self.configure(fg_color = BG) #configures background colour
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)  
        
        ctk.CTkLabel(self.frame_input, text="Verify your SoggyStreams account:", text_color=TEXT, font=("Arial", 24, "bold")).grid(row=0, column=1, padx=10, pady=10, sticky="n")
        ctk.CTkButton(self.frame_input, text="Send 2FA code", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self._twofactorsend).grid(row=1, column=1, padx=10, pady=10, sticky="n")

    def _twofactorsend(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        self.configure(fg_color = BG) #configures background colour
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)  
        
        ctk.CTkLabel(self.frame_input, text="Verify your SoggyStreams account:", text_color=TEXT, font=("Arial", 24, "bold")).grid(row=0, column=1, padx=10, pady=10, sticky="n") 
        self.entry_username = ctk.CTkEntry(self.frame_input, width = 300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT, placeholder_text="2FA code")
        self.entry_username.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.btn_create = ctk.CTkButton(self.frame_input,
                                        text="Verify", 
                                        command = self._2fa_verif,
                                        fg_color=PRIMARY,
                                        hover_color=PRIMARY_DARK,
                                        text_color=TEXT
                                        )
        self.btn_create.grid(row=2, column=1, padx=10, pady=10, sticky="ew") #resend button
        
        self.btn_resend = ctk.CTkButton(self.frame_input,
                                        text="Resend 2FA code", 
                                        command = self._2fa_resend,
                                        fg_color=PRIMARY,
                                        hover_color=PRIMARY_DARK,
                                        text_color=TEXT
                                        )
        self.btn_resend.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        
        self.error_label = ctk.CTkLabel(self.frame_input, text="You may need to check your spam folder.", text_color="#FF6B6B", font=("Arial", 12))
        self.error_label.grid(row=4, column=1, padx=10, pady=10, sticky="n")
        
        self.six_int_code = random.randint(100000,999999)
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465) #establishes sending connection on SMTP's port 465
        email = 'soggystreamsofficial@gmail.com' #sender email
        app_password = 'ykax vdnb trqu wmhc'  #sender 2FA password
        s.login(email, app_password) 
        
        recipients = [f'{self.email_logged_in}'] #Recipients of the 2FA, need to change to verifier email/username
        
        for recipient in recipients:
            msg = EmailMessage()
            msg.set_content(f'Your SoggyStreams 2FA code is: {self.six_int_code}')
            msg['Subject'] = 'SoggyStreams Verification Code' 
            msg['From'] = email 
            msg['To'] = recipient
            s.send_message(msg)
        s.quit()
    
    def _2fa_verif(self):
        user_fa_entered = self.entry_username.get()
        if user_fa_entered == str(self.six_int_code):
            for widget in self.winfo_children():
                widget.destroy()
            self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
            self.frame_input.grid(row=0, column=0, sticky="nsew")

            ctk.CTkLabel(self.frame_input, text="Who's watching?", text_color=TEXT, #heading
                    font=("Comic Sans MS", 20, "bold")).grid(row=0, column=0, padx=20, pady=10, sticky="w")

            profiles = [] #empty lst
            with open('userprofiles.csv', 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    if row["username"] == self.user_logged_in: #find row of currently logged in user and append to find profile name
                        profiles.append(row['profile_name'])

            for i, profile in enumerate(profiles): #create button for each profile currently existing
                ctk.CTkButton(self.frame_input, text=profile, font=("Comic Sans MS", 14),
                            fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT,
                            command=lambda p=profile: self.select_profile(p) 
                            ).grid(row=i+1, column=0, padx=10, pady=10)
        else:
            self.error_label.configure(text="Incorrect code. Please try again.")
    
    def _2fa_resend(self):
        self.six_int_code = random.randint(100000,999999)
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        email = 'soggystreamsofficial@gmail.com'
        app_password = 'ykax vdnb trqu wmhc'
        s.login(email, app_password)
        
        recipients = [f'{self.email_logged_in}']
        
        for recipient in recipients:
            msg = EmailMessage()
            msg.set_content(f'Your SoggyStreams 2FA code is: {self.six_int_code}')
            msg['Subject'] = 'SoggyStreams Verification Code'
            msg['From'] = email
            msg['To'] = recipient
            s.send_message(msg)
        s.quit()
    
    def select_profile(self, profile_name):
        self.destroy()
        app = HomePage(user_logged_in=self.user_logged_in, email_logged_in=self.email_logged_in, password_logged_in=self.password_logged_in)
        app.set_current_profile(profile_name)
        app.return_home()
        app.mainloop()
            

class HomePage(ctk.CTk):
    def __init__(self,user_logged_in,email_logged_in,password_logged_in):
        super().__init__()
        self.title("SoggyStreams")
        self.geometry("1200x1000")
        self.resizable(True, True)
        self.user_logged_in = user_logged_in
        self.email_logged_in = email_logged_in
        self.password_logged_in = password_logged_in
        self.current_profile = None
        self.current_profile_type = None
        self._build_ui()
        self.minsize(1000, 600)
        self.configure(fg_color=BG)
        self.configure(fg_color = BG)
        self.movies = [
            Movie("Zootopia", "zootopia", rating="G", length="1h 48m", thumbnail="Zootopia.jpg"),
            Movie("Frozen", "frozen", rating="PG", length="1h 42m", thumbnail="Frozen.jpg"),
            Movie("Spider-Man: No Way Home", "spidermannowayhome", rating="M", length="2h 28m", thumbnail="Spiderman.jpg"),
            Movie("Deadpool", "deadpool", rating="MA15+", length="1h 48m", thumbnail="Deadpool.jpg"),
            Movie("Titanic", "titanic", rating="M", length="3h 14m", thumbnail="Titanic.jpg")
        ]

        self.tvshows = [
            TVSHOW("Ninjago", "ninjago", rating="PG", seasons="7", episodes="280", thumbnail="Ninjago.jpg"),
            TVSHOW("Pokemon", "pokemon", rating="PG", seasons="9", episodes="718", thumbnail="Pokemon.jpg"),
            TVSHOW("The Umbrella Academy", "theumbrellaacademy", rating="MA15+", seasons = "4", episodes = "36", thumbnail="Umbrella.jpg")
        ]

    def _build_ui(self):
        self._build_frame()
        
    def _build_frame(self):
        
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_input.grid(row=0, column=0)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "SoggyStreams.jpg")
        raw_image = Image.open(image_path) # need to add logo image to folder for this to work
        self.logo_image = ctk.CTkImage(
            light_image=raw_image,
            dark_image=raw_image,
            size=(100, 100)
        )
        image_label = ctk.CTkLabel(self.frame_input, text="", image=self.logo_image)
        image_label.grid(row=1, column=0, padx=125, pady=40, sticky="n")
        
        ctk.CTkLabel(self.frame_input, text="SoggyStreams", text_color=TEXT, font=("Comic Sans MS", 24, "bold")).grid(row=0, column=0, padx=125, pady=(100, 10), sticky="n")
        
        if self.current_profile_type != "Child":
            self.btn_settings = ctk.CTkButton(self.frame_input,
                                            text="My Settings", 
                                            fg_color=PRIMARY,
                                            hover_color=PRIMARY_DARK,
                                            text_color=TEXT,
                                            font = ("Comic Sans MS", 12),
                                            command = self.openSettings
                                            )
            self.btn_settings.grid(row=2, column=0, padx=125, pady=10, sticky="n")
        
        
        self.btn_profiles = ctk.CTkButton(self.frame_input,
                                        text="Change profiles", 
                                        text_color=TEXT,
                                        font = ("Comic Sans MS", 12),
                                        fg_color=PRIMARY,
                                        hover_color=PRIMARY_DARK,
                                        command = self.openProfiles
                                        )
        self.btn_profiles.grid(row=3, column=0, padx=125, pady=10, sticky="n")
     
        self.btn_search = ctk.CTkButton(self.frame_input,
                                        text="Search",
                                        font = ("Comic Sans MS", 12,),
                                        fg_color=PRIMARY,
                                        hover_color=PRIMARY_DARK,
                                        text_color=TEXT,
                                        command = self.openSearch
                                        )
       
        
        self.btn_search.grid(row=4, column=0, padx=125, pady=10, sticky="n")
        
        self.btn_watchlist = ctk.CTkButton(self.frame_input,
                                        text="Your Watchlist",
                                        font = ("Comic Sans MS", 12,),
                                        fg_color=PRIMARY,
                                        hover_color=PRIMARY_DARK,
                                        text_color=TEXT,
                                        command = self.openWatchlist
                                        )
       
        
        self.btn_watchlist.grid(row=5, column=0, padx=125, pady=10, sticky="n")
        
        self.btn_logout = ctk.CTkButton(self.frame_input,
                                        text="Log Out", 
                                        text_color=TEXT,
                                        font = ("Comic Sans MS", 12,),
                                        fg_color=PRIMARY,
                                        hover_color=PRIMARY_DARK,
                                        command = self.logout
                                        )

        
        self.btn_logout.grid(row=6, column=0, padx=125, pady=10, sticky="n")
        
        self.btn_quit = ctk.CTkButton(self.frame_input,
                                        text="Quit", 
                                        text_color=TEXT,
                                        font = ("Comic Sans MS", 12,),
                                        fg_color=PRIMARY,
                                        hover_color=PRIMARY_DARK,
                                        command = self.openExit
                                        )

        
        self.btn_quit.grid(row=7, column=0, padx=125, pady=(10, 100), sticky="n")
    
    def openWatchlist(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")

        home_btn = ctk.CTkButton(self.frame_input,
                                 text="SoggyStreams",
                                 font = ("Comic Sans MS", 24, "bold"),
                                 fg_color="transparent",
                                 hover_color=PRIMARY_DARK,
                                 text_color=TEXT,
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        
        ctk.CTkLabel(self.frame_input, text="My Watchlist", text_color=TEXT,
                     font=("Comic Sans MS", 20, "bold")).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.return_home).grid(row=100, column=0, padx=10, pady=10)

        watchlist_titles = []
        with open('watchlist.csv', 'r') as csv_file: 
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['username'] == self.user_logged_in and row['profile_name'] == self.current_profile:
                    watchlist_titles.append(row['movie_title'])

        if not watchlist_titles:
            ctk.CTkLabel(self.frame_input, text="Your watchlist is empty.", text_color=SUBTEXT).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        else:
            for i, title in enumerate(watchlist_titles):
                item = self.find_content_by_title(title)

                title_btn = ctk.CTkButton(
                    self.frame_input,
                    text=title,
                    fg_color=PRIMARY,
                    hover_color=PRIMARY_DARK,
                    text_color=TEXT,
                    command=lambda m=item: self.play_movie(m)
                )
                title_btn.grid(row=i+2, column=0, padx=10, pady=10)

                remove_btn = ctk.CTkButton(
                    self.frame_input,
                    text="Remove",
                    fg_color=PRIMARY,
                    hover_color=PRIMARY_DARK,
                    text_color=TEXT,
                    command=lambda t=title: self.remove_from_watchlist(t)
                )
                remove_btn.grid(row=i+2, column=1, padx=10, pady=10)
    
    def remove_from_watchlist(self, title):
        rows = []
        with open('watchlist.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames
            for row in reader:
                if not (row['username'] == self.user_logged_in
                        and row['profile_name'] == self.current_profile
                        and row['movie_title'] == title):
                    rows.append(row)

        with open('watchlist.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        self.openWatchlist()
    
    
    def openExit(self):
        self.destroy()
    
    def openProfiles(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="transparent",
                                 hover_color=PRIMARY_DARK,
                                 text_color=TEXT,
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        
        ctk.CTkLabel(self.frame_input, text="Who's watching?", text_color=TEXT, #heading
                 font=("Comic Sans MS", 20, "bold")).grid(row=1, column=0, padx=20, pady=10, sticky="w")

        profiles = []
        with open('userprofiles.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row["username"] == self.user_logged_in: #find row of currently logged in user and append to find profile name
                    profiles.append(row['profile_name'])

        for i, profile in enumerate(profiles): #create button for each profile currently existing
            ctk.CTkButton(self.frame_input, text=profile, font=("Comic Sans MS", 14),
                        fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT,
                        command=lambda p=profile: self.select_profile(p)
                        ).grid(row=i+2, column=0, padx=10, pady=10)

    def select_profile(self, profile_name):
        self.destroy()
        app = HomePage(user_logged_in=self.user_logged_in, email_logged_in=self.email_logged_in, password_logged_in=self.password_logged_in)
        app.set_current_profile(profile_name)
        app.return_home()
        app.mainloop()
        
    def set_current_profile(self, profile_name): #tracks current profile for profile-specific restrictions
        self.current_profile = profile_name
        self.current_profile_type = "Adult"  # safe default if lookup fails
        with open('userprofiles.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['username'] == self.user_logged_in and row['profile_name'] == profile_name:
                    self.current_profile_type = row['profile_type'] #set profile type to found in csv
                    break

    def openSearch(self):  
        # serach, watchlist
        for widget in self.winfo_children():
            widget.destroy()

        # Build new screen
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        
        home_btn = ctk.CTkButton(self.frame_input, 
                                text="SoggyStreams", 
                                font = ("Comic Sans MS", 24, "bold"), 
                                fg_color="transparent",
                                hover_color=PRIMARY_DARK,
                                text_color=TEXT,
                                command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw") # return home button
        
        ctk.CTkLabel(self.frame_input, text="Search for a movie or TV show:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.search_entry = ctk.CTkEntry(self.frame_input, width=300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT, placeholder_text="Search...")
        self.search_entry.grid(row=2, column=0, padx=20, pady=20) # search

        self.search_button = ctk.CTkButton(self.frame_input, 
                                           text="Go", 
                                           text_color=TEXT,
                                            font = ("Comic Sans MS", 12,),
                                            fg_color=PRIMARY,
                                             hover_color=PRIMARY_DARK,
                                           command=self.run_search)
        self.search_button.grid(row=2, column=1, padx=10, pady=20)
        
        self.type_filter = ctk.CTkComboBox(self.frame_input, values=["All", "Movies", "TV Shows"],
                                            fg_color=FRAME, text_color=TEXT, border_color=BORDER)
        self.type_filter.set("All")
        self.type_filter.grid(row=2, column=2, padx=10, pady=20)

        self.rating_filter = ctk.CTkComboBox(self.frame_input, values=["All", "G", "PG", "M", "MA15+"],
                                              fg_color=FRAME, text_color=TEXT, border_color=BORDER)
        self.rating_filter.set("All")
        self.rating_filter.grid(row=2, column=3, padx=10, pady=20)
        
        self.backsearch_button = ctk.CTkButton(self.frame_input, 
                                           text="Back", 
                                           text_color=TEXT,
                                            font = ("Comic Sans MS", 12,),
                                            fg_color=PRIMARY,
                                            hover_color=PRIMARY_DARK,
                                           command=self.exit_search)
        self.backsearch_button.grid(row=100, column=0, padx=10, pady=20)
    
    def exit_search(self):
        self.return_home()
        
    def run_search(self):
        query = self.search_entry.get().strip()

        if query == "":
            return

        # normalize query
        query = query.lower().replace(" ", "").replace("-", "")

        # clear old results (keep UI)
        for widget in self.frame_input.winfo_children():
            info = widget.grid_info()
            if info.get("row", 0) >= 3 and widget != self.backsearch_button:
                widget.destroy()

        results = []

        CHILD_BLOCKED_RATINGS = {"M", "MA15+"} #unaccessable movie ratings

        # search movies
        for movie in self.movies:
            if query in movie.search_key.lower():
                if self.current_profile_type == "Child" and movie.rating in CHILD_BLOCKED_RATINGS:
                    continue
                if self.type_filter.get() == "TV Shows":
                    continue
                if self.rating_filter.get() != "All" and movie.rating != self.rating_filter.get():
                    continue
                results.append(movie)

        # search TV shows
        for show in self.tvshows:
            if query in show.search_key.lower():
                if self.current_profile_type == "Child" and show.rating in CHILD_BLOCKED_RATINGS:
                    continue
                if self.type_filter.get() == "Movies":
                    continue
                if self.rating_filter.get() != "All" and show.rating != self.rating_filter.get():
                    continue
                results.append(show)

        # no results
        if not results:
            ctk.CTkLabel(
                self.frame_input,
                text="No results found.",
                text_color=TEXT
            ).grid(row=3, column=0, padx=20, pady=10)
            return

        row = 3

        for item in results:
            btn = ctk.CTkButton(
                self.frame_input,
                text=item.title,
                fg_color=PRIMARY,
                hover_color=PRIMARY_DARK,
                text_color=TEXT,
                command=lambda m=item: self.play_movie(m)
            )
            btn.grid(row=row, column=0, padx=10, pady=10)

            watchlist_btn = ctk.CTkButton(
                self.frame_input,
                text="+ Watchlist",
                fg_color=PRIMARY,
                hover_color=PRIMARY_DARK,
                text_color=TEXT,
                command=lambda m=item: self.add_to_watchlist(m)
            )
            watchlist_btn.grid(row=row, column=1, padx=10, pady=10)
            row += 1

    def add_to_watchlist(self, item):
        with open('watchlist.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if (row['username'] == self.user_logged_in
                        and row['profile_name'] == self.current_profile
                        and row['movie_title'] == item.title):
                    self.show_error_popup(f"{item.title} is already in your watchlist.") # don't add the same title twice for this profile
                    return

        fieldnames = ['username', 'profile_name', 'movie_title']
        with open('watchlist.csv', 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({
                'username': self.user_logged_in,
                'profile_name': self.current_profile,
                'movie_title': item.title
            })
        print('Added to watchlist.')
        
        
    def play_movie(self, movie_obj):
        # clear screen
        for widget in self.winfo_children():
            widget.destroy()

        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")

        # header container (stacked layout)
        header = ctk.CTkFrame(self.frame_input, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # "Now playing" title
        now_playing = ctk.CTkLabel(
            header,
            text="Now playing:",
            text_color=SUBTEXT,
            font=("Arial", 14)
        )
        now_playing.grid(row=0, column=0, sticky="w")

        # movie title
        title_label = ctk.CTkLabel(
            header,
            text=movie_obj.title,
            text_color=TEXT,
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=1, column=0, pady=(5, 10), sticky="w")

        # thumbnail UNDER title
        if getattr(movie_obj, "thumbnail", None):
            try:
                img = Image.open(movie_obj.thumbnail)
                img = img.resize((180, 260))

                img_ctk = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(180, 260)
                )

                img_label = ctk.CTkLabel(
                    header,
                    image=img_ctk,
                    text=""
                )
                img_label.image = img_ctk
                img_label.grid(row=2, column=0, pady=10, sticky="w")

            except Exception as e:
                print("Thumbnail load failed:", e)

        # info line
        info = movie_obj.get_info()
        ctk.CTkLabel(
            self.frame_input,
            text=info,
            text_color=SUBTEXT
        ).grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        # back button
        ctk.CTkButton(
            self.frame_input,
            text="Return Home",
            fg_color=PRIMARY,
            hover_color=PRIMARY_DARK,
            text_color=TEXT,
            command=self.return_home
        ).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        fieldnames = ['username', 'profile_name', 'viewed_movie', 'timestamp']
        with open('viewinghistory.csv', 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({
                'username': self.user_logged_in,
                'profile_name': self.current_profile,
                'viewed_movie': movie_obj.title,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })          

    def return_home(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._build_frame()
    
    def openSettings(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="transparent",
                                 hover_color=PRIMARY_DARK,
                                 text_color=TEXT,
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Settings", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Manage Profiles", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.manage_profiles).grid(row=2, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Subscription Details", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.subscription_details).grid(row=3, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Update Payment Information", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.update_payment_info).grid(row=4, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Export Viewing History", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.export_viewing_hist).grid(row=5, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Back to Home", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.exit_search).grid(row=6, column=0, padx=10, pady=10)

    def subscription_details(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, text="SoggyStreams", font = ("Comic Sans MS", 24, "bold"), fg_color="transparent", hover_color=PRIMARY_DARK, text_color=TEXT, command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Subscription Details", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        with open('userdata.csv', 'r') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                if row ["username"] == self.user_logged_in or row ["email"] == self.email_logged_in:
                    self.user_details = dict(row)
                    
        ctk.CTkLabel(self.frame_input, text="Username:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text=f"{self.user_details['username']}", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=2, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Email:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text=f"{self.user_details['email']}", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=3, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Password:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.password_label = ctk.CTkLabel(self.frame_input, text="**********", text_color=TEXT, font=("Comic Sans MS", 14))
        self.password_label.grid(row=4, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Reveal Password", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.decrypt_password).grid(row=4, column=2, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Change Password", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.change_password_page).grid(row=4, column=3, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Current Plan:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=5, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text=f"{self.user_details['subscription_plan']}", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=5, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Change Plan", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.change_plan_page).grid(row=5, column=2, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.backsettings).grid(row=7, column=0, padx=10, pady=10)
    
    def change_plan_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="transparent",
                                 hover_color=PRIMARY_DARK,
                                 text_color=TEXT,
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Current Plan:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text=f"{self.user_details['subscription_plan']}", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Change your plan to:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        all_plans = ["Standard", "Premium", "Ultra Premium"]
        available_plans = [plan for plan in all_plans if plan != self.user_details['subscription_plan']]
        self.plan_type = ctk.CTkComboBox(self.frame_input, values=available_plans, fg_color=FRAME, text_color=TEXT, border_color=BORDER)
        self.plan_type.grid(row=2, column=1, padx=20, pady=10)
        ctk.CTkLabel(self.frame_input, text="Your card will be automatically billed.", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Save", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.save_plan).grid(row=4, column=0, padx=10, pady=10) 
        ctk.CTkButton(self.frame_input, text="Back", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.subscription_details).grid(row=5, column=0, padx=10, pady=10)
    

    def save_plan(self):
        new_plan = self.plan_type.get()
        self.generatesubscriptioninvoice()
        self.show_success_popup(f"Your plan has been changed to {new_plan}. An invoice has been generated.")
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
    
    def generatesubscriptioninvoice(self):
        now = datetime.now()
        filename = f"invoice_{self.user_logged_in}_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as invoice:
            invoice.write("SoggyStreams Subscription Invoice\n")
            invoice.write("-" * 40 + "\n")
            invoice.write(f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            invoice.write(f"Username: {self.user_logged_in}\n")
            invoice.write(f"Email: {self.email_logged_in}\n")
            invoice.write("-" * 40 + "\n")
            invoice.write(f"Previous Plan: {self.user_details['subscription_plan']}\n")
            invoice.write(f"New Plan: {self.plan_type.get()}\n")
            invoice.write("-" * 40 + "\n")
            invoice.write(f"Card billed: {self.user_details['card_number']}\n")
            invoice.write("-" * 40 + "\n")
            invoice.write("Thank you for subscribing to SoggyStreams!\n")
    
    def decrypt_password(self):
        self.password_label.configure(text=self.user_details['original_password'])
    
    def change_password_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="transparent",
                                 hover_color=PRIMARY_DARK,
                                 text_color=TEXT,
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Enter your old password:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Enter your new password:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Confirm your new password:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.oldpasswordinput = ctk.CTkEntry(self.frame_input, placeholder_text="Old password", font=("Comic Sans MS", 14), width=300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT)
        self.oldpasswordinput.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.newpasswordinput1 = ctk.CTkEntry(self.frame_input, placeholder_text="New password", font=("Comic Sans MS", 14), width=300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT)
        self.newpasswordinput1.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        self.newpasswordinput2 = ctk.CTkEntry(self.frame_input, placeholder_text="New password", font=("Comic Sans MS", 14), width=300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT)
        self.newpasswordinput2.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        self.confirmnumberchange = ctk.CTkButton(self.frame_input, text="Confirm", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.checkpasswords)
        self.confirmnumberchange.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.subscription_details).grid(row=5, column=0, padx=20, pady=10, sticky="w")

    def checkpasswords(self):
        textboxoldpassword = self.oldpasswordinput.get() #takes the input of the first box
        newpasswordinput1 = self.newpasswordinput1.get() #takes the input of the second box
        newpasswordinput2 = self.newpasswordinput2.get() #takes the input of the third box
        textboxoldpassword = textboxoldpassword.replace(" ", "")
        newpasswordinput1 = newpasswordinput1.replace(" ", "")
        newpasswordinput2 = newpasswordinput2.replace(" ", "")
        if textboxoldpassword == self.password_logged_in and newpasswordinput1 == newpasswordinput2:    
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
            self.show_success_popup("Password successfully changed!")
        else:
            self.show_error_popup("Old password is incorrect, or new passwords don't match.")    
    
    def update_payment_info(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="transparent",
                                 hover_color=PRIMARY_DARK,
                                 text_color=TEXT,
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        with open('userdata.csv', 'r') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                if row ["username"] == self.user_logged_in or row ["email"] == self.email_logged_in:
                    self.user_details = dict(row)
        ctk.CTkLabel(self.frame_input, text="Current Payment Information:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Card Number:", text_color=TEXT, font=("Comic Sans MS", 14))
        self.cardno_label = ctk.CTkLabel(self.frame_input, text="****************", text_color=TEXT, font=("Comic Sans MS", 14))
        self.cardno_label.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.updatecard_no = ctk.CTkButton(self.frame_input, text="Update Card Number", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.updatecardnumber)
        self.updatecard_no.grid(row=1, column=2, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Card Expiry:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.cardexp_label = ctk.CTkLabel(self.frame_input, text="****", text_color=TEXT, font=("Comic Sans MS", 14))
        self.cardexp_label.grid(row=2, column=1, padx=20, pady=10, sticky="w")  
        self.updateexp_no = ctk.CTkButton(self.frame_input, text="Update Card Expiry", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.updatecardexpiry)
        self.updateexp_no.grid(row=2, column=2, padx=20, pady=10, sticky="w")      
        ctk.CTkLabel(self.frame_input, text="Card CVV:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.cardcvv_label = ctk.CTkLabel(self.frame_input, text="***", text_color=TEXT, font=("Comic Sans MS", 14))
        self.cardcvv_label.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        self.updatecvv_no = ctk.CTkButton(self.frame_input, text="Update CVV", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.updatecardcvv)
        self.updatecvv_no.grid(row=3, column=2, padx=20, pady=10, sticky="w")  
        self.revealpay_label = ctk.CTkButton(self.frame_input, text="Reveal all payment information", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.revealpay)
        self.revealpay_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.backsettings).grid(row=5, column=0, padx=10, pady=10)
    
    def backsettings(self):
        self.openSettings()
    
    def revealpay(self): 
        self.cardno_label.configure(text=self.user_details['card_number']) 
        self.cardexp_label.configure(text=self.user_details['card_exp'])
        self.cardcvv_label.configure(text=self.user_details['card_cvv'])
    
    def updatecardnumber(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="transparent",
                                 hover_color=PRIMARY_DARK,
                                 text_color=TEXT,
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Enter your new card number:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Confirm card number:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.newcardnumber1 = ctk.CTkEntry(self.frame_input, placeholder_text="New card number", font=("Comic Sans MS", 14), width=300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT)
        self.newcardnumber1.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.newcardnumber2 = ctk.CTkEntry(self.frame_input, placeholder_text="Confirm new card number", font=("Comic Sans MS", 14), width=300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT)
        self.newcardnumber2.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        self.confirmnumberchange = ctk.CTkButton(self.frame_input, text="Confirm", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.checkcardnumbers)
        self.confirmnumberchange.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.backpayment).grid(row=4, column=0, padx=20, pady=10, sticky="w")
    
    def backpayment(self):
        self.update_payment_info()
        
    def checkcardnumbers(self):
        textboxcardno1 = self.newcardnumber1.get() #takes the input of the first card number box
        textboxcardno2 = self.newcardnumber2.get() #takes the input of the second card number box
        textboxcardno1 = textboxcardno1.replace(" ", "")
        textboxcardno2 = textboxcardno2.replace(" ", "")
        if len(textboxcardno1) == 16 and len(textboxcardno2) == 16 and textboxcardno1.isdigit() and textboxcardno2.isdigit() and textboxcardno1 == textboxcardno2:
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
            self.show_success_popup("Card number successfully changed!")    

        else:
            self.show_error_popup("Card number must be exactly 16 digits, and both entries must match.")

    def updatecardexpiry(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="transparent",
                                 hover_color=PRIMARY_DARK,
                                 text_color=TEXT,
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Enter your new card expiry date:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Confirm card expiry:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.newcardexpiry1 = ctk.CTkEntry(self.frame_input, placeholder_text="New card expiry", font=("Comic Sans MS", 14), width=300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT)
        self.newcardexpiry1.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.newcardexpiry2 = ctk.CTkEntry(self.frame_input, placeholder_text="Confirm new card expiry", font=("Comic Sans MS", 14), width=300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT)
        self.newcardexpiry2.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Note: Please enter your card expiry as a four digit number, without spaces or slashes. Enter in MM/YY format.", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.confirmexpirychange = ctk.CTkButton(self.frame_input, text="Confirm", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.checkcardexpiry)
        self.confirmexpirychange.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.backpayment).grid(row=5, column=0, padx=20, pady=10, sticky="w")

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
                self.show_error_popup("Month is invalid.")
            elif year < now.year or (year == now.year and month < now.month): #past date
                self.show_error_popup("Card is expired.")
            else:   
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
                self.show_success_popup("Card expiry successfully changed!") 
        else:
            self.show_error_popup("Card expiry must be exactly 4 digits (MMYY), and both entries must match.")
    
    def updatecardcvv(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="transparent",
                                 hover_color=PRIMARY_DARK,
                                 text_color=TEXT,
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Enter your new CVV", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.frame_input, text="Confirm CVV:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.newcvvnumber1 = ctk.CTkEntry(self.frame_input, placeholder_text="New CVV", font=("Comic Sans MS", 14), width=300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT)
        self.newcvvnumber1.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.newcvvnumber2 = ctk.CTkEntry(self.frame_input, placeholder_text="Confirm new CVV", font=("Comic Sans MS", 14), width=300, fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT)
        self.newcvvnumber2.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        self.confirmcvvchange = ctk.CTkButton(self.frame_input, text="Confirm", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.checkcardcvv)
        self.confirmcvvchange.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Back", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.backpayment).grid(row=4, column=0, padx=20, pady=10, sticky="w")

    def checkcardcvv(self):
        textboxcvvno1 = self.newcvvnumber1.get() #takes the input of the first card CVV box
        textboxcvvno2 = self.newcvvnumber2.get() #takes the input of the second card CVV box
        textboxcvvno1 = textboxcvvno1.replace(" ", "")
        textboxcvvno2 = textboxcvvno2.replace(" ", "")
        if len(textboxcvvno1) == 3 and len(textboxcvvno2) == 3 and textboxcvvno1.isdigit() and textboxcvvno2.isdigit() and textboxcvvno1 == textboxcvvno2:    
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
            self.show_success_popup("Card CVV successfully changed.")
        else:
            self.show_error_popup("CVV must be exactly 3 digits, and both entries must match.")
        
    def manage_profiles(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="transparent",
                                 hover_color=PRIMARY_DARK,
                                 text_color=TEXT,
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Select a profile:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkButton(self.frame_input, text="Edit Profiles", font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.editprofiles).grid(row=1, column=1, padx=20, pady=10, sticky="w")
        
        self.user_profile_lst = []
        with open('userprofiles.csv', 'r') as csv_file:
            profilereader = csv.DictReader(csv_file)
            for row in profilereader:
                if row ["username"] == self.user_logged_in:
                    self.user_profile_lst.append(row['profile_name'])
        for i, profile in enumerate (self.user_profile_lst):
            ctk.CTkButton(self.frame_input, text=profile, font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.profileclicked).grid(row=i+2, column=0, padx=10, pady=10)
         
        self.user_proftyp_lst = []
        with open('userprofiles.csv', 'r') as csv_file:
            proftypreader = csv.DictReader(csv_file)
            for row in proftypreader:
                if row ["username"] == self.user_logged_in:
                    self.user_proftyp_lst.append(row['profile_type'])
        for i, profile_typ in enumerate(self.user_proftyp_lst):
            ctk.CTkLabel(self.frame_input, text=profile_typ, text_color=TEXT,
                         font=("Comic Sans MS", 14)).grid(row=i+2, column=1, padx=10, pady=10)
        
        create_profile_btn = ctk.CTkButton(self.frame_input, text="Create New Profile", fg_color=PRIMARY,
                                        hover_color=PRIMARY_DARK, text_color=TEXT, command=self.create_profile)
        create_profile_btn.grid(row=99, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Back", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.backsettings).grid(row=100, column=0, padx=10, pady=10)
    
    def editprofiles(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, 
                                 text="SoggyStreams", 
                                 font = ("Comic Sans MS", 24, "bold"), 
                                 fg_color="transparent",
                                 hover_color=PRIMARY_DARK,
                                 text_color=TEXT,
                                 command=self.return_home)
        home_btn.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Choose profiles to edit or delete:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="w")
        
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
            ctk.CTkButton(self.frame_input, text=profile, font=("Comic Sans MS", 14), fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT).grid(row=i+2, column=1, padx=10, pady=10)
         
        self.user_proftyp_lst = []
        with open('userprofiles.csv', 'r') as csv_file:
            proftypreader = csv.DictReader(csv_file)
            for row in proftypreader:
                if row ["username"] == self.user_logged_in:
                    self.user_proftyp_lst.append(row['profile_type'])
        self.prof_typ_comboboxes = []
        for i, profile_typ in enumerate(self.user_proftyp_lst):
            combo = ctk.CTkComboBox(self.frame_input, values=["Adult", "Child"], font=("Comic Sans MS", 14), fg_color=FRAME, text_color=TEXT, border_color=BORDER,
                         command=lambda choice, name=self.user_profile_lst[i]: self.save_edited_prof_typ(name, choice))
            combo.set(profile_typ)
            combo.grid(row=i+2, column=2, padx=10, pady=10)
            self.prof_typ_comboboxes.append(combo)
            
                
        delete_prof_btn = ctk.CTkButton(self.frame_input, text="Delete", fg_color=PRIMARY,
                                        hover_color=PRIMARY_DARK, text_color=TEXT, command=self.checkbox_event)
        delete_prof_btn.grid(row=7, column=1, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Save", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.manage_profiles).grid(row=8, column=1, padx=10, pady=10) 
    
    def save_edited_prof_typ(self, profile_name, new_type):
        rows = []
        with open('userprofiles.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['username'] == self.user_logged_in and row['profile_name'] == profile_name:
                    row['profile_type'] = new_type
                rows.append(row)
        with open('userprofiles.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    
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
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, text="SoggyStreams", font = ("Comic Sans MS", 24, "bold"), fg_color="transparent",
                                        hover_color=PRIMARY_DARK, text_color=TEXT, command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Create a new profile:", text_color=TEXT, font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.prof_name = ctk.CTkEntry(self.frame_input, width=300, placeholder_text="Profile Name", fg_color=FRAME, text_color=TEXT, border_color=BORDER, placeholder_text_color=SUBTEXT)
        self.prof_name.grid(row=2, column=0, padx=20, pady=20)
        self.prof_type = ctk.CTkComboBox(self.frame_input, values=["Adult", "Child"], fg_color=FRAME, text_color=TEXT, border_color=BORDER)
        self.prof_type.grid(row=3, column=0, padx=20, pady=10)
        ctk.CTkButton(self.frame_input, text="Create Profile", command=self.save_new_profile, fg_color=PRIMARY,
                                        hover_color=PRIMARY_DARK, text_color=TEXT).grid(row=4, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Back", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.backprofile).grid(row=5, column=0, padx=10, pady=10)
    
    def backprofile(self):
        self.manage_profiles()
    
    def build_account(self):
        with open('userdata.csv', 'r') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                if row['username'] == self.user_logged_in or row['email'] == self.email_logged_in:
                    account = Account(
                        username=row['username'],
                        email=row['email'],
                        password=row['password'],
                        subscription_plan=row['subscription_plan'],
                        card_number=row['card_number'],
                        card_exp=row['card_exp'],
                        card_cvv=row['card_cvv']
                    )
                    break

        with open('userprofiles.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['username'] == self.user_logged_in:
                    account.add_profile(Profile(row['profile_name'], row['profile_type']))

        return account


    def find_content_by_title(self, title):
        for item in self.movies + self.tvshows:
            if item.title == title:
                return item
        return None
    
    def save_new_profile(self):
        newprofname = self.prof_name.get()
        newproftype = self.prof_type.get()
        if newprofname == "":
            self.show_error_popup("Profile name cannot be empty.")
            return
        with open('userprofiles.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([self.user_logged_in, newprofname, newproftype])
        
        self.save_viewinghistory_row(newprofname) 

        self.manage_profiles()
    
    def save_viewinghistory_row(self, profile_name):
        fieldnames = ['username', 'profile_name', 'viewed_movie', 'timestamp']#establish columns
        with open('viewinghistory.csv', 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames) #establish writer and columns to amend
            writer.writerow({
                'username': self.user_logged_in,
                'profile_name': profile_name,
                'viewed_movie': '', #amended with above movie_obj when a movie is viewed
                'timestamp': ''
            }) 
    
    def export_viewing_hist(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.frame_input = ctk.CTkFrame(self, fg_color=FRAME)
        self.frame_input.grid(row=0, column=0, sticky="nsew")
        home_btn = ctk.CTkButton(self.frame_input, text="SoggyStreams", font = ("Comic Sans MS", 24, "bold"), fg_color="transparent",
                                        hover_color=PRIMARY_DARK, text_color=TEXT, command=self.return_home)
        home_btn.grid(row=0, column=0, padx=20, pady=20, sticky = "nw")
        ctk.CTkLabel(self.frame_input, text="Export completed.", font = ("Comic Sans MS", 18)).grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_input, text="Back", fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color=TEXT, command=self.backsettings).grid(row=2, column=0, padx=10, pady=10)

        now = datetime.now()
        filename = f"viewing_history_{self.user_logged_in}_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        user_views = [] #empty lst
        with open('viewinghistory.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['username'] == self.user_logged_in and row['viewed_movie']: #read and extract viewed movies
                    user_views.append(row)
        with open(filename, 'w') as history:
            history.write("SoggyStreams Viewing History\n")
            history.write("-" * 40 + "\n")
            history.write(f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            history.write(f"Username: {self.user_logged_in}\n")
            history.write(f"Email: {self.email_logged_in}\n")
            history.write("-" * 40 + "\n")
            if not user_views:
                history.write("No viewing history yet.\n")
            else:
                for view in user_views:
                    history.write(f"Profile: {view['profile_name']}   Movie: {view['viewed_movie']}   Watched: {view['timestamp']}\n")
            history.write("-" * 40 + "\n")
            history.write("Thank you for using SoggyStreams!\n")
    
    def show_error_popup(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x200")
        error_window.configure(fg_color=BG)

        ctk.CTkLabel(error_window, text=message, text_color="#E73636",
                     font=("Comic Sans MS", 14), wraplength=350).pack(expand=True, padx=20, pady=20)

        ctk.CTkButton(error_window, text="OK", fg_color=PRIMARY, hover_color=PRIMARY_DARK,
                      text_color=TEXT, command=error_window.destroy).pack(pady=10)

    def show_success_popup(self, message):
        success_window = ctk.CTkToplevel(self)
        success_window.title("Success")
        success_window.geometry("400x200")
        success_window.configure(fg_color=BG)

        ctk.CTkLabel(success_window, text=message, text_color="#32CD6B",
                     font=("Comic Sans MS", 14), wraplength=350).pack(expand=True, padx=20, pady=20)

        ctk.CTkButton(success_window, text="OK", fg_color=PRIMARY, hover_color=PRIMARY_DARK,
                      text_color=TEXT, command=success_window.destroy).pack(pady=10)
    
    def logout(self):
        self.destroy()
        app = Login()
        app.mainloop()        

if __name__ == "__main__":
    app = Login()
    app.mainloop()