from tkinter import *
from tkinter import messagebox
import time
from tkinter import ttk
from datetime import datetime, timedelta
import mysql.connector
import os
from tkinter.simpledialog import askstring
import re
from tkinter import font
import pyautogui
from PIL import Image
import socket


# ustawienia połączenia
host = "sql7.freesqldatabase.com"
user = "sql7609320"
password = 'ICRy5uVZ6K'
database = "sql7609320"

# nawiązanie połączenia
conn = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database
)


cursor = conn.cursor()


def create_file():
    try:
        source = 'C:/xampp/htdocs/webcfg/'
        user_folder = os.path.join(source, username)
        os.mkdir(user_folder)
    except:
        pass


def delete_user(root):
    global username

    
    # sprawdzenie, czy użytkownik o podanej nazwie istnieje w bazie danych
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result is None:
        error_label.config(text="Użytkownik o takiej nazwie nie istnieje!")
        error_label.after(5000, lambda: error_label.config(text=""))
        return

   
    ask = messagebox.askquestion(title="Potwierdzenie", message=f"Czy na pewno chcesz usunąć konto {username}")

    if ask == 'yes':

        chceck_password = askstring("Potwierdzenie", "Jeżeli chcesz usunąć konto, musisz wpisać hasło:")

        if chceck_password != result[2]:
            messagebox.showerror(title=None, message="Podano złe hasło")
            return
        else:
            # usunięcie użytkownika z bazy danych
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
            conn.commit()

            # usunięcie folderu użytkownika
            source = 'C:/xampp/htdocs/webcfg/'
            user_folder = os.path.join(source, username)
            try:
                os.rmdir(user_folder)
            except OSError:
                pass
            else:
                messagebox.showinfo("Sukces", "Użytkownik został usunięty!")
            
                  
            root.destroy()


def login_successful():
    root.destroy()
    main_content()

def login_failed(error_label):
    error_label.config(text="Błędna nazwa użytkownika lub hasło!")
    error_label.after(5000, lambda: error_label.config(text=""))

def register_successful():
    messagebox.showinfo("Sukces", "Rejestracja udana!")
    code_label.destroy()
    code_entry.destroy()
    register_done_button.destroy()
    error_code.destroy()
    back_button.destroy()
    again_code_button.destroy()

    login_window()

def register_failed():
    error_register_label.config(text="Użytkownik o takiej nazwie już istnieje!")
    error_register_label.after(5000, lambda: error_register_label.config(text=""))

def send_code_bnt_again():
    send_code_bnt()
    error_code.config(text="Wyslalismy kod jeszcze raz!")
    error_code.after(5000, lambda: error_label.config(text=""))

def send_code_bnt():
    from email.message import EmailMessage
    import ssl
    import smtplib
    import random
    global code
    

    email_sender = ' konradskora37@gmail.com'
    email_password = 'jkxeelngqignkomr'
    email_receiver = email
    code = random.randint(10000, 99999)

    subject = f"Kod weryfikacjyjny"
    body = f"""
    To jest twój kod weryfikacyjny: {code}
    """

    
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)


    context = ssl.create_default_context()

    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
    except:
        pass
    
    print(code)

def check(s):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(pat, s):
        return "poprawne"
    else:
        return "Niepoprawny Email"
    
def register_user():
    send_code = code_entry.get()
    ip = socket.gethostbyname(socket.gethostname())
    if send_code.isdigit():
        send_code = int(send_code)
        if code == send_code:
            cursor.execute("INSERT INTO users (username, password, email, account_date, IP) VALUES (%s, %s, %s, %s, %s)", (username, password, email, account_date, ip))
            conn.commit()

            create_file()
            register_successful()
        else:
            error_code.config(text="Nieprawidlowy kod")
            error_code.after(5000, lambda: error_code.config(text=""))

    else:
        error_code.config(text="Nieprawidłowy kod")
        error_code.after(5000, lambda: error_code.config(text=""))

def back_to_login():
    label_username_register.destroy()
    entry_username_register.destroy()
    label_email_register.destroy()
    entry_email_register.destroy()
    label_password_register.destroy()
    entry_password_register.destroy()
    next_register_register.destroy()
    error_register_label.destroy()

    login_window()
          


def back_to_register():
    code_label.destroy()
    code_entry.destroy()
    register_done_button.destroy()
    error_code.destroy()
    back_button.destroy()
    again_code_button.destroy()

    register()
    

def verify_code():
    global account_date, username, email, code_entry, error_code, password, code_label , register_done_button, again_code_button, back_button
    account_date = datetime.now().strftime("%d-%m-%Y")
    username = entry_username_register.get()
    email = entry_email_register.get()
    password = entry_password_register.get()
    

    if len(username) < 4:
        error_register_label.config(text="Login musi mieć minimum niż 4 litery!")
        error_register_label.after(5000, lambda: error_register_label.config(text=""))
    elif len(username) > 15:
        error_register_label.config(text="Login musi mieć mniej niż 16 liter!")
        error_register_label.after(5000, lambda: error_register_label.config(text=""))
    elif len(email) == 0:
        error_register_label.config(text="Niepoprawny adres e-mail!")
        error_register_label.after(5000, lambda: error_register_label.config(text=""))
    elif check(email.strip()) != "poprawne":
        error_register_label.config(text="Niepoprawny adres e-mail!")
        error_register_label.after(5000, lambda: error_register_label.config(text=""))
    elif len(password) < 5:
        error_register_label.config(text="Hasło musi mieć minimum 5 liter!")
        error_register_label.after(5000, lambda: error_register_label.config(text=""))
    elif len(password) > 20:
        error_register_label.config(text="Hasło musi mieć mniej niż 25 liter!")
        error_register_label.after(5000, lambda: error_register_label.config(text=""))
    elif " " in username:
        error_register_label.config(text="Nazwa użytkownika nie może zawierać spacji!")
        error_register_label.after(5000, lambda: error_register_label.config(text=""))
    elif " " in password:
        error_register_label.config(text="Hasło nie może zawierać spacji!")
        error_register_label.after(5000, lambda: error_register_label.config(text=""))
    
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result is not None:
            register_failed()
            return
        
        label_username_register.destroy()
        entry_username_register.destroy()
        label_email_register.destroy()
        entry_email_register.destroy()
        label_password_register.destroy()
        entry_password_register.destroy()
        next_register_register.destroy()
        error_register_label.destroy()

        send_code_bnt()
        
        
        code_label = Label(root, text="Wpisz kod ktory wyslalismy ci na twoja poczte")
        code_label.pack(pady=(35,4))

        code_entry = Entry(root)
        code_entry.pack()

        register_done_button = Button(root, text="Potwierdz kod",command=register_user)
        register_done_button.pack(pady=5)

        error_code = Label(root)
        error_code.pack(pady=5)

        back_button = Button(root, text="Powrot", command=back_to_register)
        back_button.place(x=2, y=2)
        
        again_code_button = Button(root, text="Wyslij kod jeszcze raz", command=send_code_bnt_again)
        again_code_button.pack(pady=(35,0))


def login():
    global username
    global password
    global account_date
    global email
    
    
    username = entry_username.get().lower()
    password = entry_password.get()
    
    
    

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE LOWER(username) = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    if result is not None:
        account_date = result[4]
        email = result[3]
        login_successful()
        return
    
    login_failed(error_label)


def register():
    label_username.destroy()
    entry_username.destroy()
    label_password.destroy()
    entry_password.destroy()
    button_login.destroy()
    button_register.destroy()
    error_label.destroy()
    
    global label_username_register, entry_username_register, label_email_register, entry_email_register, label_password_register, entry_password_register, next_register_register, error_register_label
    
    root.title("Rejestracja")
    root.geometry("350x250")
    
    
    


    label_username_register = Label(root, text="Nazwa użytkownika:")
    label_username_register.pack(pady=(16, 2))

    entry_username_register = Entry(root, width=30)
    entry_username_register.pack()
    
    label_email_register = Label(root, text="Adres e-mail:")
    label_email_register.pack(pady=2)

    entry_email_register = Entry(root, width=30)
    entry_email_register.pack()

    label_password_register = Label(root, text="Hasło:")
    label_password_register.pack(pady=2)

    entry_password_register = Entry(root, show="•", width=30)
    entry_password_register.pack()

    next_register_register = Button(root, text="Przejdz dalej", command=verify_code)
    next_register_register.pack(pady=10)

    error_register_label = Label(root)
    error_register_label.pack()

    back_login = Button(root, text="Powrot", command=back_to_login)
    back_login.place(x=2, y=2)
    

    

def login_window():
    global label_username, entry_username, label_password, entry_password, button_login, error_label, button_register
    root.geometry("350x210")
    root.title("Logowanie")

    label_username = Label(root, text="Nazwa użytkownika:")
    label_username.pack(pady=(10, 2))

    entry_username = Entry(root, width=30)
    entry_username.pack()


    label_password = Label(root, text="Hasło:")
    label_password.pack(pady=2)

    entry_password = Entry(root, show="•", width=30)
    entry_password.pack()

    button_login = Button(root, text="Zaloguj się", command=login)
    button_login.pack(pady=10)

    error_label = Label(root)
    error_label.pack()

    button_register = Button(root, text="Zarejestruj się", command=register)
    button_register.pack(padx= (250, 0), pady=(17, 0))





#       !!!!!!!!!!!!!!!!!!!!!!        Główna zawartość        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def main_content(): 
    root = Tk()
    root.geometry("800x500")
    root.title("Aplikacja")
    root.resizable(0, 0)
    
    
    global main_frame

    
    def check_license():    
        import datetime
        
        cnx = mysql.connector.connect(host = "sql7.freesqldatabase.com", 
                                    user = "sql7609320",
                                    password = 'ICRy5uVZ6K',
                                    database = "sql7609320")
        cursor = cnx.cursor()

        # Pobranie klucza licencyjnego od użytkownika
        license_key = license_key_entry.get()

        # Sprawdzenie, czy klucz licencyjny jest aktywny i ważny
        query = ("SELECT id, max_uses, uses, expiration_date, active FROM licenses "
                "WHERE license_key = %s")
        cursor.execute(query, (license_key,))
        result = cursor.fetchone()
        

        if result is None:
            license_status_label.config(text="Niepoprawny klucz licencyjny")
        else:
            license_id, max_uses, uses, expiration_date, active = result

            if not active:
                license_status_label.config(text="Ten klucz nie jest już aktywny")
                
            elif expiration_date < datetime.date.today():
                license_status_label.config(text="Ten klucz jest już przedawnony")
                
            elif uses >= max_uses:
                license_status_label.config(text="Ten klucz został użyty już maksymalną ilość razy")
                
            else:
                license_status_label.config(text="Poprawny klucz licencyjny")
                # Zwiększenie licznika użyć klucza licencyjnego w bazie danych
                update_query = ("UPDATE licenses SET uses = uses + 1 WHERE id = %s")
                cursor.execute(update_query, (license_id,))
                cnx.commit()
                
                
                cursor.execute("SELECT date FROM licenses WHERE license_key = %s", (license_key,))
                date = cursor.fetchone()[0]
                date_now = datetime.datetime.now() + datetime.timedelta(days=date)
                license_date = date_now.strftime('%d-%m-%Y')

                # Zapisanie licencji użytkownika w bazie danych
                
                cursor.execute("UPDATE users SET license_date = %s WHERE username = %s", (license_date, username))
                cnx.commit()
                
                user_query = ("UPDATE users SET license = 1 WHERE username = %s")
                cursor.execute(user_query, (username,))
                cnx.commit()
                
                check_button.config(state=DISABLED)
                messagebox.showinfo("", "Uruchom ponownie program")
                root.destroy()
                login_window()
                    
                        
        
            cursor.close()
            cnx.close()
            
        
        

    def send_message():
        from email.message import EmailMessage
        import ssl
        import smtplib
        mail = mail_entry.get()
        send_text = text_box.get("1.0", "end")


        email_sender = ' konradskora37@gmail.com'
        email_password = 'jkxeelngqignkomr'
        email_receiver = mail


        subject = f"Wiadomość"
        body = f"{send_text}"
        
        
        
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        em.set_content(body)


        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL( 'smtp.gmail.com' , 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
        except:
            pass


    def collect_chest_twitch():
        kolka = ['img\kolko1.png', 'img/kolko2.png']
        obrazy_kolek = []
        for kolo in kolka:
            obraz_kola = Image.open(kolo)
            obrazy_kolek.append(obraz_kola)

        while True:
            for obraz_kola in obrazy_kolek:
                pozycja_kolka = pyautogui.locateOnScreen(obraz_kola)
                if pozycja_kolka:
                    x, y = pyautogui.center(pozycja_kolka)
                    pyautogui.moveTo(x, y)
                    time.sleep(0.5)
                    pyautogui.click()
                time.sleep(1)

    frame = ttk.Notebook(root, width=800, height=500)
    frame.pack_propagate(0)
    frame.pack(expand=True)

    # create frames
    main_frame = Frame(frame)
    main_frame.pack()
    profile = Frame(frame)
    profile.pack()
    save_file = Frame(frame)
    save_file.pack()
    bind_settings = Frame(frame, width=300)
    bind_settings.pack()
    settings = Frame(frame)
    settings.pack()
    


    # add frames to frame
    frame.add(main_frame, text='General Information')
    frame.add(profile, text='Profil')
    frame.add(save_file, text="Zapisz ustawienia")
    frame.add(bind_settings, text="Bindy")
    frame.add(settings, text="Ustawienia")
    



    #side frame
    side_frame = LabelFrame(main_frame, relief="groove", borderwidth=3)
    side_frame.grid(row=0, column=0, rowspan=1, sticky="nsew")
    side_frame.config(highlightcolor="red")
    side_frame.columnconfigure(0, minsize=170)
    side_frame.rowconfigure(0, minsize=300, weight=1)

    
    
    # Button
    logout_button = Button(main_frame, text="Wyloguj", command=root.destroy)
    logout_button.place(x=735, y=445)

    

    user_frame = LabelFrame(side_frame, padx=5, pady=5)
    user_frame.grid(row=0, column=0, padx=5, pady=5)

    loginuser = Label(user_frame, text=f"Zalogowano jako {username}")
    loginuser.grid(row=0, column=0)

    
    # send email

    email_frame = LabelFrame(main_frame, text="Wyslij e-mail")
    email_frame.grid(row=0, column=2)

    mail_label = Label(email_frame, text="Podaj e-mail'a")
    mail_label.grid(row=1, padx=5, pady=5, column=0)
                    
    mail_entry = Entry(email_frame)
    mail_entry.grid(row=1, padx=5, pady=5, column=1)
    

    mail_button = Button(email_frame, text="Wyślij wiadomość", command=send_message)
    mail_button.grid(row=2, padx=5, pady=5, columnspan=2)


    # text box

    text_frame = Frame(email_frame, padx=5, pady=5)
    text_frame.grid(row=3, columnspan=2)
    
    
    text_box = Text(text_frame, width=25, height=10)
    text_box.pack(side=LEFT, fill=Y)
    
    scrollbar = Scrollbar(text_frame, command=text_box.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_box.config(yscrollcommand=scrollbar.set)
    

    

    
    # Profile
    
    profile_font = ("Lucida", 10)
    license_font = ("Robot", 12)

    profile_frame = LabelFrame(profile, padx=5, pady=5)
    profile_frame.grid(row=1, column=0, pady=5, padx=5)
    
    

    

    date_create_accounts = Label(profile_frame, text=f"Data utworzenia konta: {account_date}", font=profile_font)
    date_create_accounts.grid(row=0, column=0, pady=2, sticky=W)
    
    show_username = Label(profile_frame, text=f"Username: {username}", font=profile_font)
    show_username.grid(row=1, column=0, sticky=W, pady=3)

    show_email = Label(profile_frame, text=f"e-mail: {email}", font=profile_font)
    show_email.grid(row=2, column=0, sticky=W, pady=3)

    show_password = Label(profile_frame, text=f"Hasło: {'•' * len(password)}", font=profile_font)
    show_password.grid(row=3, column=0, sticky=W, pady=3)

    show_licenses = Label(profile_frame, text="", font=profile_font)
    show_licenses.grid(row=4, column=0, sticky=W, pady=5)

    show_licenses_time = Label(profile_frame, text="Data wygasniecia konta: 0000-00-00", font=profile_font)
    show_licenses_time.grid(row=5, column=0, sticky=W, pady=5)
    

    var = IntVar()

    chceckbutton_password = Checkbutton(profile_frame, text="Pokaż hasło", variable=var)

    def on_check():
        if var.get() == 1:
            show_password.config(text=f"Hasło: {password}")
        else:
            show_password.config(text=f"Hasło: {'•' * len(password)}")

    chceckbutton_password.config(command=on_check)
    chceckbutton_password.grid(row=3, column=1)
    
    delate_user = Button(profile_frame, text="Usuń konto", command=lambda:delete_user(root))
    delate_user.grid(row=4, column=1, pady=3, padx=10)

    

    # License frame

    license_frame = LabelFrame(profile, padx=10, pady=12)
    license_frame.grid(row=1, column=1, padx=(50,10), pady=5)
    

    license_key_label = Label(license_frame, text="Kod licencji:", font=license_font)
    license_key_label.pack(pady=5)
    license_key_entry = Entry(license_frame, width=45)
    license_key_entry.pack(pady=5)
    check_button = Button(license_frame, text="Sprawdz licencje", command=check_license)
    check_button.pack(pady=5)
    license_status_label = Label(license_frame, text="")
    license_status_label.pack(pady=5) 

    license_query = "SELECT license FROM users WHERE username = %s"
    cursor.execute(license_query, (username,))
    result = cursor.fetchall()
    
    check_license_date = "SELECT license_date FROM users WHERE username = %s"
    cursor.execute(check_license_date, (username,))
    license_date_check = cursor.fetchall()
    
    
    if result and result[0][0] == 1 and license_date_check and datetime.strptime(license_date_check[0][0], '%d-%m-%Y').date() >= datetime.today().date():
        show_licenses.config(text="Licencja: Premium")
        check_button.config(state=DISABLED)
        show_licenses_time.config(text=f"Data wygasniecia konta: {license_date_check[0][0]}")

    else:
        show_licenses.config(text="Licencja: Brak")
        frame.tab(2, state='disabled')
        frame.tab(3, state='disabled')
        
        
        

    


root = Tk()
root.resizable(0, 0)

login_window()



root.mainloop()

