import tkinter as tk
import db
import dashboard_page

def alterUserPage(app, attribute):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20, ipadx = 5, ipady = 5)

    img = app.images(frTitle, "images/yoyo.jpg", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Modificar Información")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 0, row = 1, sticky = tk.E)

    fr = app.labelFrames(app.mainFr, "")
    fr.pack(ipady = 2, ipadx = 5, padx = 100, pady = 30)

    input = app.inputs(fr)

    if attribute == 1:
        fr.configure(bg = "#000", text = "Nombre:")
    elif attribute == 2:
        fr.configure(bg = "#000", text = "Nombre de usuario (máximo 15 caracteres):")
        fr.pack(ipady = 2, ipadx = 5, padx = 100, pady = 30)
    elif attribute == 3:
        fr.configure(bg = "#000", text = "Correo Electrónico:")
        fr.pack(ipady = 2, ipadx = 5, padx = 100, pady = 30)
    elif attribute == 4:
        fr.configure(bg = "#000", text = "Contraseña (8 a 20 caracteres):")
        fr.pack(ipady = 2, ipadx = 5, padx = 100, pady = 30)

        input.configure(show = "*")

    input.bind("<F12>", lambda e: db.alter_user_info(app, input.get(), attribute))
    input.pack(ipadx = 10, ipady = 5)

    singin = app.buttons(app.mainFr, "Guardar <F12>")
    singin.configure(command = lambda:db.alter_user_info(app, input.get(), attribute))
    singin.pack(pady = 5, padx = 100, fill = "x")

    back = app.buttons(app.mainFr, "Atrás")
    back.configure(command = lambda:dashboard_page.dasboardPage(app))
    back.pack(pady = 5, padx = 100, fill = "x")

    btns = [singin, back]
    functions = [print, dashboard_page.dasboardPage]
    args = [("alter pressed",), (app,)]

    app.navegate(0, btns, functions, True, args)