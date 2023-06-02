from frontend.strings import strs
from backend import dicom_info
from backend import process_dicom
import tkinter as tk
import tkinter.messagebox as tkm
from tkinter import ttk
from tkinter.filedialog import askdirectory
from PIL import ImageTk, Image
import pandas as pd

##### global vars #####
## styles
paddings = {'padx': 5, 'pady': 5}
entry_font = {'font': ('Calibri', 12)}
basic_style = {'background': 'white', 'foreground': 'black', 'border': 1, 'font': ('Calibri', 12)} 
button_style = {'background': 'black', 'foreground': 'white', 'font': ('Calibri', 12)}
positive_style = {'background': 'white', 'foreground': 'green', 'font': ('Calibri', 12)}
negative_style = {'background': 'white', 'foreground': 'red', 'font': ('Calibri', 12)}
## data structures
dicoms = {}
results_imgs = {}


##### create app window #####
def root_window():
  app = tk.Tk()
  app.title(strs["home_title"])
  app.geometry('1200x900')
  app.configure(bg='white')
  return app


##### screens #####
## home screen
def home_screen(app):
  clear_window(app)
  home = tk.Frame(app)
  home.configure(bg='white')
  lbl_home = tk.Label(home, text=strs["home_title"], **basic_style)
  lbl_home.pack()
  lbl_description = tk.Label(home, text=strs["home_description"], padx=50, pady=150, **basic_style)
  lbl_description.pack()
  btn_home = tk.Button(home, text=strs["home_button"], width=6, height=3, command=lambda: file_path_selection_screen(app), **button_style, **paddings)
  btn_home.pack()
  #limpa lista de exames
  global dicoms
  dicoms = {}
  home.pack()
## path for TC files and path for saving results selection screen
def file_path_selection_screen(app):
  #clean
  clear_window(app)
  #directory for saving results
  txt_save_path = tk.StringVar()
  #dicom dictionaries
  global dicoms

  #create and configure frame grid
  path_selection_screen = tk.Frame(app)
  path_selection_screen.configure(bg='white')
  path_selection_screen.rowconfigure(0, weight=1)
  path_selection_screen.rowconfigure(1, minsize=400, weight=1)
  path_selection_screen.rowconfigure(2, weight=1)
  path_selection_screen.columnconfigure(0, minsize=900, weight=1)

  frm_header = tk.Frame(path_selection_screen, relief=tk.FLAT, bg='white', **paddings)

  lbl_explanation_row = tk.Label(frm_header, text=strs["path_select_title"], bg='white', **paddings, **entry_font)
  
  btn_add_body = tk.Button(frm_header, text=strs["path_select_add_button"], command=lambda:add_DICOM_row(frm_body, dicoms),  **button_style, **paddings)
  lbl_id = tk.Label(frm_header, text=strs["processing_tc_id_header"], width=10, background='white', foreground='black', name="ident", **paddings, **entry_font)
  lbl_path = tk.Label(frm_header, text=strs["processing_file_path_header"],width=60, background='white', foreground='black', **paddings, **entry_font)
  lbl_description = tk.Label(frm_header, text=strs["processing_description_header"], width=25, background='white', foreground='black', name="desc", **paddings, **entry_font)
  lbl_date = tk.Label(frm_header, text=strs["processing_date_header"], width=15, background='white', foreground='black', name="date", **paddings, **entry_font)
  
  frm_body = tk.Frame(path_selection_screen, bg='white')
  separator = ttk.Separator(frm_body, orient='horizontal')

  frm_footer = tk.Frame(path_selection_screen, relief=tk.RAISED, bg='white', **paddings)
  frm_save_path = tk.Frame(frm_footer, relief=tk.RAISED, bg='white')
  lbl_save_path = tk.Label(frm_save_path, text=strs["save_path_select_title"], **basic_style, **paddings)
  ent_save_path = tk.Entry(frm_save_path, textvariable=txt_save_path, width=120, **basic_style)
  btn_save_path = tk.Button(frm_save_path, text=strs["save_path_select_button"], height=1, command=lambda:select_save_path(ent_save_path), **button_style, **paddings)
  btn_run = tk.Button(frm_footer, text='Run', width=6, height=3, command=lambda: init_processing(app, txt_save_path.get(), dicoms), **button_style, **paddings)
  
  ## widgets placement
  lbl_explanation_row.pack(fill=tk.X)

  lbl_id.pack(side=tk.LEFT)
  lbl_path.pack(side=tk.LEFT)
  lbl_description.pack(side=tk.LEFT)
  lbl_date.pack(side=tk.LEFT)
  btn_add_body.pack(side=tk.RIGHT)

  separator.pack(fill=tk.X)
  
  frm_save_path.pack(fill=tk.X)
  lbl_save_path.pack(side=tk.LEFT)
  ent_save_path.pack(side=tk.LEFT)
  btn_save_path.pack(side=tk.RIGHT)
  btn_run.pack()

  frm_header.grid(row=0, column=0, sticky='ew')
  frm_body.grid(row=1, column=0, sticky='nsew')
  frm_footer.grid(row=2, column=0, sticky='ew')
  path_selection_screen.pack()
## processing status and files info screen
def processing_screen(app, save_path: str, bodies: dict):
  clear_window(app)
  #global processing_DICOM
  processing_screen = tk.Frame(app, bg='white')
  processing_screen.rowconfigure(0, weight=1)
  processing_screen.rowconfigure(1, minsize=400, weight=1)
  processing_screen.rowconfigure(2, weight=1)
  processing_screen.columnconfigure(0, minsize=900, weight=1)

  frm_proc_body = tk.Frame(processing_screen, bg='white')
  separator = ttk.Separator(frm_proc_body, orient='horizontal')

  frm_proc_header = tk.Frame(processing_screen, relief=tk.FLAT, bg='white')
  lbl_proc_id = tk.Label(frm_proc_header, text=strs["processing_tc_id_header"], width=10, name="ident", **basic_style, **paddings)
  lbl_proc_path = tk.Label(frm_proc_header, text=strs["processing_file_path_header"],width=60, background='white', foreground='black', **paddings, **entry_font)
  lbl_proc_description = tk.Label(frm_proc_header, text=strs["processing_description_header"], width=25, background='white', foreground='black', name="desc", **paddings, **entry_font)
  lbl_proc_date = tk.Label(frm_proc_header, text=strs["processing_date_header"], width=15, background='white', foreground='black', name="date", **paddings, **entry_font)
  lbl_proc_status = tk.Label(frm_proc_header, text=strs["processing_status_header"], width=10, background='white', foreground='black', **paddings, **entry_font)

  frm_proc_footer = tk.Frame(processing_screen, relief=tk.RAISED, bg='white')
  btn_proc_res = tk.Button(frm_proc_footer, text=strs["processing_final_button"], command=lambda: results_screen(app, save_path, bodies), width=15, height=3, background='black', foreground='white', **entry_font)

  separator.pack(fill=tk.X)

  for filepath in bodies.keys():
      create_file_processing_row(frm_proc_body, filepath, bodies)
  
  lbl_proc_id.pack(side=tk.LEFT)
  lbl_proc_path.pack(side=tk.LEFT)
  lbl_proc_description.pack(side=tk.LEFT)
  lbl_proc_date.pack(side=tk.LEFT)
  lbl_proc_status.pack(side=tk.RIGHT)

  btn_proc_res.pack()

  frm_proc_header.grid(row=0, column=0, sticky='ew')
  frm_proc_body.grid(row=1, column=0, sticky='nsew')
  frm_proc_footer.grid(row=2, column=0, sticky='ew')
  processing_screen.pack()

  #for filepath in bodies.keys():
  #  update_processing_status(filepath, "Falhou", bodies)

  #process_all_dicom_files(app, save_path, bodies)
## results image and data preview screen
def results_screen(app, save_path, bodies):
  clear_window(app)
  results_screen = tk.Frame(app, background='white')
  results_screen.configure(**paddings)
  results_screen.rowconfigure(0, weight=1)
  results_screen.rowconfigure(1, minsize=400, weight=1)
  results_screen.rowconfigure(2, weight=1)
  results_screen.columnconfigure(0, minsize=900, weight=1)

  frm_result_header = tk.Frame(results_screen, relief=tk.RAISED, bg='white')
  lbl_result = tk.Label(frm_result_header, text=strs["results_description"], background='white', **entry_font)
  lbl_result.pack()

  frm_result_body = tk.Frame(results_screen, bg='white', **paddings)

  metrics = pd.read_csv(os.path.join(save_path, 'metrics', 'metrics.csv'), index_col='Patient ID')
  
  for filepath in bodies.keys():
    if (bodies[filepath]['status'].get()==strs["processing_status_success"]):
      create_results_frame(frm_result_body, filepath, save_path, metrics)

  
  frm_result_footer = tk.Frame(results_screen, relief=tk.RAISED, bg='white')
  lbl_final = tk.Label(frm_result_footer, text=strs["results_save_path_description"]+save_path, background='white', **entry_font)
  btn_back = tk.Button(frm_result_footer, text=strs["results_button_back"], height=3, command=lambda: home_screen(app), background='black', foreground='white', **entry_font, **paddings)
  lbl_final.pack()
  btn_back.pack()

  frm_result_header.grid(row=0, column=0, sticky='ew')
  frm_result_body.grid(row=1, column=0, sticky='nsew')
  frm_result_footer.grid(row=2, column=0, sticky='ew')
  results_screen.pack()


##### sub frames ##### 
## result image and data frame
def create_results_frame(masterFrame, filepath, save_path, metrics):
  global results_imgs
  result_frm = tk.Frame(masterFrame, relief=tk.GROOVE, bg='white', border=1)
  
  results_imgs[filepath] = result_frm
  id_dicom=dicoms[filepath]['id']
  lbl_result = tk.Label(result_frm, text=id_dicom, background='white', **entry_font, **paddings)
  lbl_result.pack(side=tk.TOP)
  imagem = Image.open(os.path.join(save_path, id_dicom+'.png'))
  imagem = imagem.resize((384, 384), Image.ANTIALIAS)
  photo =  ImageTk.PhotoImage(imagem)
  image_label = tk.Label(
      result_frm,
      background='white',
      image=photo,
      **paddings
  )
  image_label.image = photo
  image_label.pack(fill=tk.X)

  #metrics recovering
  id_dicom=int(dicoms[filepath]['id'])
  musc=metrics.loc[id_dicom].loc['Muscle HU']
  musc2=metrics.loc[id_dicom].loc['Muscle CSA (cm^2)']
  imat=metrics.loc[id_dicom].loc['IMAT HU']
  imat2=metrics.loc[id_dicom].loc['IMAT CSA (cm^2)']
  sat=metrics.loc[id_dicom].loc['SAT HU']
  sat2=metrics.loc[id_dicom].loc['SAT CSA (cm^2)']
  vat=metrics.loc[id_dicom].loc['VAT HU']
  vat2=metrics.loc[id_dicom].loc['VAT CSA (cm^2)']

  # for metric in metrics:
  #   print(metrics[metric][id_dicom])

  #frame and grid for metrics display
  frm_result_data = tk.Frame(result_frm, background='white', **paddings)
  frm_result_data.rowconfigure(0, weight=1)
  frm_result_data.rowconfigure(1, weight=1)
  frm_result_data.rowconfigure(2, weight=1)

  cell_width=9
  HU = tk.Label(frm_result_data, text=strs["results_metric_unit_hu"], width=cell_width, **basic_style) 
  HU.grid(row=1, column=0)
  cm2 = tk.Label(frm_result_data, text=strs["results_metric_unit_cm2"], width=cell_width, **basic_style) 
  cm2.grid(row=2, column=0)

  header_musc = tk.Label(frm_result_data, text=strs["results_metric_header_muscle"], width=cell_width, **basic_style) 
  header_musc.grid(row=0, column=1)
  HU_musc = tk.Label(frm_result_data, text=round(musc), width=cell_width, **basic_style) 
  HU_musc.grid(row=1, column=1)
  cm2_musc = tk.Label(frm_result_data, text=round(musc2), width=cell_width, **basic_style) 
  cm2_musc.grid(row=2, column=1)

  header_imat = tk.Label(frm_result_data, text=strs["results_metric_header_imat"], width=cell_width, **basic_style) 
  header_imat.grid(row=0, column=2)
  HU_imat = tk.Label(frm_result_data, text=round(imat), width=cell_width, **basic_style) 
  HU_imat.grid(row=1, column=2)
  cm2_imat = tk.Label(frm_result_data, text=round(imat2), width=cell_width, **basic_style) 
  cm2_imat.grid(row=2, column=2)

  header_vat = tk.Label(frm_result_data, text=strs["results_metric_header_vat"], width=cell_width, **basic_style) 
  header_vat.grid(row=0, column=3)
  HU_vat = tk.Label(frm_result_data, text=round(vat), width=cell_width, **basic_style) 
  HU_vat.grid(row=1, column=3)
  cm2_vat = tk.Label(frm_result_data, text=round(vat2), width=cell_width, **basic_style) 
  cm2_vat.grid(row=2, column=3)

  header_sat = tk.Label(frm_result_data, text=strs["results_metric_header_sat"], width=cell_width, **basic_style) 
  header_sat.grid(row=0, column=4)
  HU_sat = tk.Label(frm_result_data, text=round(sat), width=cell_width, **basic_style) 
  HU_sat.grid(row=1, column=4)
  cm2_sat = tk.Label(frm_result_data, text=round(sat2), width=cell_width, **basic_style) 
  cm2_sat.grid(row=2, column=4)

  frm_result_data.pack(fill=tk.X)
  result_frm.pack()
## processing file row frame
def create_file_processing_row(master, filepath: str, bodies: dict):
  frm_proc_body_row = tk.Frame(master, relief=tk.FLAT, bg='white', border=1,**paddings)
  status_proc = tk.StringVar(frm_proc_body_row, strs["processing_status_ongoing"])
  
  bodies[filepath].update({'procframe': frm_proc_body_row, 'status': status_proc})

  lbl_proc_id = tk.Label(frm_proc_body_row, text=dicoms[filepath]['id'], width=10, bg='white', **paddings)
  lbl_proc_file_path = tk.Label(frm_proc_body_row, text=filepath, width=70, bg='white', **paddings)
  lbl_proc_description = tk.Label(frm_proc_body_row, text=dicoms[filepath]['description'], width=25, bg='white', **paddings)
  lbl_proc_date = tk.Label(frm_proc_body_row, text=dicoms[filepath]['date'].date(), width=15, bg='white', **paddings)
  lbl_proc_status = tk.Label(frm_proc_body_row, textvariable=status_proc, width=10, bg='white', name='statuslbl', **paddings)

  lbl_proc_id.pack(side=tk.LEFT)
  lbl_proc_file_path.pack(side=tk.LEFT)
  lbl_proc_status.pack(side=tk.RIGHT)
  lbl_proc_date.pack(side=tk.RIGHT)
  lbl_proc_description.pack(side=tk.LEFT)

  frm_proc_body_row.pack(fill=tk.X)
## selected files row frame
def create_file_selection_row(master, filepath: str, bodies: dict):
  frm_body_row = tk.Frame(master, relief=tk.FLAT, bg='white', border=1,**paddings)

  bodies[filepath] = {'pathframe': frm_body_row}
  bodies[filepath].update(dicom_info(filepath))

  lbl_file_path = tk.Label(frm_body_row, text=filepath, width=70, bg='white', **paddings)
  lbl_id = tk.Label(frm_body_row, text=bodies[filepath]['id'], width=10, bg='white', **paddings)
  lbl_description = tk.Label(frm_body_row, text=bodies[filepath]['description'], width=25, bg='white', **paddings)
  lbl_date = tk.Label(frm_body_row, text=bodies[filepath]['date'].date(), width=15, bg='white', **paddings)
  btn_remove_body = tk.Button(frm_body_row, text='❌', background='white', foreground='red', command= lambda: delete_DICOM_row(filepath,bodies), **paddings)
  #positions
  lbl_id.pack(side=tk.LEFT)
  lbl_file_path.pack(side=tk.LEFT)
  lbl_description.pack(side=tk.LEFT)
  lbl_date.pack(side=tk.LEFT)
  btn_remove_body.pack(side=tk.RIGHT)
  frm_body_row.pack(fill=tk.X)


#### handlers ##### 
##save results path 
def select_save_path(entry):
  folderpath = askdirectory()
  if not folderpath:
      return
  entry.delete(0, tk.END)
  entry.insert(0, folderpath)
##delete DICOM path
def delete_DICOM_row(filepath: str, bodies: dict):
  bodies[filepath]['pathframe'].pack_forget()
  bodies[filepath]['pathframe'].destroy()
  del bodies[filepath]
##add DICOM path
def add_DICOM_row(bodyframe, bodies: dict):
  filepath = askdirectory() #askopenfilename(filetypes=[("All Files", "*.*")])  
  if not filepath:
      return
  create_file_selection_row(bodyframe,filepath,bodies)
## update proccessing status
def update_processing_status(filepath, status, bodies):
  bodies[filepath]['status'].set(status)
## delete actual frame on app window
def clear_window(window):
  for widget in window.winfo_children():
    widget.destroy()
## delete actual frame on app window
def process_all_dicom_files(app, save_path, bodies):
  for filepath in bodies.keys():
    try:
      process_dicom(filepath, save_path)
      bodies[filepath]['status'].set(strs["processing_status_success"])
      bodies[filepath]['procframe'].pack()
      tkm.showinfo("Concluído")
    except Exception as err:
      bodies[filepath]['status'].set(strs["processing_status_failed"])
      bodies[filepath]['procframe'].pack()
      tkm.showinfo("Ouve um erro na identificação de vértebras.")
      print(err)
## construct processing screen then start processing
def init_processing(app, save_path, bodies):
  processing_screen(app, save_path, bodies)
  process_all_dicom_files(app, save_path, bodies)
  return