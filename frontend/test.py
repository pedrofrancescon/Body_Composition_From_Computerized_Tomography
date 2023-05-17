from copy import deepcopy
import tkinter as tk
from tkinter.messagebox import showinfo
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory, askopenfilename

paddings = {'padx': 5, 'pady': 5}
entry_font = {'font': ('Helvetica', 11)}

#### Nav
def show_page(page_number):
    global current_page
    current_page.pack_forget()
    current_page = pages[page_number]
    current_page.pack()

#### App Window
app = tk.Tk()
app.title('Composição Corporal')
app.geometry('1200x900')
app.configure(bg='white')


#### frame tela boas vindas
home = tk.Frame(app)
home.configure(bg='white')
# label
home_label = ttk.Label(home, text='Composição Corporal')
home_label.pack()
# button
home_button = ttk.Button(home, text='Iniciar', command=lambda: show_page(1), padding={'padx': 5, 'pady': 5})
home_button.pack()



#### frame escolha de diretorios
pathSelectionScreen = tk.Frame(app)
pathSelectionScreen.configure(bg='white')
pathSelectionScreen.rowconfigure(0, weight=1)
pathSelectionScreen.rowconfigure(1, minsize=400, weight=1)
pathSelectionScreen.rowconfigure(2, weight=1)
pathSelectionScreen.columnconfigure(0, minsize=600, weight=1)

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
  
  frm_body_row = tk.Frame(frm_body, relief=tk.SUNKEN, bg='white', border=1,**paddings)
  lbl_file_path = tk.Label(frm_body_row, text=filepath, bg='white', **paddings)
  btn_remove_body = tk.Button(frm_body_row, text='x', background='red', foreground='white', command= lambda: delete_body_row(filepath), **paddings)

  bodies[filepath] = frm_body_row

  lbl_file_path.pack(side=tk.LEFT)
  btn_remove_body.pack(side=tk.RIGHT)
  frm_body_row.pack(fill=tk.X)


      ## widgets creation

frm_header = tk.Frame(pathSelectionScreen, relief=tk.RAISED, bg='white')
lbl_save_path = tk.Label(frm_header, text='Save path:', background='white', foreground='black', **paddings, **entry_font)
ent_save_path = tk.Entry(frm_header, width=50, background='white', foreground='black', **entry_font)
btn_save_path = tk.Button(frm_header, text='Open', height=1, command=open_file, background='white', foreground='black', **paddings, **entry_font)
btn_add_body = tk.Button(frm_header, text='+', background='green', foreground='white', command=add_body_row, **paddings, **entry_font)

frm_body = tk.Frame(pathSelectionScreen, bg='white')

frm_footer = tk.Frame(pathSelectionScreen, relief=tk.RAISED, bg='white')
btn_run = tk.Button(frm_footer, text='Run', width=6, height=3, command=lambda: show_page(2), background='green', foreground='white', **entry_font, **paddings)

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

#### frame processamento
processingScreen = tk.Frame(app)

frm_body_row2 = tk.Frame(frm_body, relief=tk.SUNKEN, bg='white', border=1,**paddings)
lbl_file_path2 = tk.Label(frm_body_row2, text="paciente", bg='white', **paddings)
lbl_status_proc = tk.Button(frm_body_row2, text='x', background='red', foreground='white', command= lambda: delete_body_row(filepath), **paddings)


lbl_file_path2.pack(side=tk.LEFT)
lbl_status_proc.pack(side=tk.RIGHT)
frm_body_row2.pack(fill=tk.X)

frm_header2 = tk.Frame(processingScreen, relief=tk.RAISED, bg='white')
lbl_save_path2 = tk.Label(frm_header2, text='Save path:', background='white', foreground='black', **paddings, **entry_font)
lbl_saved_path2 = tk.Label(frm_header2, text='Save path:', background='white', foreground='black', **paddings, **entry_font)
btn_save_path2 = tk.Button(frm_header2, text='Open', height=1, command=open_file, background='white', foreground='black', **paddings, **entry_font)
btn_add_body2 = tk.Button(frm_header2, text='+', background='green', foreground='white', command=add_body_row, **paddings, **entry_font)

frm_body2 = tk.Frame(processingScreen, bg='white')

frm_footer2 = tk.Frame(processingScreen, relief=tk.RAISED, bg='white')
btn_run2 = tk.Button(frm_footer2, text='Run', width=6, height=3, command=lambda: show_page(3), background='green', foreground='white', **entry_font, **paddings)

lbl_save_path2.pack(side=tk.LEFT)
lbl_saved_path2.pack(side=tk.LEFT, padx=5)
btn_save_path2.pack(side=tk.LEFT)
btn_add_body2.pack(side=tk.RIGHT)

btn_run2.pack()

frm_header2.grid(row=0, column=0, sticky='ew')
frm_body2.grid(row=1, column=0, sticky='nsew')
frm_footer2.grid(row=2, column=0, sticky='ew')

#### frame resultados
resultsScreen = tk.Frame(app)
lbl_result = ttk.Label(resultsScreen, text='Deu tudo errado!!!', background='white', **entry_font)
lbl_result.pack()

# Dicionário para mapear as páginas
pages = {0: home, 1: pathSelectionScreen, 2: processingScreen, 3: resultsScreen}
current_page = home
current_page.pack()

app.mainloop()