import tkinter as tk
from tkinter import ttk

import sqlite3
from tkinter import messagebox
def init_db():
    conn = sqlite3.connect('buisness_orders.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT IF NOT NULL,
    order_details TEXT IF NOT NULL,
    status TEXT IF NOT NULL)
    ''')
    conn.commit()
    conn.close()

def add_order():
    conn = sqlite3.connect('buisness_orders.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO orders (customer_name, order_details, status) VALUES (?,?, "Новый")',
                (customer_name_entry.get(),order_details_entry.get()))
    conn.commit()
    conn.close()
    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
    viev_orders()


def viev_orders():
    for i in tree.get_children():
        tree.delete(i)
    conn = sqlite3.connect('buisness_orders.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

def comlete_order():
    selected_item = tree.selection()
    if selected_item:
        order_id = tree.item(selected_item[0])['values'][0]
        conn=sqlite3.connect('buisness_orders.db')
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status = 'Завершен' WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()
        viev_orders()
    else:
        messagebox.showwarning("Предупреждение","Выберите заказ для завершения")

app = tk.Tk()
app.title('Система управления заказами')

tk.Label(app, text = 'Имя клиента').pack()

customer_name_entry = tk.Entry(app)
customer_name_entry.pack()

tk.Label(app, text = 'Детали заказа').pack()

order_details_entry = tk.Entry(app)
order_details_entry.pack()

add_button = tk.Button(app, text = 'Добавить заказ', command=add_order)
add_button.pack()

complete_button = tk.Button(app, text='Завершить заказ', command=comlete_order)
complete_button.pack()

columns = ('id', 'customer_name', 'order_details','status')
tree = ttk.Treeview(app, columns=columns, show='headings')
for column in columns:
    tree.heading(column, text=column)
tree.pack()

init_db()
viev_orders()
app.mainloop()
