from frontend.screens import home_screen, root_window

if __name__ == '__main__':
    root_window = root_window()
    home_screen(root_window)
    root_window.mainloop()