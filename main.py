from frontend.screens import home, root_window
#from backend import dicom_info
#from backend import process_dicom

if __name__ == '__main__':
    root_window = root_window()
    home(root_window)
    root_window.mainloop()