import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory, askopenfilename

window = tk.Tk()
window.title("TCC das putas")

window.rowconfigure(0, weight=1)
window.rowconfigure(1, minsize=400, weight=1)
window.rowconfigure(2, weight=1)
window.columnconfigure(0, minsize=600, weight=1)

bodies = {}

## handlers 

def open_file():
    folderpath = askdirectory()
    if not folderpath:
        return
    ent_save_path.delete(0, tk.END)
    ent_save_path.insert(0, folderpath)

def delete_body_row(filepath):
    bodies[filepath].pack_forget()
    bodies[filepath].destroy()
    del bodies[filepath]

def add_body_row():
    filepath = askopenfilename(filetypes=[("All Files", "*.*")])
    
    if not filepath:
        return
    
    frm_body_row = tk.Frame(frm_body, relief=tk.SUNKEN, bd=2)
    lbl_file_path = tk.Label(frm_body_row, text=filepath, padx=10)
    btn_remove_body = tk.Button(frm_body_row, text='x', background='red', foreground='white', command= lambda: delete_body_row(filepath))

    bodies[filepath] = frm_body_row

    lbl_file_path.pack(side=tk.LEFT)
    btn_remove_body.pack(side=tk.RIGHT)
    frm_body_row.pack(fill=tk.X)


## widgets creation

frm_header = tk.Frame(window, relief=tk.RAISED, border=2)
lbl_save_path = tk.Label(frm_header, text='Save path:')
ent_save_path = tk.Entry(frm_header, width=50, )
btn_save_path = tk.Button(frm_header, text='Open', height=1, command=open_file)
btn_add_body = tk.Button(frm_header, text='+', background='green', foreground='white', command=add_body_row)

frm_body = tk.Frame(window)

frm_footer = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_run = tk.Button(frm_footer, text='Run', width=6, height=3, background='green', foreground='white')

## widgets placement

lbl_save_path.pack(side=tk.LEFT)
ent_save_path.pack(side=tk.LEFT, padx=5)
btn_save_path.pack(side=tk.LEFT)
btn_add_body.pack(side=tk.RIGHT)

btn_run.pack()

frm_header.grid(row=0, column=0, sticky='ew')
frm_body.grid(row=1, column=0, sticky='nsew')
frm_footer.grid(row=2, column=0, sticky='ew')
    
## end

window.mainloop()