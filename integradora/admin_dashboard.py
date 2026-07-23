import coments_admin
import view_users_admin

def dasboardPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.config(bg = "#000")
    frTitle.pack(pady = 20)

    img = app.images(frTitle, "images/modo_bienestar.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.config(bg = "#000")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "eladmintienezida")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    frMenu = app.frames(app.mainFr)
    frMenu.config(bg = "#000")
    frMenu.pack(pady = 20)

    frButtonUsers = app.buttons(frMenu, "Usuarios")
    frButtonUsers.config(width = 50, command = lambda:view_users_admin.viewUsers_admin(app))
    frButtonUsers.pack(pady = 5)

    frButtonComents = app.buttons(frMenu, "Comentarios")
    frButtonComents.config(width = 50, command = lambda:coments_admin.comentsPage(app))
    frButtonComents.pack(pady = 5)