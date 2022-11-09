from tkinter import *

from lab1 import Lab_1_window


def main():
    window = Tk()
    window.title("Select")
    window.geometry("90x400")
    btn_lab1 = Button(window, text="1", command=Lab_1_window, height=1, width=5)
    btn_lab2 = Button(window, text="2", command=Lab_1_window, height=1, width=5)
    btn_lab3 = Button(window, text="3", command=Lab_1_window, height=1, width=5)
    btn_lab4 = Button(window, text="4", command=Lab_1_window, height=1, width=5)
    btn_lab5 = Button(window, text="5", command=Lab_1_window, height=1, width=5)

    btn_lab1.grid(row=1, column=0, padx=5, pady=5)
    btn_lab2.grid(row=2, column=0, padx=5, pady=5)
    btn_lab3.grid(row=3, column=0, padx=5, pady=5)
    btn_lab4.grid(row=4, column=0, padx=5, pady=5)
    btn_lab5.grid(row=5, column=0, padx=5, pady=5)
    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    main()