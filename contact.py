import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import csv

# Initialize main window
root = tk.Tk()
root.title("Professional Contact Book")
root.geometry("700x750")
root.config(bg="#f5f5f5")

# Contact storage
contacts = []

# Functions for managing contacts
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if name and phone:
        contacts.append({"name": name, "phone": phone, "email": email, "address": address})
        clear_form()
        messagebox.showinfo("Success", "Contact added successfully!")
        display_contacts()
    else:
        messagebox.showwarning("Input Error", "Name and phone number are required!")

def display_contacts():
    contact_list.delete(*contact_list.get_children())
    for contact in contacts:
        contact_list.insert('', tk.END, values=(contact["name"], contact["phone"], contact["email"]))

def search_contact():
    search_term = search_entry.get().lower()
    contact_list.delete(*contact_list.get_children())
    for contact in contacts:
        if search_term in contact["name"].lower() or search_term in contact["phone"]:
            contact_list.insert('', tk.END, values=(contact["name"], contact["phone"], contact["email"]))

def update_contact():
    selected_item = contact_list.focus()
    if selected_item:
        index = contact_list.index(selected_item)
        contacts[index]["name"] = name_entry.get()
        contacts[index]["phone"] = phone_entry.get()
        contacts[index]["email"] = email_entry.get()
        contacts[index]["address"] = address_entry.get()
        display_contacts()
        clear_form()
        messagebox.showinfo("Success", "Contact updated successfully!")
    else:
        messagebox.showwarning("Selection Error", "No contact selected!")

def delete_contact():
    selected_item = contact_list.focus()
    if selected_item:
        index = contact_list.index(selected_item)
        contacts.pop(index)
        contact_list.delete(selected_item)
        messagebox.showinfo("Success", "Contact deleted successfully!")
    else:
        messagebox.showwarning("Selection Error", "No contact selected!")

def clear_form():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

def show_details():
    selected_item = contact_list.focus()
    if selected_item:
        index = contact_list.index(selected_item)
        contact = contacts[index]
        details_message = f"Name: {contact['name']}\nPhone: {contact['phone']}\nEmail: {contact['email']}\nAddress: {contact['address']}"
        messagebox.showinfo("Contact Details", details_message)
    else:
        messagebox.showwarning("Selection Error", "No contact selected!")

def export_contacts():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filename:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Email", "Address"])
            for contact in contacts:
                writer.writerow([contact['name'], contact['phone'], contact['email'], contact['address']])
        messagebox.showinfo("Success", "Contacts exported successfully!")

def import_contacts():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contacts.append(row)
        display_contacts()
        messagebox.showinfo("Success", "Contacts imported successfully!")

# GUI Styling
style = ttk.Style()
style.configure("TButton", font=('Helvetica', 12), padding=6)
style.configure("TEntry", padding=10, font=('Helvetica', 12))

# Frames
top_frame = tk.Frame(root, bg="#f0f0f0")
top_frame.pack(pady=20)

form_frame = tk.Frame(root, bg="#ffffff")
form_frame.pack(pady=20)

list_frame = tk.Frame(root, bg="#f9f9f9")
list_frame.pack(pady=20)

# Labels and Entries for contact details
tk.Label(form_frame, text="Name:", font=('Helvetica', 12), bg="#ffffff").grid(row=0, column=0, padx=10, pady=5)
name_entry = ttk.Entry(form_frame, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Phone:", font=('Helvetica', 12), bg="#ffffff").grid(row=1, column=0, padx=10, pady=5)
phone_entry = ttk.Entry(form_frame, width=30)
phone_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Email:", font=('Helvetica', 12), bg="#ffffff").grid(row=2, column=0, padx=10, pady=5)
email_entry = ttk.Entry(form_frame, width=30)
email_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Address:", font=('Helvetica', 12), bg="#ffffff").grid(row=3, column=0, padx=10, pady=5)
address_entry = ttk.Entry(form_frame, width=30)
address_entry.grid(row=3, column=1, padx=10, pady=5)

# Buttons for Add, Update, Delete, Search, and Export
tk.Button(top_frame, text="Add Contact", command=add_contact, bg="#4CAF50", fg="white", font=('Helvetica', 12), width=15).grid(row=0, column=0, padx=10)
tk.Button(top_frame, text="Update Contact", command=update_contact, bg="#2196F3", fg="white", font=('Helvetica', 12), width=15).grid(row=0, column=1, padx=10)
tk.Button(top_frame, text="Delete Contact", command=delete_contact, bg="#f44336", fg="white", font=('Helvetica', 12), width=15).grid(row=0, column=2, padx=10)
tk.Button(top_frame, text="Clear Form", command=clear_form, bg="#FF9800", fg="white", font=('Helvetica', 12), width=15).grid(row=1, column=0, padx=10, pady=10)
tk.Button(top_frame, text="Show Details", command=show_details, bg="#00BCD4", fg="white", font=('Helvetica', 12), width=15).grid(row=1, column=1, padx=10, pady=10)

# Contact List Display
columns = ('Name', 'Phone', 'Email')
contact_list = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
contact_list.heading('Name', text="Name")
contact_list.heading('Phone', text="Phone")
contact_list.heading('Email', text="Email")
contact_list.pack()

# Search functionality
tk.Label(root, text="Search by Name or Phone:", font=('Helvetica', 12), bg="#f5f5f5").pack(pady=10)
search_entry = ttk.Entry(root, width=30)
search_entry.pack(pady=5)
tk.Button(root, text="Search", command=search_contact, bg="#FF9800", fg="white", font=('Helvetica', 12), width=15).pack(pady=5)

# Export/Import buttons
tk.Button(root, text="Export Contacts", command=export_contacts, bg="#8BC34A", fg="white", font=('Helvetica', 12), width=20).pack(pady=5)
tk.Button(root, text="Import Contacts", command=import_contacts, bg="#8BC34A", fg="white", font=('Helvetica', 12), width=20).pack(pady=5)

# Run the main event loop
root.mainloop()
