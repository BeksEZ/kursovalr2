class Material:
    def __init__(self, m_id, s_id, name, date_got, amount, cost, m_units):
        self.m_id = m_id
        self.s_id = s_id
        self.name = name
        self.date_got = date_got
        self.amount = amount
        self.cost = cost
        self.m_units = m_units

    def createEditWindow(self, tableName):
        window_key = f"{self, tableName}"
        if window_key in self.windows and self.windows[window_key].winfo_exists():
            self.windows[window_key].focus()
        else:
            new_window = self.createNewWindowTables(tableName)
            self.windows[window_key] = new_window

            selectType = customtkinter.CTkFrame(new_window)
            selectType.grid(row=10, column=0, padx=10, pady=5)

            chooseTypeL = customtkinter.CTkLabel(selectType, text="Choose action type:")
            chooseTypeL.grid(row=1, column=0, padx=10, pady=5)
            chooseType = customtkinter.CTkOptionMenu(selectType, values=["add", "edit", "delete"])
            chooseType.grid(row=1, column=1, padx=5, pady=5)

            chooseTableL = customtkinter.CTkLabel(selectType, text="Choose table:")
            chooseTableL.grid(row=2, column=0, padx=10, pady=5)
            tables = fetch_table_name()
            chooseTable = customtkinter.CTkOptionMenu(selectType, values=tables)
            chooseTable.grid(row=2, column=1, padx=5, pady=5)

            inputInfo = customtkinter.CTkFrame(new_window)
            inputInfo.grid(row=20, column=0, padx=10, pady=5)

            def optionmenu_callback(choice):
                if choice == "user":
                    clients = list(set(self.get_clients_without_accounts()))
                    clients = sorted(clients)
                    clients = list(set(row[1] for row in clients))
                    self.client = customtkinter.CTkOptionMenu(inputInfo, values=[str(id) for id in clients])
                    self.client.grid(row=3, column=0, padx=10, pady=5)
                elif choice == "admin":
                    self.client_id = None

            def actionOnAccounts(actionType):
                if actionType == "add":
                    login = customtkinter.CTkEntry(inputInfo, placeholder_text="login")
                    login.grid(row=0, column=0, padx=10, pady=5)
                    password = customtkinter.CTkEntry(inputInfo, placeholder_text="password")
                    password.grid(row=1, column=0, padx=10, pady=5)
                    accType = customtkinter.CTkOptionMenu(inputInfo, values=["admin", "user"],
                                                          command=optionmenu_callback)
                    accType.grid(row=2, column=0, padx=10, pady=5)
                    self.client = customtkinter.CTkOptionMenu(inputInfo, values=[])  # Initialize as empty option menu
                    return login, password, accType
                elif actionType == "edit":
                    accounts = list(set((self.getAccounts())))
                    accounts = sorted(accounts)
                    accounts = list(set(row[0] for row in accounts))
                    accLogin = customtkinter.CTkOptionMenu(inputInfo, values=[str(login) for login in accounts])
                    accLogin.grid(row=0, column=0, padx=10, pady=5)
                    accChange = customtkinter.CTkOptionMenu(inputInfo,
                                                            values=["login", "password", "account_type", "req_id"])
                    accChange.grid(row=0, column=1, padx=10, pady=5)
                    new_value = customtkinter.CTkEntry(inputInfo, placeholder_text="new value...")
                    new_value.grid(row=1, column=0, padx=10, pady=5)
                    self.client = customtkinter.CTkOptionMenu(inputInfo, values=[])  # Initialize as empty option menu
                    return accLogin, accChange, new_value
                elif actionType == "delete":
                    accounts = list(set((self.getAccounts())))
                    accounts = sorted(accounts)
                    accounts = list(set(row[0] for row in accounts))
                    accLogin = customtkinter.CTkOptionMenu(inputInfo, values=[str(login) for login in accounts])
                    accLogin.grid(row=0, column=0, padx=10, pady=5)
                    return accLogin

            def actionOnMaterial(actionType):
                if actionType == "add":
                    suppliers = sorted(list(set(self.getSuppliers())))
                    supplier = customtkinter.CTkOptionMenu(inputInfo, values=[str(name) for name in suppliers],
                                                           )
                    supplier.grid(row=0, column=0, padx=10, pady=5)

                    materialName = customtkinter.CTkEntry(inputInfo, placeholder_text="material name")
                    materialName.grid(row=1, column=0, padx=10, pady=5)
                    materialAmount = customtkinter.CTkEntry(inputInfo, placeholder_text="material amount")
                    materialAmount.grid(row=2, column=0, padx=10, pady=5)
                    materialCost = customtkinter.CTkEntry(inputInfo, placeholder_text="material cost")
                    materialCost.grid(row=3, column=0, padx=10, pady=5)

                    materialUnits = customtkinter.CTkOptionMenu(inputInfo, values=["kilo", "piece", "liter", "m^3"],
                                                                )
                    materialUnits.grid(row=4, column=0, padx=10, pady=5)
                    buildings = sorted(list(set(self.fetch_table("building"))))
                    buildings = list(set(row[2] for row in buildings))
                    materialBuilding = customtkinter.CTkOptionMenu(inputInfo, values=[str(name) for name in buildings],
                                                                   )
                    materialBuilding.grid(row=5, column=0, padx=10, pady=5)

                    return materialName.get(), materialAmount.get(), materialCost.get(), materialUnits.get(), materialBuilding.get()
                elif actionType == "edit":
                    materials = list(set((self.fetch_table("material"))))
                    materials = sorted(materials)
                    materials = list(set(row[2] for row in materials))
                    materialName = customtkinter.CTkOptionMenu(inputInfo, values=[str(name) for name in materials])
                    materialName.grid(row=0, column=0, padx=10, pady=5)

                    def optionMaterial(choice):
                        if choice == "material_units":
                            materialNewValue = customtkinter.CTkOptionMenu(inputInfo,
                                                                           values=["kilo", "piece", "liter", "m^3"],
                                                                           )
                            materialNewValue.grid(row=4, column=0, padx=10, pady=5)

                        elif choice == "building_name":
                            buildings = sorted(list(set(self.fetch_table("building"))))
                            buildings = list(set(row[2] for row in buildings))
                            materialNewValue = customtkinter.CTkOptionMenu(inputInfo,
                                                                           values=[str(name) for name in buildings],
                                                                           )
                            materialNewValue.grid(row=5, column=0, padx=10, pady=5)

                        else:
                            materialNewValue = customtkinter.CTkEntry(inputInfo, placeholder_text="new value...")
                            materialNewValue.grid(row=1, column=0, padx=10, pady=5)

                    materialChange = customtkinter.CTkOptionMenu(inputInfo,
                                                                 values=["material_name", "material_dategot",
                                                                         "material_amount", "material_cost",
                                                                         "material_units", "building_name"],
                                                                 command=optionMaterial)
                    materialChange.grid(row=0, column=1, padx=10, pady=5)

                    return materialName.get(), materialChange.get(), materialNewValue

                elif actionType == "delete":
                    materials = list(set((self.fetch_table("material"))))
                    materials = sorted(materials)
                    materials = list(set(row[2] for row in materials))
                    materialChoose = customtkinter.CTkOptionMenu(inputInfo, values=[str(name) for name in materials])
                    materialChoose.grid(row=0, column=0, padx=10, pady=5)
                    materialChosen = materialChoose.get()
                    return materialChosen

            def changeTypebutton():
                if chooseTable.get() == "accounts":
                    if chooseType.get() == "add":
                        login, password, accType = actionOnAccounts("add")
                        confirmButton = customtkinter.CTkButton(selectType, text="Confirm action",
                                                                command=lambda: confirmActionAccount("add", login.get(),
                                                                                                     password.get(),
                                                                                                     accType.get()))
                        confirmButton.grid(row=5, column=0, padx=10, pady=5)
                    elif chooseType.get() == "edit":
                        accLogin, accChange, new_value = actionOnAccounts("edit")
                        confirmButton = customtkinter.CTkButton(selectType, text="Confirm action",
                                                                command=lambda: confirmActionAccount("edit",
                                                                                                     accLogin.get(),
                                                                                                     accChange.get(),
                                                                                                     new_value.get()))
                        confirmButton.grid(row=5, column=0, padx=10, pady=5)
                    elif chooseType.get() == "delete":
                        accLogin = actionOnAccounts("delete")
                        confirmButton = customtkinter.CTkButton(selectType, text="Confirm action",
                                                                command=lambda: confirmActionAccount("delete",
                                                                                                     accLogin.get()))
                        confirmButton.grid(row=5, column=0, padx=10, pady=5)
                if chooseTable.get() == "material":
                    if chooseType.get() == "add":
                        materialName, materialAmount, materialCost, materialUnits, materialBuilding = actionOnMaterial(
                            "add")
                        confirmButton = customtkinter.CTkButton(selectType, text="Confirm action",
                                                                command=lambda: confirmActionBuilding("add",
                                                                                                      materialName,
                                                                                                      materialAmount,
                                                                                                      materialCost,
                                                                                                      materialUnits,
                                                                                                      materialBuilding))
                        confirmButton.grid(row=5, column=0, padx=10, pady=5)
                    elif chooseType.get() == "edit":
                        accLogin, accChange, new_value = actionOnMaterial("edit")
                        confirmButton = customtkinter.CTkButton(selectType, text="Confirm action",
                                                                command=lambda: confirmActionBuilding("edit",
                                                                                                      accLogin.get(),
                                                                                                      accChange.get(),
                                                                                                      new_value.get()))
                        confirmButton.grid(row=5, column=0, padx=10, pady=5)
                    elif chooseType.get() == "delete":
                        accLogin = actionOnMaterial("delete")
                        confirmButton = customtkinter.CTkButton(selectType, text="Confirm action",
                                                                command=lambda: confirmActionBuilding("delete",
                                                                                                      accLogin.get()))
                        confirmButton.grid(row=5, column=0, padx=10, pady=5)

            def confirmActionAccount(actionType, param1, param2=None, param3=None):
                conn = connect_to_db()
                cursor = conn.cursor()
                if actionType == "add":
                    self.client_id = None if self.client is None else self.getClientIdByName(self.client.get())
                    query = """
                                   INSERT INTO public.accounts (login, password, acc_type, req_id)
                                   VALUES (%s, %s, %s, %s)
                                   RETURNING acc_id;
                                   """
                    cursor.execute(query, (param1, param2, param3, self.client_id))
                    acc_id = cursor.fetchone()[0]
                    confirmation_label.configure(text=f"successfully created account with id: {acc_id}")
                elif actionType == "edit":
                    query = f"UPDATE public.accounts SET {param2} = %s WHERE login = %s"
                    cursor.execute(query, (param3, param1))
                    confirmation_label.configure(text=f"successfully updated account: {param1}")
                elif actionType == "delete":
                    query = "DELETE FROM public.accounts WHERE login = %s"
                    cursor.execute(query, (param1,))
                    confirmation_label.configure(text=f"successfully deleted account: {param1}")
                conn.commit()
                cursor.close()
                conn.close()



            confirmation_label = customtkinter.CTkLabel(inputInfo, text="", fg_color="transparent")
            confirmation_label.grid(row=4, column=0, padx=20, pady=10)


            new_window.wm_attributes("-topmost", True)