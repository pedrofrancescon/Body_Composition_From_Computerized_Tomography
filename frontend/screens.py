import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
import tkinter.ttk as ttk
from PIL import ImageTk, Image


paddings = {'padx': 5, 'pady': 5}
entry_font = {'font': ('Helvetica', 12)}
description = "Selecione pastas contendo arquivos DICOM de exames tomográficos para determinação automatica da composição corporal dos pacientes"
DICOM = {}
processing_DICOM = {}
resultsImgs = {}


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
  clear_window(app)
  home = tk.Frame(app)
  home.configure(bg='white')
  lbl_home = tk.Label(home, text='Composição Corporal', background='white',**entry_font)
  lbl_home.pack()
  lbl_description = tk.Label(home, text=description, background='white', padx=50, pady=150, **entry_font)
  lbl_description.pack()
  btn_home = tk.Button(home, text='Iniciar', command=lambda: path_selection(app), background='black', foreground='white', **paddings)
  btn_home.pack()
  home.pack()

def path_selection(app):
  #clean
  clear_window(app)

  #directory for saving results
  txt_save_path = tk.StringVar()

  #dicom dictionaries
  global DICOM

  #create and configure frame grid
  pathSelectionScreen = tk.Frame(app)
  pathSelectionScreen.configure(bg='white')
  pathSelectionScreen.rowconfigure(0, weight=1)
  pathSelectionScreen.rowconfigure(1, minsize=400, weight=1)
  pathSelectionScreen.rowconfigure(2, weight=1)
  pathSelectionScreen.columnconfigure(0, minsize=600, weight=1)

  frm_body = tk.Frame(pathSelectionScreen, bg='white')
  explanation_row = tk.Frame(frm_body, relief=tk.SUNKEN, bg='white', **paddings)
  lbl_add_dicom = tk.Label(explanation_row, text="Adicione diretórios contendo exames de Tomografia", bg='white', **paddings, **entry_font)
  btn_add_body = tk.Button(explanation_row, text='Adicionar', background='black', foreground='white', command=lambda:add_body_row(frm_body, DICOM), **paddings, **entry_font)


  frm_header = tk.Frame(pathSelectionScreen, relief=tk.RAISED, bg='white')
  lbl_save_path = tk.Label(frm_header, text='Salvar em', background='white', foreground='black', **paddings, **entry_font)
  ent_save_path = tk.Entry(frm_header, textvariable=txt_save_path, width=80 , background='white', foreground='black')
  btn_save_path = tk.Button(frm_header, text='Escolher Local', height=1, command=lambda:open_file(ent_save_path), background='white', foreground='black', **paddings, **entry_font)
  
  frm_footer = tk.Frame(pathSelectionScreen, relief=tk.RAISED, bg='white')
  btn_run = tk.Button(frm_footer, text='Run', width=6, height=3, command=lambda: processing(app, txt_save_path, DICOM), background='black', foreground='white', **entry_font, **paddings)
  
  ## widgets placement
  explanation_row.pack(fill=tk.X)
  lbl_save_path.pack(side=tk.LEFT)
  ent_save_path.pack(side=tk.LEFT)
  btn_save_path.pack(side=tk.RIGHT)
  lbl_add_dicom.pack(side=tk.LEFT)
  btn_add_body.pack(side=tk.RIGHT)

  btn_run.pack()

  frm_header.grid(row=0, column=0, sticky='ew')
  frm_body.grid(row=1, column=0, sticky='nsew')
  frm_footer.grid(row=2, column=0, sticky='ew')
  pathSelectionScreen.pack()

def processing(app,txt_save_path: str,bodies: dict):
  clear_window(app)
  global processing_DICOM
  processing_screen = tk.Frame(app)
  frm_proc_body = tk.Frame(processing_screen, bg='white')

  frm_proc_header = tk.Frame(processing_screen, relief=tk.RAISED, bg='white')
  lbl_proc_save_path = tk.Label(frm_proc_header, text='Save path:', background='white', foreground='black', name="filha", **paddings, **entry_font)
  lbl_proc_saved_path = tk.Label(frm_proc_header, textvariable=txt_save_path, background='white', foreground='black', **paddings, **entry_font)
  lbl_info_body = tk.Label(frm_proc_header, text='Info', background='white', foreground='black', **paddings, **entry_font)
  lbl_proc_status = tk.Label(frm_proc_header, text='Status', background='white', foreground='black', **paddings, **entry_font)

  frm_proc_footer = tk.Frame(processing_screen, relief=tk.RAISED, bg='white')
  btn_proc_res = tk.Button(frm_proc_footer, text='Visualizar', command=lambda: results(app, txt_save_path), width=6, height=3, background='black', foreground='white', **entry_font, **paddings)

  for filepath in bodies.keys():
      createProcsRowFrame(frm_proc_body, filepath)
  
  lbl_proc_save_path.pack(side=tk.LEFT)
  lbl_proc_saved_path.pack(side=tk.LEFT, padx=5)
  lbl_info_body.pack(side=tk.LEFT)
  lbl_proc_status.pack(side=tk.RIGHT)

  btn_proc_res.pack()

  frm_proc_header.grid(row=0, column=0, sticky='ew')
  frm_proc_body.grid(row=1, column=0, sticky='nsew')
  frm_proc_footer.grid(row=2, column=0, sticky='ew')
  processing_screen.pack()

  #TODO: chamar aqui 'for' para processamento dos DICOM.

def results(app, save_path):
  clear_window(app)
  results_screen = tk.Frame(app, background='white')
  results_screen.configure(bg='white')
  results_screen.rowconfigure(0, weight=1)
  results_screen.rowconfigure(1, minsize=200, weight=1)
  results_screen.rowconfigure(2, weight=1)
  results_screen.columnconfigure(0, minsize=600, weight=1)

  frm_result_header = tk.Frame(results_screen, relief=tk.RAISED, bg='white')
  lbl_result = ttk.Label(frm_result_header, text='Resultados', background='white', **entry_font)
  lbl_result.pack()

  frm_result_body = tk.Frame(results_screen, bg='white')
  for filepath in processing_DICOM.keys():
    createResultImage(frm_result_body, filepath)
  
  frm_result_footer = tk.Frame(results_screen, relief=tk.RAISED, bg='white')
  lbl_final = ttk.Label(frm_result_footer, text=save_path.get(), background='white', **entry_font)
  btn_back = tk.Button(frm_result_footer, text='Início', width=6, height=3, command=lambda: home(app), background='black', foreground='white', **entry_font, **paddings)
  lbl_final.pack()
  btn_back.pack()

  frm_result_header.grid(row=0, column=0, sticky='ew')
  frm_result_body.grid(row=1, column=0, sticky='nsew')
  frm_result_footer.grid(row=2, column=0, sticky='ew')
  results_screen.pack()



def updateProcessingStatus(filepath, status):
  processing_DICOM[filepath]['status'].set(status)

def createResultImage(masterFrame, filepath):
  global resultsImgs
  result_img = tk.Frame(masterFrame, relief=tk.SUNKEN, bg='white', border=1,**paddings)
  resultsImgs[filepath] = result_img
  lbl_result = ttk.Label(result_img, text=filepath[-10:], background='white', **entry_font)
  lbl_result.pack()
  imagem = Image.open('D:/Documentos/TCC/Comp2Comp/figures/muscle_adipose_tissue_example.png')
  imagem = imagem.resize((192, 192), Image.ANTIALIAS)
  photo =  ImageTk.PhotoImage(imagem)
  image_label = ttk.Label(
      result_img,
      background='white',
      image=photo,
      padding=5
  )
  image_label.image = photo
  image_label.pack()
  result_img.pack()

## rows
def createProcsRowFrame(master, filepath: str):
  frm_proc_body_row = tk.Frame(master, relief=tk.SUNKEN, bg='white', border=1,**paddings)
  status_proc = tk.StringVar(frm_proc_body_row, "Ongoing")
  lbl_proc_file_path = tk.Label(frm_proc_body_row, text=filepath, bg='white', **paddings)
  lbl_proc_status = tk.Label(frm_proc_body_row, textvariable=status_proc, bg='white', name='status', **paddings)

  processing_DICOM[filepath] = {'framebody': frm_proc_body_row, 'status': status_proc}

  lbl_proc_file_path.pack(side=tk.LEFT)
  lbl_proc_status.pack(side=tk.RIGHT)
  frm_proc_body_row.pack(fill=tk.X)

def createPathsRowFrame(master, filepath: str, bodies: dict):
  frm_body_row = tk.Frame(master, relief=tk.SUNKEN, bg='white', border=1,**paddings)
  bodies[filepath] = frm_body_row
  lbl_file_path = tk.Label(frm_body_row, text=filepath, bg='white', **paddings)
  btn_remove_body = tk.Button(frm_body_row, text='X', background='white', foreground='red', command= lambda: delete_body_row(filepath,bodies), **paddings)
  lbl_file_path.pack(side=tk.LEFT)
  btn_remove_body.pack(side=tk.RIGHT)
  frm_body_row.pack(fill=tk.X)

## handlers 
def open_file(entry):
  folderpath = askdirectory()
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