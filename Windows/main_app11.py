
from CTkMessagebox import CTkMessagebox
import customtkinter
from Windows.user_window1 import open_user_window1
from Windows.admin_window1 import open_admin_window1
from Verification.account_ver11 import register_button_event1, verify_credentials


# Event for login button
def login_button_event(entry_login, entry_pass, app11, login_error_label):

    login = entry_login.get()
    password = entry_pass.get()
    if not login:
        entry_login.focus()
        login_error_label.configure(text="Fill login.")
        return

    if not password:
        entry_pass.focus()
        login_error_label.configure(text="Fill password.")
        return
    user_data = verify_credentials(login, password)
    if user_data:
        acc_type = user_data[0]
        if acc_type == 'admin':
            open_admin_window1(login, app11)
        elif acc_type == 'user':
            open_user_window1(login, app11)
        else:
            CTkMessagebox(title="Error!", message="Invalid account type.", icon="cancel")
    else:
        CTkMessagebox(title="Error!", message="Invalid login or password.\n Maybe Try creating a new account!", icon="cancel")


# Function to open new window
def create_main_window1():

    # Main app window
    app11 = customtkinter.CTk()
    app11.title("Building Company Register")
    app11.geometry("800x600")


    entry_frame = customtkinter.CTkFrame(app11)
    entry_frame.grid(row=0, column=0, padx=20, pady=20)
    entry_login = customtkinter.CTkEntry(entry_frame, placeholder_text="login...")
    entry_login.grid(row=0, column=0, padx=20, pady=20)
    entry_pass = customtkinter.CTkEntry(entry_frame, placeholder_text="password...", show="*")
    entry_pass.grid(row=1, column=0, padx=20, pady=10)

    button_login = customtkinter.CTkButton(entry_frame, text="Log in", command=lambda: login_button_event(entry_login, entry_pass, app11, login_error_label))
    button_login.grid(row=2, column=0, padx=20, pady=10)
    button_register = customtkinter.CTkButton(entry_frame, text="Register", command=lambda : register_button_event1(app11))
    button_register.grid(row=3, column=0, padx=20, pady=10)
    login_error_label = customtkinter.CTkLabel(entry_frame, text="", fg_color="transparent")
    login_error_label.grid(row=4, column=0, padx=20, pady=5)

    app11.mainloop()

# Only open the window when this script is executed directly
if __name__ == '__main__':
    create_main_window1()


