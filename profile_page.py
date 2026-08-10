import tkinter as tk
import dashboard_page
import db
import alteruser_page

def profilePage(app, name, username, email, strike):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20)

    img = app.images(frTitle, "images/yoyo.jpg", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Perfil")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 0, row = 1)

    fr1 = app.frames(app.mainFr)
    fr1.configure(fg_color = "#2b2b2b")
    fr1.pack(pady = 5)

    btnN = app.buttons(fr1, "Modificar")
    btnN.configure(width = 10, command = lambda:alteruser_page.alterUserPage(app, 1))
    btnN.grid(row = 0, column = 0)

    labelName = app.labelTxt(fr1, "Nombre:")
    labelName.configure(width = 30, font = ("Inter", 20, "bold"), bg = "#2b2b2b")
    labelName.grid(padx = 10, row = 0, column = 1)

    labelName1 = app.labelTxt(fr1, name)
    labelName1.configure(width = 30, bg = "#2b2b2b")
    labelName1.grid(padx = 10, row = 0, column = 2)

    fr2 = app.frames(app.mainFr)
    fr2.configure(fg_color = "#2b2b2b")
    fr2.pack(pady = 5)

    btnU = app.buttons(fr2, "Modificar")
    btnU.configure(width = 10, command = lambda:alteruser_page.alterUserPage(app, 2))
    btnU.grid(row = 0, column = 0)

    labelUname = app.labelTxt(fr2, "Nombre de Usuario:")
    labelUname.configure(width = 30, font = ("Inter", 20, "bold"), bg = "#2b2b2b")
    labelUname.grid(padx = 10, row = 0, column = 1)

    labelUname1 = app.labelTxt(fr2, username)
    labelUname1.configure(width = 30, bg = "#2b2b2b")
    labelUname1.grid(padx = 10, row = 0, column = 2)

    fr3 = app.frames(app.mainFr)
    fr3.configure(fg_color = "#2b2b2b")
    fr3.pack(pady = 5)

    btnM = app.buttons(fr3, "Modificar")
    btnM.configure(width = 10, command = lambda:alteruser_page.alterUserPage(app, 3))
    btnM.grid(row = 0, column = 0)

    labelMail = app.labelTxt(fr3, "Correo Electrónico:")
    labelMail.configure(width = 30, font = ("Inter", 20, "bold"), bg = "#2b2b2b")
    labelMail.grid(padx = 10, row = 0, column = 1)

    labelMail1 = app.labelTxt(fr3, email)
    labelMail1.configure(width = 30, bg = "#2b2b2b")
    labelMail1.grid(padx = 10, row = 0, column = 2)

    fr4 = app.frames(app.mainFr)
    fr4.configure(fg_color = "#2b2b2b")
    fr4.pack(pady = 5)

    btnP = app.buttons(fr4, "Modificar")
    btnP.configure(width = 10, command = lambda:alteruser_page.alterUserPage(app, 4))
    btnP.grid(row = 0, column = 0)

    labelPass = app.labelTxt(fr4, "Contraseña:")
    labelPass.configure(width = 30, font = ("Inter", 20, "bold"), bg = "#2b2b2b")
    labelPass.grid(padx = 10, row = 0, column = 1)

    labelPass1 = app.labelTxt(fr4, "********")
    labelPass1.configure(width = 30, bg = "#2b2b2b")
    labelPass1.grid(padx = 10, row = 0, column = 2)

    fr5 = app.frames(app.mainFr)
    fr5.configure(fg_color = "#2b2b2b")
    fr5.pack(pady = 5)

    btnS = app.buttons(fr5, "Modificar")
    btnS.configure(width = 10, state = "disabled")
    btnS.grid(row = 0, column = 0)

    labelS = app.labelTxt(fr5, "Strikes:")
    labelS.configure(width = 30, font = ("Inter", 20, "bold"), bg = "#2b2b2b")
    labelS.grid(padx = 10, row = 0, column = 1)

    labelS1 = app.labelTxt(fr5, strike)
    labelS1.configure(width = 30, bg = "#2b2b2b")
    labelS1.grid(padx = 10, row = 0, column = 2)

    buttonFr = app.frames(app.mainFr)
    buttonFr.configure(fg_color = "#000")
    buttonFr.columnconfigure(0, weight = 1)
    buttonFr.columnconfigure(1, weight = 1)
    buttonFr.columnconfigure(2, weight = 1)
    buttonFr.pack(expand = True, pady = 10, padx = 100, fill = "x")

    singin = app.buttons(buttonFr, "Borrar Cuenta")
    singin.configure(command = lambda:db.deleteUser(app, username))
    singin.grid(row = 0, column = 0, padx = 20, sticky = "ew")

    r = app.buttons(buttonFr, "Cerrar Sesión")
    r.configure(command = lambda:db.logout(app))
    r.grid(row = 0, column = 1, padx = 20, sticky = "ew")

    back = app.buttons(buttonFr, "Atrás")
    back.configure(command = lambda:dashboard_page.dasboardPage(app))
    back.grid(row = 0, column = 2, padx = 20, sticky = "ew")

    btns = [singin, r, back]
    functions = [db.deleteUser, db.logout, dashboard_page.dasboardPage]
    args = [(app, username), (app,), (app,)]

    app.navegate(0, btns, functions, True, args)