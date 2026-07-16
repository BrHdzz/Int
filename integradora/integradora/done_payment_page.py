import tkinter as tk
import dashboard_page
import db
import os

def init(bar, app, l, method, amount):
    bar["value"] = 0

    charge(bar, app, l, method, amount)    

def charge(bar, app, l, method, amount):
    if bar["value"] < 10:
        l.config(text = "Generando dirección de recepción...")
    elif bar["value"] < 20:
        l.config(text = "Validate IP Sussesful...")
    elif bar["value"] < 30:
        l.config(text = "Search dependences...")
    elif bar["value"] < 45:
        l.config(text = "Node-001 requesting...")
    elif bar["value"] < 60:
        l.config(text = "Esperando confirmación de bloque...")
    elif bar["value"] < 70:
        l.config(text = "Node-002 requesting...")
    elif bar["value"] < 80:
        l.config(text = "Esperando confirmación de bloque...")
    elif bar["value"] < 100:
        l.config(text = "Conectando Servidores...")
    else:
        donate = db.donate(method, amount)
        
        l.config(text = donate)
    
    if bar["value"] < 100:
        bar["value"] += 1
        app.mainFr.after(100, charge, bar, app, l, method, amount)
    else:
        back = app.buttons(app.mainFr, "Terminar")
        back.config(width = 70, command = lambda:dashboard_page.dasboardPage(app))
        back.pack(pady = 5)


def donePayPage(app, method, amount):
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
    
    label = app.labelTxt(app.mainFr, "Su contribución ayuda a otras personas día con día.\n\nNo cierre esta ventana.")
    label.pack(pady = 20)
    
    label1 = app.labelTxt(app.mainFr, "")
    label1.pack(pady = 20)

    progBar = app.progressBars(app.mainFr)
    progBar.pack(pady = 10)

    init(progBar, app, label1, method, amount)