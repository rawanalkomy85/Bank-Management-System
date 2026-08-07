import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# 1. CORE LOGIC CLASSES
# ==========================================

class Customer:
    def __init__(self, customer_id, name, phone, email, address):
        self.id = customer_id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

class Bank:
    accounts = []

    def __init__(self):
        self.customers = []
        self.customer_id = 1

    def add_customer(self, name, phone, email, address):
        if not (name and phone and email and address):
            return False, "All fields are required!"
        
        customer = Customer(self.customer_id, name, phone, email, address)
        self.customers.append(customer)
        self.customer_id += 1
        return True, f"Customer added successfully! ID: {customer.id}"

    def update_customer(self, cid, name=None, phone=None, email=None, address=None):
        for c in self.customers:
            if c.id == cid:
                if name: c.name = name
                if phone: c.phone = phone
                if email: c.email = email
                if address: c.address = address
                return True, "Customer updated successfully!"
        return False, "Customer not found!"

    def delete_customer(self, cid):
        for c in self.customers:
            if c.id == cid:
                self.customers.remove(c)
                return True, "Customer deleted successfully!"
        return False, "Customer not found!"

    @classmethod
    def add_account(cls, account):
        cls.accounts.append(account)

    @classmethod
    def find_account(cls, account_id):
        for account in cls.accounts:
            if account.account_id == account_id:
                return account
        return None

class Account:
    next_account_id = 1000

    def __init__(self, customer_id, account_type, balance):
        self.account_id = Account.next_account_id
        Account.next_account_id += 1
        self.customer_id = customer_id
        self.account_type = account_type
        self.__balance = max(0.0, balance)
        self.status = "Active"
        Bank.add_account(self)

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, amount):
        if amount >= 0:
            self.__balance = amount

    def update_account(self, account_type=None, balance=None):
        if account_type: self.account_type = account_type
        if balance is not None: self.balance = balance

    def close_account(self):
        self.status = "Closed"

class Transaction:
    def __init__(self, transaction_id, transaction_type, from_account_id, to_account_id, amount, date):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = amount
        self.date = date

class TransactionManager:
    transactions = []

    def deposit(self, to_account_id, amount):
        acc = Bank.find_account(to_account_id)
        if not acc: return False, "Account Not Found"
        if acc.status == "Closed": return False, "Account is closed."
        if amount <= 0: return False, "Amount must be > 0."

        acc.balance += amount
        t = Transaction(len(self.transactions) + 1, "Deposit", None, to_account_id, amount, dt.datetime.now())
        self.transactions.append(t)
        return True, f"Deposited successfully! New Balance: ${acc.balance:.2f}"

    def withdraw(self, from_account_id, amount):
        acc = Bank.find_account(from_account_id)
        if not acc: return False, "Account Not Found"
        if acc.status == "Closed": return False, "Account is closed."
        if amount <= 0: return False, "Amount must be > 0."
        if amount > acc.balance: return False, "Insufficient balance."

        acc.balance -= amount
        t = Transaction(len(self.transactions) + 1, "Withdraw", from_account_id, None, amount, dt.datetime.now())
        self.transactions.append(t)
        return True, f"Withdrawn successfully! New Balance: ${acc.balance:.2f}"

    def transfer(self, from_id, to_id, amount):
        sender = Bank.find_account(from_id)
        receiver = Bank.find_account(to_id)
        if not sender or not receiver: return False, "One or both accounts not found."
        if from_id == to_id: return False, "Cannot transfer to same account."
        if sender.status == "Closed" or receiver.status == "Closed": return False, "Account is closed."
        if amount <= 0: return False, "Amount must be > 0."
        if amount > sender.balance: return False, "Insufficient balance."

        sender.balance -= amount
        receiver.balance += amount
        t = Transaction(len(self.transactions) + 1, "Transfer", from_id, to_id, amount, dt.datetime.now())
        self.transactions.append(t)
        return True, "Transfer completed successfully!"

# --- Employee DB Management ---
employees_db = {}
next_employee_id = 1
bank = Bank()
transaction_manager = TransactionManager()

def create_employee(username, password, name, role="Employee"):
    global next_employee_id
    for emp in employees_db.values():
        if emp['username'] == username:
            return False, "Username exists!"
    
    emp_id = f"EMP-{next_employee_id:03d}"
    employees_db[emp_id] = {
        "employee_id": emp_id, "username": username, "password": password, "name": name, "role": role
    }
    next_employee_id += 1
    return True, f"Employee created! ID: {emp_id}"

create_employee("admin", "1234", "Main Admin", role="Admin")


# ==========================================
# 2. GUI APPLICATION (TKINTER)
# ==========================================

class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🏦 Bank Management System")
        self.geometry("850x600")
        self.current_user = None

        # Container Frame
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.show_login_frame()

    def show_login_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        login_frame = ttk.Frame(self.container, padding=20)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(login_frame, text="Bank Management System", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(login_frame, text="Username:").grid(row=1, column=0, sticky="e", pady=5)
        ent_user = ttk.Entry(login_frame)
        ent_user.grid(row=1, column=1, pady=5)

        ttk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky="e", pady=5)
        ent_pass = ttk.Entry(login_frame, show="*")
        ent_pass.grid(row=2, column=1, pady=5)

        def handle_login():
            u = ent_user.get().strip()
            p = ent_pass.get().strip()
            user = next((emp for emp in employees_db.values() if emp['username'] == u), None)
            
            if user and user['password'] == p:
                self.current_user = user
                self.show_main_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password!")

        ttk.Button(login_frame, text="Login", command=handle_login).grid(row=3, column=0, columnspan=2, pady=15)

    def show_main_dashboard(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        # Top Bar
        top_bar = ttk.Frame(self.container, padding=10)
        top_bar.pack(fill="x")
        
        user_info = f"Logged in as: {self.current_user['name']} ({self.current_user['role']})"
        ttk.Label(top_bar, text=user_info, font=("Arial", 10, "bold")).pack(side="left")
        ttk.Button(top_bar, text="Logout", command=self.show_login_frame).pack(side="right")

        # Tabs
        notebook = ttk.Notebook(self.container)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab Views
        self.setup_customer_tab(notebook)
        self.setup_account_tab(notebook)
        self.setup_transaction_tab(notebook)
        
        if self.current_user['role'] == "Admin":
            self.setup_employee_tab(notebook)

    # ------------------ CUSTOMERS TAB ------------------
    def setup_customer_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text="Customers")

        # Left Inputs
        f_left = ttk.LabelFrame(tab, text="Customer Actions", padding=10)
        f_left.pack(side="left", fill="y", padx=5, pady=5)

        ttk.Label(f_left, text="Name:").pack(anchor="w")
        e_name = ttk.Entry(f_left); e_name.pack(fill="x", pady=2)
        
        ttk.Label(f_left, text="Phone:").pack(anchor="w")
        e_phone = ttk.Entry(f_left); e_phone.pack(fill="x", pady=2)

        ttk.Label(f_left, text="Email:").pack(anchor="w")
        e_email = ttk.Entry(f_left); e_email.pack(fill="x", pady=2)

        ttk.Label(f_left, text="Address:").pack(anchor="w")
        e_address = ttk.Entry(f_left); e_address.pack(fill="x", pady=2)

        def add_c():
            succ, msg = bank.add_customer(e_name.get(), e_phone.get(), e_email.get(), e_address.get())
            if succ:
                messagebox.showinfo("Success", msg)
                refresh_c_list()
            else: messagebox.showerror("Error", msg)

        ttk.Button(f_left, text="Add Customer", command=add_c).pack(fill="x", pady=10)

        # Right Table
        f_right = ttk.Frame(tab)
        f_right.pack(side="right", fill="both", expand=True)

        cols = ("ID", "Name", "Phone", "Email", "Address")
        tree = ttk.Treeview(f_right, columns=cols, show="headings")
        for col in cols: tree.heading(col, text=col); tree.column(col, width=100)
        tree.pack(fill="both", expand=True)

        def refresh_c_list():
            for item in tree.get_children(): tree.delete(item)
            for c in bank.customers:
                tree.insert("", "end", values=(c.id, c.name, c.phone, c.email, c.address))

        refresh_c_list()

    # ------------------ ACCOUNTS TAB ------------------
    def setup_account_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text="Accounts")

        f_left = ttk.LabelFrame(tab, text="Create Account", padding=10)
        f_left.pack(side="left", fill="y", padx=5, pady=5)

        ttk.Label(f_left, text="Customer ID:").pack(anchor="w")
        e_cid = ttk.Entry(f_left); e_cid.pack(fill="x", pady=2)

        ttk.Label(f_left, text="Account Type:").pack(anchor="w")
        e_type = ttk.Combobox(f_left, values=["Savings", "Checking"]); e_type.pack(fill="x", pady=2)
        e_type.current(0)

        ttk.Label(f_left, text="Initial Balance:").pack(anchor="w")
        e_bal = ttk.Entry(f_left); e_bal.pack(fill="x", pady=2)

        def create_acc():
            try:
                cid = int(e_cid.get())
                bal = float(e_bal.get())
                if not any(c.id == cid for c in bank.customers):
                    messagebox.showerror("Error", "Customer ID Not Found!")
                    return
                acc = Account(cid, e_type.get(), bal)
                messagebox.showinfo("Success", f"Account Created! ID: {acc.account_id}")
                refresh_acc_list()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numerical values.")

        ttk.Button(f_left, text="Create Account", command=create_acc).pack(fill="x", pady=10)

        f_right = ttk.Frame(tab)
        f_right.pack(side="right", fill="both", expand=True)

        cols = ("Acc ID", "Customer ID", "Type", "Balance", "Status")
        tree = ttk.Treeview(f_right, columns=cols, show="headings")
        for col in cols: tree.heading(col, text=col); tree.column(col, width=90)
        tree.pack(fill="both", expand=True)

        def refresh_acc_list():
            for item in tree.get_children(): tree.delete(item)
            for a in Bank.accounts:
                tree.insert("", "end", values=(a.account_id, a.customer_id, a.account_type, f"${a.balance:.2f}", a.status))

        refresh_acc_list()

    # ------------------ TRANSACTIONS TAB ------------------
    def setup_transaction_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text="Transactions")

        # Operations Frame
        f_ops = ttk.LabelFrame(tab, text="Execute Transaction", padding=10)
        f_ops.pack(fill="x", pady=5)

        ttk.Label(f_ops, text="From Acc ID:").grid(row=0, column=0, padx=5)
        e_from = ttk.Entry(f_ops, width=10); e_from.grid(row=0, column=1, padx=5)

        ttk.Label(f_ops, text="To Acc ID:").grid(row=0, column=2, padx=5)
        e_to = ttk.Entry(f_ops, width=10); e_to.grid(row=0, column=3, padx=5)

        ttk.Label(f_ops, text="Amount:").grid(row=0, column=4, padx=5)
        e_amt = ttk.Entry(f_ops, width=10); e_amt.grid(row=0, column=5, padx=5)

        def do_deposit():
            try:
                succ, msg = transaction_manager.deposit(int(e_to.get()), float(e_amt.get()))
                messagebox.showinfo("Result", msg) if succ else messagebox.showerror("Error", msg)
                refresh_tx_list()
            except ValueError: messagebox.showerror("Error", "Invalid inputs!")

        def do_withdraw():
            try:
                succ, msg = transaction_manager.withdraw(int(e_from.get()), float(e_amt.get()))
                messagebox.showinfo("Result", msg) if succ else messagebox.showerror("Error", msg)
                refresh_tx_list()
            except ValueError: messagebox.showerror("Error", "Invalid inputs!")

        def do_transfer():
            try:
                succ, msg = transaction_manager.transfer(int(e_from.get()), int(e_to.get()), float(e_amt.get()))
                messagebox.showinfo("Result", msg) if succ else messagebox.showerror("Error", msg)
                refresh_tx_list()
            except ValueError: messagebox.showerror("Error", "Invalid inputs!")

        ttk.Button(f_ops, text="Deposit", command=do_deposit).grid(row=1, column=1, pady=10)
        ttk.Button(f_ops, text="Withdraw", command=do_withdraw).grid(row=1, column=3, pady=10)
        ttk.Button(f_ops, text="Transfer", command=do_transfer).grid(row=1, column=5, pady=10)

        # History Table
        cols = ("Tx ID", "Type", "From", "To", "Amount", "Date")
        tree = ttk.Treeview(tab, columns=cols, show="headings")
        for col in cols: tree.heading(col, text=col)
        tree.pack(fill="both", expand=True, pady=5)

        def refresh_tx_list():
            for item in tree.get_children(): tree.delete(item)
            for t in TransactionManager.transactions:
                date_str = t.date.strftime("%Y-%m-%d %H:%M")
                tree.insert("", "end", values=(t.transaction_id, t.transaction_type, t.from_account_id or "-", t.to_account_id or "-", f"${t.amount:.2f}", date_str))

    # ------------------ EMPLOYEES TAB (ADMIN) ------------------
    def setup_employee_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text="Employees (Admin)")

        f_left = ttk.LabelFrame(tab, text="Add Employee", padding=10)
        f_left.pack(side="left", fill="y", padx=5)

        ttk.Label(f_left, text="Username:").pack(anchor="w")
        e_u = ttk.Entry(f_left); e_u.pack(fill="x", pady=2)

        ttk.Label(f_left, text="Password:").pack(anchor="w")
        e_p = ttk.Entry(f_left, show="*"); e_p.pack(fill="x", pady=2)

        ttk.Label(f_left, text="Full Name:").pack(anchor="w")
        e_n = ttk.Entry(f_left); e_n.pack(fill="x", pady=2)

        ttk.Label(f_left, text="Role:").pack(anchor="w")
        e_r = ttk.Combobox(f_left, values=["Employee", "Admin"]); e_r.pack(fill="x", pady=2)
        e_r.current(0)

        def add_emp():
            succ, msg = create_employee(e_u.get(), e_p.get(), e_n.get(), e_r.get())
            if succ:
                messagebox.showinfo("Success", msg)
                refresh_emp_list()
            else: messagebox.showerror("Error", msg)

        ttk.Button(f_left, text="Add Employee", command=add_emp).pack(fill="x", pady=10)

        cols = ("Emp ID", "Username", "Name", "Role")
        tree = ttk.Treeview(tab, columns=cols, show="headings")
        for col in cols: tree.heading(col, text=col)
        tree.pack(side="right", fill="both", expand=True)

        def refresh_emp_list():
            for item in tree.get_children(): tree.delete(item)
            for emp in employees_db.values():
                tree.insert("", "end", values=(emp['employee_id'], emp['username'], emp['name'], emp['role']))

        refresh_emp_list()


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()