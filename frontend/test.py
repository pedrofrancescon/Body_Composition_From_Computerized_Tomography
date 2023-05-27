import tkinter as tk
from tkinter.messagebox import showinfo
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory, askopenfilename

paddings = {'padx': 5, 'pady': 5}
entry_font = {'font': ('Helvetica', 12)}
description = "Selecione pastas contendo arquivos DICOM de exames tomográficos para determinação automatica da composição corporal dos pacientes"
bodies = {}
proc_bodies = {}

#### Navigation
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
txt_save_path = tk.StringVar()
####################

#### frame tela boas vindas
def createHomeFrame():
  home = tk.Frame(app)
  home.configure(bg='white')
  lbl_home = ttk.Label(home, text='Composição Corporal', background='white',**entry_font)
  lbl_home.pack()
  lbl_description = ttk.Label(home, text=description, background='white', padding={'padx': 5, 'pady': 5}, **entry_font)
  lbl_description.pack()
  btn_home = ttk.Button(home, text='Iniciar', command=lambda: show_page(1), padding={'padx': 5, 'pady': 5})
  btn_home.pack()
  return home
########################

def createPathsRowFrame(master, filepath):
  frm_body_row = tk.Frame(master, relief=tk.SUNKEN, bg='white', border=1,**paddings)
  lbl_file_path = tk.Label(frm_body_row, text=filepath, bg='white', **paddings)
  btn_remove_body = tk.Button(frm_body_row, text='x', background='red', foreground='white', command= lambda: delete_body_row(filepath), **paddings)
  bodies[filepath] = frm_body_row
  lbl_file_path.pack(side=tk.LEFT)
  btn_remove_body.pack(side=tk.RIGHT)
  frm_body_row.pack(fill=tk.X)

def createProcsRowFrame(master, filepath):
  #add to processing frame
  frm_proc_body_row = tk.Frame(master, relief=tk.SUNKEN, bg='white', border=1,**paddings)
  lbl_proc_file_path = tk.Label(frm_proc_body_row,frm_proc_body_row, text=filepath, bg='white', **paddings)
  lbl_proc_status = tk.Label(frm_proc_body_row, text="ongoing", bg='white', **paddings)
  proc_bodies[filepath] = frm_proc_body_row
  lbl_proc_file_path.pack(side=tk.LEFT)
  lbl_proc_status.pack(side=tk.RIGHT)
  frm_proc_body_row.pack(fill=tk.X)

## handlers 
def open_file(entry):
  folderpath = askopenfilename(filetypes=[("All Files", "*.*")]) #askdirectory()
  if not folderpath:
      return
  entry.delete(0, tk.END)
  entry.insert(0, folderpath)
  
def delete_body_row(filepath):
  bodies[filepath].pack_forget()
  bodies[filepath].destroy()
  del bodies[filepath]
  #proc_bodies[filepath].pack_forget()
  #proc_bodies[filepath].destroy()
  #del proc_bodies[filepath]

def add_body_row(bodyframe):
  filepath = askdirectory() #askopenfilename(filetypes=[("All Files", "*.*")])  
  print(filepath)
  if not filepath:
      return
  #add to pathselection frame
  createPathsRowFrame(bodyframe,filepath)

#### frame escolha de diretorios
def createPathsSelectionFrame():
  pathSelectionScreen = tk.Frame(app)
  pathSelectionScreen.configure(bg='white')
  pathSelectionScreen.rowconfigure(0, weight=1)
  pathSelectionScreen.rowconfigure(1, minsize=400, weight=1)
  pathSelectionScreen.rowconfigure(2, weight=1)
  pathSelectionScreen.columnconfigure(0, minsize=600, weight=1)

  
  ## widgets creation
  frm_body = tk.Frame(pathSelectionScreen, bg='white')
  frm_header = tk.Frame(pathSelectionScreen, relief=tk.RAISED, bg='white')
  lbl_save_path = tk.Label(frm_header, text='Save path:', background='white', foreground='black', **paddings, **entry_font)
  ent_save_path = tk.Entry(frm_header, textvariable=txt_save_path, width=50, background='white', foreground='black', **entry_font)
  btn_save_path = tk.Button(frm_header, text='Open', height=1, command=lambda:open_file(ent_save_path), background='white', foreground='black', **paddings, **entry_font)
  btn_add_body = tk.Button(frm_header, text='+', background='green', foreground='white', command=lambda:add_body_row(frm_body), **paddings, **entry_font)

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

  return pathSelectionScreen
  ######################

#### frame processamento
def createProcessingFrame():
  processingScreen = tk.Frame(app)
  frm_proc_body = tk.Frame(processingScreen, bg='white')

  frm_proc_header = tk.Frame(processingScreen, relief=tk.RAISED, bg='white')
  lbl_proc_save_path = tk.Label(frm_proc_header, text='Save path:', background='white', foreground='black', **paddings, **entry_font)
  lbl_proc_saved_path = tk.Label(frm_proc_header, textvariable=txt_save_path, background='white', foreground='black', **paddings, **entry_font)
  lbl_info_body = tk.Label(frm_proc_header, text='Info', background='white', foreground='black', **paddings, **entry_font)
  lbl_proc_status = tk.Label(frm_proc_header, text='Status', background='white', foreground='black', **paddings, **entry_font)

  frm_proc_footer = tk.Frame(processingScreen, relief=tk.RAISED, bg='white')
  btn_proc_res = tk.Button(frm_proc_footer, text='Visualizar', width=6, height=3, command=lambda: show_page(3), background='green', foreground='white', **entry_font, **paddings)

  print(f'createProcFram {bodies}')
  for filep in bodies:
      print(filep)
      createProcsRowFrame(frm_proc_body, filep)

  lbl_proc_save_path.pack(side=tk.LEFT)
  lbl_proc_saved_path.pack(side=tk.LEFT, padx=5)
  lbl_info_body.pack(side=tk.LEFT)
  lbl_proc_status.pack(side=tk.RIGHT)

  btn_proc_res.pack()

  frm_proc_header.grid(row=0, column=0, sticky='ew')
  frm_proc_body.grid(row=1, column=0, sticky='nsew')
  frm_proc_footer.grid(row=2, column=0, sticky='ew')
  return processingScreen
####################

#### frame resultados
def createResultFrame():
  
  return resultsScreen
####################
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
#creating frames
home = createHomeFrame()
pathSelectionScreen = createPathsSelectionFrame()
processingScreen = createProcessingFrame()
#resultsScreen = createResultFrame()

#### Dicionário para mapear as páginas
pages = {0: home, 1: pathSelectionScreen, 2: processingScreen, 3: resultsScreen}
current_page = home
current_page.pack()
####################

app.mainloop()