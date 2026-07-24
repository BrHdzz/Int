import tkinter as tk
import dashboard_page

def aboutUsPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.config(bg = "#000")
    frTitle.pack(pady = 20)

    logo = app.images(frTitle, "images/logo.png", 200, 200)
    logo.grid(padx = 10, row = 0, column = 0)

    imgN = app.images(frTitle, "images/nega_logo.png", 200, 300)
    imgN.grid(padx = 10, row = 0, column = 1)
    
    label = app.labelTitle(app.mainFr, "Nosotros")
    label.pack(pady = 10)

    txt = "Somos una pequeña empresa en desarrollo sin fines de lucro, que busca" \
    "\nayudar a las personas con discpacidad en las manos a que puedan recuperar" \
    "\nsu movilidad o no perder la poca que les queda a travez de ejercicios no tan terapeúticos" \
    "\na simple vista xdddd.\n\n" \
    "En NEGA nos comprometemos a demostrar que la tecnología, puede aportar bienestar real a personas\n" \
    "con discapacidad motriz. Buscamos que la rehabilitación no se sienta como una carga solitaria,\n" \
    "sino como un proceso acompañado, humano y ligero, poniendo nuestro conocimiento en ingeniería al\n" \
    "servicio de quienes más lo necesitan."

    labeltxt = app.labelTxt(app.mainFr, txt)
    labeltxt.pack(pady = 10)

    back = app.buttons(app.mainFr, "Atrás")
    back.config(width = 50, command = lambda:dashboard_page.dasboardPage(app))
    back.pack()