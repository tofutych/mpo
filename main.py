from tkinter import *

from labs import (Lab_1_window, Lab_2_window, Lab_3_window, Lab_4_window,
                  Lab_5_window, Lab_6_window, Lab_7_window, Lab_8_window)


def main():
    window = Tk()
    window.resizable(False, False)
    window.title("Select")
    window.geometry("90x400")
    btn_lab1 = Button(window, text="1", command=Lab_1_window,
                      height=1, width=5)
    btn_lab2 = Button(window, text="2", command=Lab_2_window,
                      height=1, width=5)
    btn_lab3 = Button(window, text="3", command=Lab_3_window,
                      height=1, width=5)
    btn_lab4 = Button(window, text="4", command=Lab_4_window,
                      height=1, width=5)
    btn_lab5 = Button(window, text="5", command=Lab_5_window,
                      height=1, width=5)
    btn_lab6 = Button(window, text="6", command=Lab_6_window,
                      height=1, width=5)
    btn_lab7 = Button(window, text="7", command=Lab_7_window,
                      height=1, width=5)
    btn_lab8 = Button(window, text="8", command=Lab_8_window,
                      height=1, width=5)
    exit_button = Button(window, text="Exit", command=window.quit)

    btn_lab1.grid(row=1, column=0, padx=5, pady=5)
    btn_lab2.grid(row=2, column=0, padx=5, pady=5)
    btn_lab3.grid(row=3, column=0, padx=5, pady=5)
    btn_lab4.grid(row=4, column=0, padx=5, pady=5)
    btn_lab5.grid(row=5, column=0, padx=5, pady=5)
    btn_lab6.grid(row=6, column=0, padx=5, pady=5)
    btn_lab7.grid(row=7, column=0, padx=5, pady=5)
    btn_lab8.grid(row=8, column=0, padx=5, pady=5)
    exit_button.grid(row=10, column=0, padx=10, pady=5)
    exit_button.place(x=15, y=370)
    window.mainloop()


if __name__ == "__main__":
    main()
