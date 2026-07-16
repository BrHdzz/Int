import tkinter as tk
from tkinter import messagebox
import dashboard_page
import pay_page

def validateAm(app, method, amount):
    try:
        x = float(amount)
        pay_page.payPage(app, method, x)
    except:
        return messagebox.showerror("Error", "Ingrese una cantidad válida.")

def donatePage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.config(bg = "#000")
    frTitle.pack(pady = 20)

    img = app.images(frTitle, "images/poor.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.config(bg = "#000")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Donación")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)
    
    label = app.labelTxt(app.mainFr, "Su contribución ayuda a otras personas día con día.")
    label.pack(pady = 20)

    fr = app.labelFrames(app.mainFr, "Cantidad (MXN):")
    fr.config(bg = "#000")
    fr.pack(ipady = 2, ipadx = 5, pady = 30)

    input = app.inputs(fr)
    input.pack(ipadx = 10, ipady = 5)

    xmr = app.buttons(app.mainFr, "Monero (XMR)")
    xmr.config(width = 50, command = lambda:validateAm(app, "XMR", input.get()))
    xmr.pack(pady = 5)

    btc = app.buttons(app.mainFr, "BitCoin (BTC)")
    btc.config(width = 50, command = lambda:validateAm(app, "BTC", input.get()))
    btc.pack(pady = 5)

    back = app.buttons(app.mainFr, "Atrás")
    back.config(width = 50, command = lambda:dashboard_page.dasboardPage(app))
    back.pack(pady = 5)