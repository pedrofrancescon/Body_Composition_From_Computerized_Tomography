import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
import tkinter.ttk as ttk


paddings = {'padx': 5, 'pady': 5}
entry_font = {'font': ('Helvetica', 12)}
description = "Selecione pastas contendo arquivos DICOM de exames tomográficos para determinação automatica da composição corporal dos pacientes"

def root_window():
  app = tk.Tk()
  app.title('Composição Corporal')
  app.geometry('1200x900')
  app.configure(bg='white')
  return app

def clear_window(window):
  for widget in window.winfo_children():
    widget.destroy()

## screens
def home(app):
  home = tk.Frame(app)
  home.configure(bg='white')
  lbl_home = ttk.Label(home, text='Composição Corporal', background='white',**entry_font)
  lbl_home.pack()
  lbl_description = ttk.Label(home, text=description, background='white', padding={'padx': 5, 'pady': 5}, **entry_font)
  lbl_description.pack()
  btn_home = ttk.Button(home, text='Iniciar', command=lambda: path_selection(app), padding={'padx': 5, 'pady': 5})
  btn_home.pack()
  home.pack()

def path_selection(app):
  clear_window(app)

  txt_save_path = tk.StringVar()
  bodies = {}

  pathSelectionScreen = tk.Frame(app)
  pathSelectionScreen.configure(bg='white')
  pathSelectionScreen.rowconfigure(0, weight=1)
  pathSelectionScreen.rowconfigure(1, minsize=400, weight=1)
  pathSelectionScreen.rowconfigure(2, weight=1)
  pathSelectionScreen.columnconfigure(0, minsize=600, weight=1)

  frm_body = tk.Frame(pathSelectionScreen, bg='white')
  frm_header = tk.Frame(pathSelectionScreen, relief=tk.RAISED, bg='white')
  lbl_save_path = tk.Label(frm_header, text='Save path:', background='white', foreground='black', **paddings, **entry_font)
  ent_save_path = tk.Entry(frm_header, textvariable=txt_save_path, width=50, background='white', foreground='black', **entry_font)
  btn_save_path = tk.Button(frm_header, text='Open', height=1, command=lambda:open_file(ent_save_path), background='white', foreground='black', **paddings, **entry_font)
  btn_add_body = tk.Button(frm_header, text='+', background='green', foreground='white', command=lambda:add_body_row(frm_body, bodies), **paddings, **entry_font)

  frm_footer = tk.Frame(pathSelectionScreen, relief=tk.RAISED, bg='white')
  btn_run = tk.Button(frm_footer, text='Run', width=6, height=3, command=lambda: processing(app, txt_save_path, bodies), background='green', foreground='white', **entry_font, **paddings)
  
  ## widgets placement
  lbl_save_path.pack(side=tk.LEFT)
  ent_save_path.pack(side=tk.LEFT, padx=5)
  btn_save_path.pack(side=tk.LEFT)
  btn_add_body.pack(side=tk.RIGHT)

  btn_run.pack()

  frm_header.grid(row=0, column=0, sticky='ew')
  frm_body.grid(row=1, column=0, sticky='nsew')
  frm_footer.grid(row=2, column=0, sticky='ew')
  pathSelectionScreen.pack()

def processing(app,txt_save_path: str,bodies: dict):
  clear_window(app)

  processingScreen = tk.Frame(app)
  frm_proc_body = tk.Frame(processingScreen, bg='white')

  frm_proc_header = tk.Frame(processingScreen, relief=tk.RAISED, bg='white')
  lbl_proc_save_path = tk.Label(frm_proc_header, text='Save path:', background='white', foreground='black', **paddings, **entry_font)
  lbl_proc_saved_path = tk.Label(frm_proc_header, textvariable=txt_save_path, background='white', foreground='black', **paddings, **entry_font)
  lbl_info_body = tk.Label(frm_proc_header, text='Info', background='white', foreground='black', **paddings, **entry_font)
  lbl_proc_status = tk.Label(frm_proc_header, text='Status', background='white', foreground='black', **paddings, **entry_font)

  frm_proc_footer = tk.Frame(processingScreen, relief=tk.RAISED, bg='white')
  btn_proc_res = tk.Button(frm_proc_footer, text='Visualizar', command=lambda: results(app), width=6, height=3, background='green', foreground='white', **entry_font, **paddings)

  for filep in bodies.keys():
      createProcsRowFrame(frm_proc_body, filep)

  lbl_proc_save_path.pack(side=tk.LEFT)
  lbl_proc_saved_path.pack(side=tk.LEFT, padx=5)
  lbl_info_body.pack(side=tk.LEFT)
  lbl_proc_status.pack(side=tk.RIGHT)

  btn_proc_res.pack()

  frm_proc_header.grid(row=0, column=0, sticky='ew')
  frm_proc_body.grid(row=1, column=0, sticky='nsew')
  frm_proc_footer.grid(row=2, column=0, sticky='ew')
  processingScreen.pack()

def results(app):
  clear_window(app)
  resultsScreen = tk.Frame(app, background='white')
  lbl_result = ttk.Label(resultsScreen, text='Deu tudo errado!!!', background='white', **entry_font)
  lbl_result.pack()
  photo = tk.PhotoImage(file='./wdw_hbone/4899.png')
  image_label = ttk.Label(
      resultsScreen,
      background='white',
      image=photo,
      padding=5
  )
  image_label.pack()
  resultsScreen.pack()

## rows
def createProcsRowFrame(master, filepath: str):
  proc_bodies = {}
  frm_proc_body_row = tk.Frame(master, relief=tk.SUNKEN, bg='white', border=1,**paddings)
  lbl_proc_file_path = tk.Label(frm_proc_body_row, text=filepath, bg='white', **paddings)
  lbl_proc_status = tk.Label(frm_proc_body_row, text="ongoing", bg='white', **paddings)
  proc_bodies[filepath] = frm_proc_body_row
  lbl_proc_file_path.pack(side=tk.LEFT)
  lbl_proc_status.pack(side=tk.RIGHT)
  frm_proc_body_row.pack(fill=tk.X)

def createPathsRowFrame(master, filepath: str, bodies: dict):
  frm_body_row = tk.Frame(master, relief=tk.SUNKEN, bg='white', border=1,**paddings)
  bodies[filepath] = frm_body_row
  lbl_file_path = tk.Label(frm_body_row, text=filepath, bg='white', **paddings)
  btn_remove_body = tk.Button(frm_body_row, text='x', background='red', foreground='white', command= lambda: delete_body_row(filepath,bodies), **paddings)
  lbl_file_path.pack(side=tk.LEFT)
  btn_remove_body.pack(side=tk.RIGHT)
  frm_body_row.pack(fill=tk.X)

## handlers 
def open_file(entry):
  folderpath = askopenfilename(filetypes=[("All Files", "*.*")]) #askdirectory()
  if not folderpath:
      return
  entry.delete(0, tk.END)
  entry.insert(0, folderpath)
  
def delete_body_row(filepath: str, bodies: dict):
  bodies[filepath].pack_forget()
  bodies[filepath].destroy()
  del bodies[filepath]
  #proc_bodies[filepath].pack_forget()
  #proc_bodies[filepath].destroy()
  #del proc_bodies[filepath]

def add_body_row(bodyframe, bodies: dict):
  filepath = askdirectory() #askopenfilename(filetypes=[("All Files", "*.*")])  
  if not filepath:
      return
  createPathsRowFrame(bodyframe,filepath,bodies)