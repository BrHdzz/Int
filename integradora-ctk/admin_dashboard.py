import coments_admin
import view_users_admin
import passwords

def dasboardPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20, ipadx = 5, ipady = 5)

    img = app.images(frTitle, "images/modo_bienestar.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Panel de Admin")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    frButtonUsers = app.buttons(app.mainFr, "Usuarios")
    frButtonUsers.configure(command = lambda:view_users_admin.viewUsers_admin(app))
    frButtonUsers.pack(pady = 5, fill = "x", padx = 100)

    frButtonComents = app.buttons(app.mainFr, "Comentarios")
    frButtonComents.configure(command = lambda:coments_admin.comentsPage(app))
    frButtonComents.pack(pady = 5, fill = "x", padx = 100)

    frButtonComents = app.buttons(app.mainFr, "Contraseñas")
    frButtonComents.configure(command = lambda:passwords.psswd(app))
    frButtonComents.pack(pady = 5, fill = "x", padx = 100)