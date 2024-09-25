
from CTkMessagebox import CTkMessagebox
from tktooltip import ToolTip
import customtkinter
from psycopg2 import sql
from DataBase.conn_to_db import connect_to_db

from Windows.user_window1 import open_user_window1
from Windows.admin_window1 import open_admin_window1

# Secret passwords list
secret_passwords = ["secret1", "secret2", "secret3", "secret4", "secret5"]

def check_if_exists(column, value):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = f"SELECT COUNT(*) FROM public.accounts WHERE {column} = %s"
    cursor.execute(query, (value,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def check_payinfo(column, value):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = f"SELECT client_id FROM public.client WHERE client_payinfo = %s"
    cursor.execute(query, (value,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def check_login():
    choice = optionmenu.get()
    print(choice)
    if choice == "admin":
        login = admin_entry_login.get()
        if check_if_exists('login', login):
            error_login.configure(text="Login already exists")
            return False
        else:
            error_login.configure(text="")
            return True
    else:
        login = user_entry_login.get()
        if check_if_exists('login', login):
            error_login.configure(text="Login already exists")
            return False
        else:
            error_login.configure(text="")
            return True

def check_secret_password(secret):
    if secret in secret_passwords:
        secret_passwords.remove(secret)
        return True
    else:
        return False

def verify_credentials(login, password):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = sql.SQL("SELECT acc_type FROM public.accounts WHERE login = %s AND password = %s")
        cursor.execute(query, (login, password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    else:
        return None


def login_button_event_reg(app):
    login = admin_entry_login.get()
    password = admin_entry_password.get()
    user_data = verify_credentials(login, password)
    if user_data:
        acc_type = user_data[0]
        if acc_type == 'admin':
            open_admin_window1(login, app)
            register_window.destroy()
            register_window.update()
        elif acc_type == 'user':
            open_user_window1(login, app)

def login_button_event_reg_user(app):
    login = user_entry_login.get()
    password = user_entry_password.get()
    user_data = verify_credentials(login, password)
    if user_data:
        acc_type = user_data[0]
        if acc_type == 'admin':
            open_admin_window1(login, app)
        elif acc_type == 'user':
            open_user_window1(login, app)
            register_window.destroy()
            register_window.update()

def admin_confirm_register():

    if not check_login():
        CTkMessagebox(title="Error!", message="Login already exists.", icon="cancel")
        return

    login = admin_entry_login.get()
    password = admin_entry_password.get()
    secret = admin_entry_secret.get()

    if not login:
        admin_entry_login.focus()
        error_secret.configure(text="Fill login.")
        return

    if not password:
        admin_entry_password.focus()
        error_secret.configure(text="Fill password.")
        return
    if not secret:
        error_secret.configure(text="Fill secret password")
        return
    if not check_secret_password(secret):
        error_secret.configure(text="Invalid secret password")
        return

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
            "INSERT INTO public.accounts (login, password, acc_type) VALUES (%s, %s, %s)",
            (login, password, 'admin')
        )
    conn.commit()
    cursor.close()
    conn.close()

    success_label.configure(text="Admin registered successfully")
    confirmed_reg.configure(state="normal")

def is_whole_number(value):
    print(value)
    try:
        value = float(value)
    except ValueError:
        return False
    print(value)
    if value.is_integer():
        return True
    else:
        return False


def user_confirm_register():

    if not check_login():
        CTkMessagebox(title="Error!", message="Login already exists.", icon="cancel")
        return

    login = user_entry_login.get()
    password = user_entry_password.get()
    payinfo = user_entry_payinfo.get()
    name = user_entry_name.get()
    phone = user_entry_phone.get()

    if not login:
        user_entry_login.focus()
        error_payinfo.configure(text="Fill login.")
        return

    if not password:
        user_entry_password.focus()
        error_payinfo.configure(text="Fill password.")
        return
    if not payinfo:
        user_entry_payinfo.focus()
        error_payinfo.configure(text="Fill payinfo")
        return
    if not name:
        user_entry_name.focus()
        error_payinfo.configure(text="Fill name")
        return
    if not phone:
        user_entry_phone.focus()
        error_payinfo.configure(text="Fill phone")
        return
    if not is_whole_number(phone):
        user_entry_phone.focus()
        error_payinfo.configure(text="Incorrect phone format")
        return
    if not is_whole_number(payinfo):
        user_entry_payinfo.focus()
        error_payinfo.configure(text="Incorrect payinfo format")
        return

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT client_id FROM public.client WHERE client_payinfo = %s",
            (payinfo,))
    client_id = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    # Create a client if not existing
    if not client_id:

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO public.client (client_name, client_phone, client_payinfo) VALUES (%s, %s, %s)",
            (name, phone, payinfo)
        )
        cursor.execute(
            "SELECT client_id FROM public.client WHERE client_payinfo = %s",
            (payinfo,))
        client_id = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        print("inserted client with client_id:", client_id)

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO public.accounts (login, password, acc_type, req_id) VALUES (%s, %s, %s, %s)",
            (login, password, 'user', client_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        success_label.configure(text="User registered successfully")
        confirmed_reg1.configure(state="normal")

    # if the client exists, ask about going back to log in
    else:
        def sendUserToStartWindow():
            registerUserExists.destroy()
            registerUserExists.update()

        def from_reg_to_login():
            registerUserExists.destroy()
            registerUserExists.update()
            register_window.destroy()
            register_window.update()
            from Windows.main_app11 import app11
            app11.deiconify()

        registerUserExists = customtkinter.CTkToplevel()
        registerUserExists.title("Register")
        registerUserExists.geometry("400x150")
        user_register_exist_frame = customtkinter.CTkFrame(registerUserExists)
        user_register_exist_frame.grid(row=0, column=0, padx=10, pady=5)
        user_reg = customtkinter.CTkLabel(user_register_exist_frame, text="This user already exists, go back, or to login page")
        user_reg.grid(row=0, column=0, padx=10, pady=5,columnspan=2)
        to_login = customtkinter.CTkButton(user_register_exist_frame, text="Login page", command=from_reg_to_login)
        to_login.grid(row=1, column=0, padx=10, pady=5)
        to_back = customtkinter.CTkButton(user_register_exist_frame, text="Back", command=sendUserToStartWindow)
        to_back.grid(row=1, column=1, padx=10, pady=5)



def register_button_event1(app11):
    global admin_entry_login, admin_entry_password, admin_entry_secret, error_payinfo, user_entry_payinfo, confirmed_reg1, register_window
    global error_login, error_secret, success_label, confirmed_reg, optionmenu, user_entry_login, user_entry_password, user_entry_phone, user_entry_name
    register_window = customtkinter.CTkToplevel()
    register_window.title("Register")
    windowWidth = 800
    windowHeight = 600
    register_window.geometry(f"{windowWidth}x{windowHeight}")

    def optionmenu_callback(choice):
        print("optionmenu dropdown clicked:", choice)
        if choice == "admin":
            user_frame.grid_forget()
            admin_frame.grid(row=2, column=0, padx=20, pady=10)
        else:
            admin_frame.grid_forget()
            user_frame.grid(row=2, column=0, padx=20, pady=10)


    app11.withdraw()

    register_label = customtkinter.CTkLabel(register_window,text="Input information for account creation:",fg_color="transparent")
    register_label.grid(row=0, column=0, padx=20, pady=10)
    optionmenu = customtkinter.CTkOptionMenu(register_window, values=["admin", "user"],command=optionmenu_callback)
    optionmenu.set("admin")
    optionmenu.grid(row=1, column=0, padx=20, pady=5)
    ToolTip(optionmenu, msg="Choose the type of account you want to create")

    # Admin frame
    admin_frame = customtkinter.CTkFrame(register_window)
    admin_label = customtkinter.CTkLabel(admin_frame, text="Admin Specific Info")
    admin_label.grid(row=0, column=0, padx=10, pady=5)

    admin_entry_login = customtkinter.CTkEntry(admin_frame, placeholder_text="login")
    admin_entry_login.grid(row=1, column=0, padx=10, pady=5)
    error_login = customtkinter.CTkLabel(admin_frame, text=" ")
    error_login.grid(row=1, column=1, padx=5, pady=5)

    admin_entry_password = customtkinter.CTkEntry(admin_frame, placeholder_text="password", show="*")
    admin_entry_password.grid(row=2, column=0, padx=10, pady=5)

    admin_entry_secret = customtkinter.CTkEntry(admin_frame, placeholder_text="secret password")
    admin_entry_secret.grid(row=4, column=0, padx=10, pady=5)
    error_secret = customtkinter.CTkLabel(admin_frame, text=" ")
    error_secret.grid(row=4, column=1, padx=5, pady=5)

    admin_confirm = customtkinter.CTkButton(admin_frame,text="Confirm", command=admin_confirm_register)
    admin_confirm.grid(row=5, column=0, padx=10, pady=5)
    success_label = customtkinter.CTkLabel(admin_frame,text="")
    success_label.grid(row=6, column=0, padx=10, pady=5)
    confirmed_reg = customtkinter.CTkButton(admin_frame, text="Log in created account", command=lambda: login_button_event_reg(app11), state="disabled")
    confirmed_reg.grid(row=7, column=0, padx=10, pady=5)

    # User frame
    user_frame = customtkinter.CTkFrame(register_window)
    user_label = customtkinter.CTkLabel(user_frame, text="User Specific Info")
    user_label.grid(row=0, column=0, padx=10, pady=10)
    user_entry = customtkinter.CTkEntry(user_frame, placeholder_text="User Field")
    user_entry.grid(row=1, column=0, padx=10, pady=10)

    user_entry_login = customtkinter.CTkEntry(user_frame, placeholder_text="login")
    user_entry_login.grid(row=1, column=0, padx=10, pady=5)
    error_login = customtkinter.CTkLabel(admin_frame, text=" ")
    error_login.grid(row=1, column=1, padx=5, pady=5)

    user_entry_password = customtkinter.CTkEntry(user_frame, placeholder_text="password", show="*")
    user_entry_password.grid(row=2, column=0, padx=10, pady=5)

    user_entry_payinfo = customtkinter.CTkEntry(user_frame, placeholder_text="payinfo")
    user_entry_payinfo.grid(row=4, column=0, padx=10, pady=5)
    error_payinfo = customtkinter.CTkLabel(user_frame, text=" ")
    error_payinfo.grid(row=4, column=1, padx=5, pady=5)
    user_entry_name = customtkinter.CTkEntry(user_frame, placeholder_text="name")
    user_entry_name.grid(row=5, column=0, padx=10, pady=5)
    user_entry_phone = customtkinter.CTkEntry(user_frame, placeholder_text="phone")
    user_entry_phone.grid(row=6, column=0, padx=10, pady=5)

    user_error_secret = customtkinter.CTkLabel(user_frame, text=" ")
    user_error_secret.grid(row=4, column=1, padx=5, pady=5)

    user_confirm = customtkinter.CTkButton(user_frame, text="Confirm", command=user_confirm_register)
    user_confirm.grid(row=7, column=0, padx=10, pady=5)
    success_label_u = customtkinter.CTkLabel(user_frame, text="START")
    success_label_u.grid(row=8, column=0, padx=10, pady=5)
    confirmed_reg1 = customtkinter.CTkButton(user_frame, text="Log in created account", command=lambda: login_button_event_reg_user(app11),
                                            state="disabled")
    confirmed_reg1.grid(row=9, column=0, padx=10, pady=5)

    # Initialize the admin frame at the start of the app
    optionmenu_callback(optionmenu.get())

