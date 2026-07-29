import tkinter as tk
import dashboard_page
import db
import alteruser_page

def profilePage(app, name, username, email, strike, id):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.config(bg = "#000")
    frTitle.pack(pady = 20)

    img = app.images(frTitle, "images/yoyo.jpg", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.config(bg = "#000")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Perfil")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 0, row = 1)

    fr1 = app.frames(app.mainFr)
    fr1.config(bg = "#2b2b2b")
    fr1.pack(pady = 5)

    btnN = app.buttons(fr1, "Modificar")
    btnN.config(width = 10, command = lambda:alteruser_page.alterUserPage(app, 1))
    btnN.grid(row = 0, column = 0)

    labelName = app.labelTxt(fr1, "Nombre:")
    labelName.config(width = 30, font = ("Inter", 20, "bold"), bg = "#2b2b2b")
    labelName.grid(padx = 10, row = 0, column = 1)

    labelName1 = app.labelTxt(fr1, name)
    labelName1.config(width = 30, bg = "#2b2b2b")
    labelName1.grid(padx = 10, row = 0, column = 2)

    fr2 = app.frames(app.mainFr)
    fr2.config(bg = "#2b2b2b")
    fr2.pack(pady = 5)

    btnU = app.buttons(fr2, "Modificar")
    btnU.config(width = 10, command = lambda:alteruser_page.alterUserPage(app, 2))
    btnU.grid(row = 0, column = 0)

    labelUname = app.labelTxt(fr2, "Nombre de Usuario:")
    labelUname.config(width = 30, font = ("Inter", 20, "bold"), bg = "#2b2b2b")
    labelUname.grid(padx = 10, row = 0, column = 1)

    labelUname1 = app.labelTxt(fr2, username)
    labelUname1.config(width = 30, bg = "#2b2b2b")
    labelUname1.grid(padx = 10, row = 0, column = 2)

    fr3 = app.frames(app.mainFr)
    fr3.config(width = 30, bg = "#2b2b2b")
    fr3.pack(pady = 5)

    btnM = app.buttons(fr3, "Modificar")
    btnM.config(width = 10, command = lambda:alteruser_page.alterUserPage(app, 3))
    btnM.grid(row = 0, column = 0)

    labelMail = app.labelTxt(fr3, "Correo Electrónico:")
    labelMail.config(width = 30, font = ("Inter", 20, "bold"), bg = "#2b2b2b")
    labelMail.grid(padx = 10, row = 0, column = 1)

    labelMail1 = app.labelTxt(fr3, email)
    labelMail1.config(width = 30, bg = "#2b2b2b")
    labelMail1.grid(padx = 10, row = 0, column = 2)

    fr4 = app.frames(app.mainFr)
    fr4.config(bg = "#2b2b2b")
    fr4.pack(pady = 5)

    btnP = app.buttons(fr4, "Modificar")
    btnP.config(width = 10, command = lambda:alteruser_page.alterUserPage(app, 4))
    btnP.grid(row = 0, column = 0)

    labelPass = app.labelTxt(fr4, "Contraseña:")
    labelPass.config(width = 30, font = ("Inter", 20, "bold"), bg = "#2b2b2b")
    labelPass.grid(padx = 10, row = 0, column = 1)

    labelPass1 = app.labelTxt(fr4, "********")
    labelPass1.config(width = 30, bg = "#2b2b2b")
    labelPass1.grid(padx = 10, row = 0, column = 2)

    fr5 = app.frames(app.mainFr)
    fr5.config(bg = "#2b2b2b")
    fr5.pack(pady = 5)

    btnS = app.buttons(fr5, "Modificar")
    btnS.config(width = 10, state = "disabled")
    btnS.grid(row = 0, column = 0)

    labelS = app.labelTxt(fr5, "Strikes:")
    labelS.config(width = 30, font = ("Inter", 20, "bold"), bg = "#2b2b2b")
    labelS.grid(padx = 10, row = 0, column = 1)

    labelS1 = app.labelTxt(fr5, strike)
    labelS1.config(width = 30, bg = "#2b2b2b")
    labelS1.grid(padx = 10, row = 0, column = 2)

    buttonFr = app.frames(app.mainFr)
    buttonFr.config(bg = "#000")
    buttonFr.pack(expand = True, pady = 70)

    singin = app.buttons(buttonFr, "Borrar Cuenta")
    singin.config(width = 20, command = lambda:db.deleteUser(app, id))
    singin.grid(row = 0, column = 0, padx = 20)

    singin = app.buttons(buttonFr, "Cerrar Sesión")
    singin.config(width = 20, command = lambda:db.logout(app))
    singin.grid(row = 0, column = 1, padx = 30)

    back = app.buttons(buttonFr, "Atrás")
    back.config(width = 20, command = lambda:dashboard_page.dasboardPage(app))
    back.grid(row = 0, column = 2, padx = 30)