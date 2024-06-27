import customtkinter as CTk
import subprocess
from bs4 import BeautifulSoup
import requests
from tkinter import messagebox
import webbrowser

data_dict = {}

def clicked(event,click_type):
    if click_type == "text":
        package.delete(0, "end")
        package.insert(CTk.END, data_dict[event]['name'])
    elif click_type == "visit-button":
        webbrowser.open_new_tab(data_dict[event]['url'])

def make_lambda(x,click_type):
    return lambda some_var: clicked(x,click_type)

def search():
    global package_name, package_version, all_packs
    search_pack = package.get()
    source = requests.get('https://pypi.org/search/?q=' + search_pack).text
    soup = BeautifulSoup(source, 'lxml')
    all_packs = soup.find_all('a', class_='package-snippet')[0:10]
    number = len(all_packs)
    show = CTk.CTkLabel(window, text=f'The top {number} search results are', font=('Arial Black', 15,"bold"), width=30)
    show.grid(column=0, row=4)
    follow_up = CTk.CTkLabel(window,text=f'Click on name to copy to search bar', font=('Arial Black', 12,"bold"), width=10)
    follow_up.grid(column=0,row=5)
    row_num = 6
    for i,name in enumerate(all_packs):
        package_name = name.h3.span.text
        package_version = name.find('span', class_='package-snippet__version').text
        package_description = name.p.text
        website_url = "https://pypi.org" + name.get('href')
        data_dict[i+1] = {"name": package_name, "version": package_version, "description": package_description, "url":website_url}
        display = package_name, package_version
        result1 = CTk.CTkLabel(window, text=display, font=('Arial Black', 15,"bold"), width=80,fg_color = "black",text_color="white")
        result1.grid(column=0, row=row_num)
        result1.bind("<Button-1>", make_lambda(i+1,"text"))

        visit_button = CTk.CTkButton(window,text="visit",font=('Arial Black', 15,"bold"),fg_color="green")
        visit_button.grid(column=1,row=row_num)
        visit_button.bind("<Button-1>",make_lambda(i+1,"visit-button"))

        row_num = row_num + 1

def install():
    file = package.get()
    result = subprocess.run(['pip', 'install', '--no-cache-dir', file], capture_output=True, text=True)
    if result.stderr == '':
        messagebox.showinfo('Result', 'Package installed successfully')
    else:
        messagebox.showerror('Error', f'Failed to install package: {result.stderr}')

def update():
    file = package.get()
    result = subprocess.run(['pip', 'install', '--no-cache-dir', '--upgrade', file], capture_output=True, text=True)
    if result.stderr == '':
        messagebox.showinfo('Result', 'Package updated successfully')
    else:
        messagebox.showerror('Error', f'Failed to update package: {result.stderr}')

def uninstall():
    file = package.get()
    result = subprocess.run(['pip', 'uninstall', '-y', file], capture_output=True, text=True)
    if result.stderr == '':
        messagebox.showinfo('Result', 'Package uninstalled successfully')
    else:
        messagebox.showerror('Error', f'Failed to uninstall package: {result.stderr}')

def on_window_resize(event):
    for child in window.winfo_children():
        child.grid_configure(padx=10, pady=10)

def center_window(window):
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    position_right = int(window.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(window.winfo_screenheight() / 2 - window_height / 2)

    window.geometry(f"+{position_right}+{position_down}")

CTk.set_appearance_mode("dark")

window = CTk.CTk()
window.title('Enhanced-GUI-for-Pip-Installer')
window.geometry('1000x750')

center_window(window)
window.resizable(True, True)

main = CTk.CTkLabel(window, text='Install Python Packages', font=("Helvetica", 20, "bold"))
main.grid(column=0, row=0)

text = CTk.CTkLabel(window, text='Enter package name', font=("Helvetica", 20,"bold"))
text.grid(column=0, row=1)

package = CTk.CTkEntry(window, width=150)
package.grid(column=0, row=3)
package.focus()

search_button = CTk.CTkButton(window, text='Search', command=search)
search_button.grid(column=1, row=3)

install_button = CTk.CTkButton(window, text='Install', command=install)
install_button.grid(column=2, row=3)

update_button = CTk.CTkButton(window, text='Update', command=update)
update_button.grid(column=3, row=3)

uninstall_button = CTk.CTkButton(window, text='Uninstall', command=uninstall)
uninstall_button.grid(column=4, row=3)

window.bind("<Configure>", on_window_resize)

window.mainloop()
