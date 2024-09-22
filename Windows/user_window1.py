from tkinter import ttk
import tkinter as tk
from datetime import datetime
import customtkinter
from DataBase.conn_to_db import connect_to_db



def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def update_time(cur_date_time, cur_date):
    cur_time = get_current_time()
    cur_date_time.configure(text=f"{cur_date} {cur_time}")
    cur_date_time.after(1000, lambda: update_time(cur_date_time, cur_date))

def find_client_id_by_login(login):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT client_id 
        FROM client 
        WHERE client_id = (SELECT req_id FROM public.accounts WHERE login = %s )""",
        (login,)
    )
    conn.commit()
    cur_client_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return cur_client_id

def fetch_header(table_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(f"""
           SELECT column_name 
           FROM information_schema.columns 
           WHERE table_name = %s;
       """, (table_name,))
    columns_info = cursor.fetchall()
    column = [column[0] for column in columns_info]
    cursor.close()
    conn.close()
    return column

def fetch_table_name():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """)
    tables_info = cursor.fetchall()
    table_names = [table[0] for table in tables_info]
    cursor.close()
    conn.close()
    return table_names


def search_building_id(contract_ids):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT contract_id FROM building WHERE contract_id=%s",
        (contract_ids,)
    )

    building_id = cursor.fetchall()
    cursor.close()
    conn.close()
    return building_id

def user_fetch_table_contract(client_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    SELECT b.building_name, c.date_signed, c.date_closed, c.contract_sum, c.status
    FROM public.contract c
    JOIN public.building b ON c.building_id = b.building_id
    JOIN public.client cl ON c.client_id = cl.client_id
    WHERE cl.client_id = %s
    """
    cursor.execute(query, (client_id,))
    table_list = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return table_list, headers

def user_fetch_table_labor(client_id, building_name=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    if building_name and building_name!="NULL":
        query = """
        SELECT b.building_name, l.labor_name, l.date_start, l.date_end
        FROM public.labor l
        JOIN public.building b ON l.building_id = b.building_id
        JOIN public.client c ON b.client_id = c.client_id
        WHERE c.client_id = %s AND b.building_name = %s;
        """
        cursor.execute(query, (client_id, building_name))
    else:
        query = """
        SELECT b.building_name, l.labor_name, l.date_start, l.date_end
        FROM public.labor l
        JOIN public.building b ON l.building_id = b.building_id
        JOIN public.client c ON b.client_id = c.client_id
        WHERE c.client_id = %s;
        """
        cursor.execute(query, (client_id,))
    table = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return table, headers

def user_fetch_table_worker(client_id, building_name=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    if building_name and building_name != "NULL":
        cursor.execute(
            "SELECT building_id FROM building WHERE building_name = %s",
            (building_name,)
        )
        building_id = cursor.fetchone()
        query = """
        SELECT b.building_name, w.fullname, j.job_name, w.employment_date, w.worker_payinfo, j.job_pay
        FROM public.worker w
        JOIN public.building b ON w.building_id = b.building_id
        JOIN public.client c ON b.client_id = c.client_id
        JOIN public.job j ON w.job_id = j.job_id
        WHERE c.client_id = %s AND b.building_id = %s;
        """
        cursor.execute(query, (client_id, building_id))
    else:
        query = """
        SELECT b.building_name, w.fullname, j.job_name, w.employment_date, w.worker_payinfo, j.job_pay
        FROM public.worker w
        JOIN public.building b ON w.building_id = b.building_id
        JOIN public.client c ON b.client_id = c.client_id
        JOIN public.job j ON w.job_id = j.job_id
        WHERE c.client_id = %s;
        """
        cursor.execute(query, (client_id,))
    table = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return table, headers


def user_fetch_table_payment(client_id, contract_id=None, payment_type=None):
    conn = connect_to_db()
    cursor = conn.cursor()


    if payment_type == 'salary':  # Payment for worker's salary
        query = """
        SELECT p.pay_id,p.contract_id, p.pay_type, w.fullname, p.pay_sum, p.pay_date
        FROM public.pay p
        JOIN public.worker w ON p.required_id = w.worker_id
        JOIN public.contract c ON p.contract_id = c.contract_id
        WHERE c.client_id = %s AND p.pay_type = 'salary'
        """
        params = [client_id]

        if contract_id !="NULL":
            query += " AND p.contract_id = %s"
            params.append(contract_id)

    elif payment_type == 'material':  # Payment for materials
        query = """
        SELECT p.pay_id, p.contract_id, p.pay_type, m.material_name, p.pay_sum, p.pay_date
        FROM public.pay p
        JOIN public.material m ON p.required_id = m.material_id
        JOIN public.contract c ON p.contract_id = c.contract_id
        WHERE c.client_id = %s AND p.pay_type = 'material'
        """
        params = [client_id]

        if contract_id !="NULL":
            query += " AND p.contract_id = %s"
            params.append(contract_id)

    elif payment_type == 'phase':  # Payment for completed phase
        query = """
        SELECT p.pay_id, p.contract_id, p.pay_type, ph.phase_name, p.pay_sum, p.pay_date
        FROM public.pay p
        JOIN public.phase ph ON p.required_id = ph.phase_id
        JOIN public.contract c ON p.contract_id = c.contract_id
        WHERE c.client_id = %s AND p.pay_type = 'phase'
        """
        params = [client_id]

        if contract_id !="NULL":
            query += " AND p.contract_id = %s"
            params.append(contract_id)

    elif contract_id != "NULL" and payment_type == "NULL":
        query = """
                   SELECT p.pay_id, p.contract_id, p.pay_type, p.required_id, p.pay_sum, p.pay_date
                   FROM public.pay p
                   JOIN public.contract c ON p.contract_id = c.contract_id
                   WHERE c.client_id = %s AND p.contract_id = %s
                   """
        params = [client_id, contract_id]
    else:  # Default case: no specific pay_type or contract_id specified
        query = """
        SELECT p.pay_id, p.contract_id, p.pay_type, p.required_id, p.pay_sum, p.pay_date
        FROM public.pay p
        JOIN public.contract c ON p.contract_id = c.contract_id
        WHERE c.client_id = %s
        """
        params = [client_id]


    cursor.execute(query, tuple(params))
    table = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return table, headers


def user_fetch_table_material(client_id, building_name=None, checkbox_value=0):
    conn = connect_to_db()
    cursor = conn.cursor()

    if building_name and building_name != "None":
        cursor.execute("SELECT building_id FROM building WHERE building_name = %s", (building_name,))
        building_id = cursor.fetchone()
        building_id = building_id[0] if building_id else None

        if checkbox_value == "1":
            query = """
            SELECT l.labor_name, b.building_name, m.material_name, um.amount, m.material_cost, (um.amount * m.material_cost) AS total_material_cost
            FROM public.used_materials um
            JOIN public.material m ON um.material_id = m.material_id
            JOIN public.labor l ON um.labor_id = l.labor_id
            JOIN public.building b ON l.building_id = b.building_id
            JOIN public.client c ON b.client_id = c.client_id
            WHERE c.client_id = %s AND b.building_id = %s;
            """
            cursor.execute(query, (client_id, building_id))
        else:
            query = """
            SELECT s.supplier_name, b.building_name, m.material_name, m.material_dategot AS material_date, m.material_amount, m.material_cost, (m.material_amount * m.material_cost) AS total_material_cost
            FROM public.material m
            JOIN public.supplier s ON m.supplier_id = s.supplier_id
            JOIN public.building b ON m.building_id = b.building_id
            JOIN public.client c ON b.client_id = c.client_id
            WHERE c.client_id = %s AND b.building_id = %s;
            """
            cursor.execute(query, (client_id, building_id))
    else:
        if checkbox_value == "1":
            query = """
            SELECT l.labor_name, b.building_name, m.material_name, um.amount, m.material_cost, (um.amount * m.material_cost) AS total_material_cost
            FROM public.used_materials um
            JOIN public.material m ON um.material_id = m.material_id
            JOIN public.labor l ON um.labor_id = l.labor_id
            JOIN public.building b ON l.building_id = b.building_id
            JOIN public.client c ON b.client_id = c.client_id
            WHERE c.client_id = %s;
            """
            cursor.execute(query, (client_id,))
        else:
            query = """
            SELECT s.supplier_name, b.building_name, m.material_name, m.material_dategot AS material_date, m.material_amount, m.material_cost, (m.material_amount * m.material_cost) AS total_material_cost
            FROM public.material m
            JOIN public.supplier s ON m.supplier_id = s.supplier_id
            JOIN public.building b ON m.building_id = b.building_id
            JOIN public.client c ON b.client_id = c.client_id
            WHERE c.client_id = %s;
            """
            cursor.execute(query, (client_id,))

    table = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    return table, headers


def create_table_frame(new_window):
    table_frame = customtkinter.CTkFrame(new_window, width=1200, height=400)
    table_frame.grid(row=0, column=0, padx=10, pady=5)
    return table_frame

def apply_style():
    # apply style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#2e2e2e",
                    foreground="white",
                    rowheight=20,
                    fieldbackground="#2e2e2e")
    style.configure("Treeview.Heading",
                    background="#1f1f1f",
                    foreground="white",
                    relief="flat")
    style.map("Treeview.Heading",
              background=[('active', '#3d3d3d')])

    style.configure("Vertical.TScrollbar",
                    background="#3d3d3d",
                    troughcolor="#2e2e2e",
                    arrowcolor="white")

def insert_table_in_frame(headers, table_list, table_frame):
    apply_style()

    tree = ttk.Treeview(table_frame, columns=headers, show='headings', style="Treeview")

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")
    tree.configure(yscrollcommand=scrollbar.set)
    tree.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")

    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=150, stretch=tk.YES)

    for row in table_list:
        tree.insert("", "end", values=row)

    return tree


def update_tables_in_frame(table_list, headers, tree):
    apply_style()

    # Clear all existing items in the tree
    for item in tree.get_children():
        tree.delete(item)

    tree["columns"] = headers
    tree["show"] = "headings"

    # Update headers
    for header in headers:
        tree.heading(header, text=header)
        if header:
            tree.column(header, width=150, stretch=tk.YES)

    # Insert new rows
    for row in table_list:
        tree.insert("", "end", values=row)

class DatabaseManager:


    def user_fetch_table_building(self, client_id):
        conn = connect_to_db()
        cursor = conn.cursor()
        query = f"""SELECT b.building_name, b.building_area, b.building_date_start, b.building_date_end, b.city, b.address 
                    FROM building b 
                    WHERE client_id = %s"""
        cursor.execute(query, (client_id,))
        table_list = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return table_list, headers



class WindowUser:
    def __init__(self, db_manager):
        self.windows = {}
        self.cur_client_id = None
        self.db_manager = db_manager

    def create_new_window(self, table_name, client_id):
        new_window = customtkinter.CTkToplevel()
        new_window.title(f"{table_name} - Client {client_id}")
        return new_window

    def createNewWindow(self, client_id, table_name):
        window_key = f"{client_id}_{table_name}"
        new_window = customtkinter.CTkToplevel()
        new_window.title(f"{table_name} - Client {client_id}")
        self.windows[window_key] = new_window
        return new_window

    def checkWindowExists(self, client_id, table_name):
        window_key = f"{client_id}_{table_name}"
        if window_key in self.windows and self.windows[window_key].winfo_exists():
            return True
        else:
            return False

    def getWindow(self,client_id, table_name):
        window_key = f"{client_id}_{table_name}"
        if window_key in self.windows and self.windows[window_key].winfo_exists():
            return self.windows[window_key]



    def display_table_data_building(self, client_id, table_name):
        if self.checkWindowExists(client_id,table_name):
            new_window = self.getWindow(client_id, table_name)
            new_window.focus()
        else:
            new_window = self.createNewWindow(client_id, table_name)

            table_frame = create_table_frame(new_window)
            table_list, headers = self.db_manager.user_fetch_table_building(client_id)

            tree = insert_table_in_frame(headers, table_list, table_frame)
            new_window.wm_attributes("-topmost", True)

    def display_table_data_contract(self, client_id, table_name):
        window_key = f"{client_id}_{table_name}"
        if window_key in self.windows and self.windows[window_key].winfo_exists():
            self.windows[window_key].focus()
        else:
            new_window = self.create_new_window(table_name, client_id)
            self.windows[window_key] = new_window

            table_frame = create_table_frame(new_window)
            table_list, headers = user_fetch_table_contract(client_id)

            tree = insert_table_in_frame(headers, table_list, table_frame)
            new_window.wm_attributes("-topmost", True)

    def display_labor_data_user(self, client_id, table_name):
        window_key = f"{client_id}_{table_name}"
        if window_key in self.windows and self.windows[window_key].winfo_exists():
            self.windows[window_key].focus()
        else:
            new_window = self.create_new_window(table_name, client_id)
            self.windows[window_key] = new_window
            table_frame = create_table_frame(new_window)
            # get tables info and headers for it
            table_list, headers = user_fetch_table_labor(client_id)
            # create a tree, insert info
            tree = insert_table_in_frame(headers, table_list, table_frame)

            button_frame = customtkinter.CTkFrame(new_window)
            button_frame.grid(row=len(table_list) + 3, column=0, padx=10, pady=5, sticky="w")

            unique_building_ids = list(set(row[0] for row in table_list))
            unique_building_ids = sorted(unique_building_ids)
            unique_building_ids.insert(0, "NULL")  # Add null at the beginning
            optionmenuL = customtkinter.CTkLabel(button_frame, text="Search labor by building: ", fg_color="transparent")
            optionmenuL.grid(row=1, column=0, padx=5, pady=5)
            optionmenu = customtkinter.CTkOptionMenu(button_frame, values=[str(id) for id in unique_building_ids])
            optionmenu.grid(row=1, column=1, padx=5, pady=5)

            def update_table_in_frame():
                table_list, headers = user_fetch_table_labor(client_id, optionmenu.get())
                update_tables_in_frame(table_list, headers, tree)

            confirm_option = customtkinter.CTkButton(button_frame, text="Confirm selection", command=update_table_in_frame)
            confirm_option.grid(row=2, column=0, padx=5, pady=5)
            new_window.wm_attributes("-topmost", True)

    def display_worker_table_data(self, client_id, table_name):
        window_key = f"{client_id}_{table_name}"
        if window_key in self.windows and self.windows[window_key].winfo_exists():
            self.windows[window_key].focus()
        else:
            new_window = self.create_new_window(table_name, client_id)
            self.windows[window_key] = new_window


            table_frame = create_table_frame(new_window)
            # get tables info and headers for it
            table_list, headers = user_fetch_table_worker(client_id)
            # create a tree, insert info
            tree = insert_table_in_frame(headers, table_list, table_frame)

            button_frame = customtkinter.CTkFrame(new_window)
            button_frame.grid(row=len(table_list) + 3, column=0, padx=10, pady=5, sticky="w")

            unique_building_ids = list(set(row[0] for row in table_list))
            unique_building_ids = sorted(unique_building_ids)
            unique_building_ids.insert(0, "NULL")
            optionmenuL = customtkinter.CTkLabel(button_frame, text="Search workers by building: ", fg_color="transparent")
            optionmenuL.grid(row=1, column=0, padx=5, pady=5)
            optionmenu = customtkinter.CTkOptionMenu(button_frame, values=[str(id) for id in unique_building_ids])
            optionmenu.grid(row=1, column=1, padx=5, pady=5)

            def update_table_in_frame():
                table_list, headers = user_fetch_table_worker(client_id, optionmenu.get())
                update_tables_in_frame(table_list, headers, tree)

            confirm_option = customtkinter.CTkButton(button_frame, text="Confirm selection", command=update_table_in_frame)
            confirm_option.grid(row=2, column=0, padx=5, pady=5)
            new_window.wm_attributes("-topmost", True)

    def display_payment_table_data(self, client_id, table_name):
        window_key = f"{client_id}_{table_name}"
        if window_key in self.windows and self.windows[window_key].winfo_exists():
            self.windows[window_key].focus()
        else:
            new_window = self.create_new_window(table_name, client_id)
            self.windows[window_key] = new_window

            table_frame = create_table_frame(new_window)
            table_list, headers = user_fetch_table_payment(client_id)
            tree = insert_table_in_frame(headers, table_list, table_frame)

            button_frame = customtkinter.CTkFrame(new_window)
            button_frame.grid(row=len(table_list) + 3, column=0, padx=10, pady=5, sticky="w")

            contract_ids = list(set(row[1] for row in table_list))
            contract_ids = sorted(contract_ids)
            contract_ids.insert(0, "NULL")

            optionmenuL1 = customtkinter.CTkLabel(button_frame, text="Search payments by contract: ", fg_color="transparent")
            optionmenuL1.grid(row=1, column=0, padx=5, pady=5)

            optionmenu1 = customtkinter.CTkOptionMenu(button_frame, values=[str(id) for id in contract_ids])
            optionmenu1.grid(row=1, column=1, padx=5, pady=5)

            optionmenuL2 = customtkinter.CTkLabel(button_frame, text="Search payments type: ", fg_color="transparent")
            optionmenuL2.grid(row=2, column=0, padx=5, pady=5)
            payment_type = ["salary", "material", "phase"]
            payment_type.insert(0, "NULL")
            optionmenu2 = customtkinter.CTkOptionMenu(button_frame, values=payment_type)
            optionmenu2.grid(row=2, column=1, padx=5, pady=5)

            def update_table_in_frame():
                table_list, headers = user_fetch_table_payment(client_id, optionmenu1.get(), optionmenu2.get())
                update_tables_in_frame(table_list, headers, tree)

            confirm_option = customtkinter.CTkButton(button_frame, text="Confirm selection", command=update_table_in_frame)
            confirm_option.grid(row=3, column=0, padx=5, pady=5)
            new_window.wm_attributes("-topmost", True)

    def display_material_table_data(self, client_id, table_name):
        window_key = f"{client_id}_{table_name}"
        if window_key in self.windows and self.windows[window_key].winfo_exists():
            self.windows[window_key].focus()
        else:
            new_window = self.create_new_window(table_name, client_id)
            self.windows[window_key] = new_window

            table_frame = create_table_frame(new_window)
            table_list, headers = user_fetch_table_material(client_id)
            table_label = customtkinter.CTkLabel(table_frame, text="Materials Table", fg_color="transparent")
            table_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            tree = insert_table_in_frame(headers, table_list, table_frame)

            button_frame = customtkinter.CTkFrame(new_window)
            button_frame.grid(row=len(table_list) + 3, column=0, padx=10, pady=5, sticky="w")

            building_ids = list(set(row[1] for row in table_list))
            building_ids = sorted(building_ids)
            building_ids.insert(0, None)

            optionmenuL1 = customtkinter.CTkLabel(button_frame, text="Search materials by building: ", fg_color="transparent")
            optionmenuL1.grid(row=1, column=0, padx=5, pady=5)

            optionmenu1 = customtkinter.CTkOptionMenu(button_frame, values=[str(id) for id in building_ids])
            optionmenu1.grid(row=1, column=1, padx=5, pady=5)

            optionmenuL2 = customtkinter.CTkLabel(button_frame, text="Search used materials in labor: ", fg_color="transparent")
            optionmenuL2.grid(row=3, column=0, padx=5, pady=5)

            check_var = customtkinter.StringVar(value="0")
            checkbox = customtkinter.CTkCheckBox(button_frame, text=" ", variable=check_var, onvalue="1", offvalue="0")
            checkbox.grid(row=3, column=1, padx=5, pady=5)

            def update_table_in_frame():
                table_list, headers = user_fetch_table_material(client_id, optionmenu1.get(), checkbox.get())
                if checkbox.get() == "0":
                    table_label.configure(text="Materials Table")
                else:
                    table_label.configure(text="Used Materials in labor Table")
                update_tables_in_frame(table_list, headers, tree)

            confirm_option = customtkinter.CTkButton(button_frame, text="Confirm selection", command=update_table_in_frame)
            confirm_option.grid(row=4, column=0, padx=5, pady=5)
            new_window.wm_attributes("-topmost", True)




def open_user_window1(login, app11):

    def toLoginPage():
        print("pressed button")
        user_window.destroy()
        user_window.update()
        app11.deiconify()

    db_manager = DatabaseManager()
    window_user = WindowUser(db_manager)
    user_window = customtkinter.CTkToplevel()
    user_window.title("User Dashboard")
    user_window.geometry("800x600")
    cur_login = login
    cur_client_id = find_client_id_by_login(cur_login)
    app11.withdraw()
    cur_date = get_current_date()
    cur_time = get_current_time()
    hello_frame = customtkinter.CTkFrame(user_window)
    hello_frame.grid(row=0, column=0, padx=10, pady=5)
    hello_label = customtkinter.CTkLabel(hello_frame, text=f"Welcome, {cur_login}")
    hello_label.grid(row=1, column=0, padx=10, pady=5)
    cur_date_time = customtkinter.CTkLabel(hello_frame, text=f"Current time:  {cur_date} {cur_time}")
    cur_date_time.grid(row=2, column=0, padx=10, pady=5)
    update_time(cur_date_time, cur_date)
    select_frame = customtkinter.CTkFrame(user_window)
    select_frame.grid(row=3, column=0, padx=10, pady=5)
    select_label_desc = customtkinter.CTkLabel(select_frame, text=f"Show data")
    select_label_desc.grid(row=3, column=0, padx=10, pady=5)
    building_button = customtkinter.CTkButton(select_frame, text="Building list", command=lambda: window_user.display_table_data_building(cur_client_id, 'building'))
    building_button.grid(row=4, column=0, padx=10, pady=5)
    contract_button = customtkinter.CTkButton(select_frame, text="Contract list", command=lambda: window_user.display_table_data_contract(cur_client_id, 'contract'))
    contract_button.grid(row=5, column=0, padx=10, pady=5)
    labor_button = customtkinter.CTkButton(select_frame, text="Labor list", command=lambda: window_user.display_labor_data_user(cur_client_id, 'labor'))
    labor_button.grid(row=6, column=0, padx=10, pady=5)
    worker_button = customtkinter.CTkButton(select_frame, text="Worker list", command=lambda: window_user.display_worker_table_data(cur_client_id, 'worker'))
    worker_button.grid(row=7, column=0, padx=10, pady=5)
    pay_button = customtkinter.CTkButton(select_frame, text="Payments list", command=lambda: window_user.display_payment_table_data(cur_client_id, 'pay'))
    pay_button.grid(row=8, column=0, padx=10, pady=5)
    material_button = customtkinter.CTkButton(select_frame, text="Materials list", command=lambda: window_user.display_material_table_data(cur_client_id, 'material'))
    material_button.grid(row=9, column=0, padx=10, pady=5)

    toLogin = customtkinter.CTkButton(select_frame, text="To Login Page",
                                              command= toLoginPage)
    toLogin.grid(row=10, column=4, padx=10, pady=5, sticky="ns")



