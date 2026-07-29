import db
import admin_dashboard
import view_profile_user_admin_opt

def viewUsers_admin(id, app):
    row = db.profileUsers_admin(id)

    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.config(bg = "#000")
    frTitle.pack(pady = 20)

    img = app.images(frTitle, "images/whos_this.png", 100, 150)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.config(bg = "#000")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Who's this?")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)
    
    id = app.labelTxt(app.mainFr, f"ID: {row[0]}")
    id.pack(pady = 5)
    
    name = app.labelTxt(app.mainFr, f"Nombre: {row[1]}")
    name.pack(pady = 5)
    
    username = app.labelTxt(app.mainFr, f"Usuario: {row[2]}")
    username.pack(pady = 5)
    
    date = app.labelTxt(app.mainFr, f"Fecha de Creación: {row[3]}")
    date.pack(pady = 5)
    
    email = app.labelTxt(app.mainFr, f"Email: {row[4]}")
    email.pack(pady = 5)
    
    tick = app.labelTxt(app.mainFr, f"Strikes: {row[5]}")
    tick.pack(pady = 5)
    
    xp = app.labelTxt(app.mainFr, f"Experiencia: {row[6]} XP")
    xp.pack(pady = 5)
    
    accurate = app.labelTxt(app.mainFr, f"Presisión: {row[7]}%")
    accurate.pack(pady = 5)
    
    viewR = app.buttons(app.mainFr, "Opciones")
    viewR.config(width = 70, command = lambda:view_profile_user_admin_opt.viewUsers_adminOpt(row[0], app))
    viewR.pack(pady = 5)
    
    back = app.buttons(app.mainFr, "Atrás")
    back.config(width = 70, command = lambda:admin_dashboard.dasboardPage(app))
    back.pack(pady = 5)