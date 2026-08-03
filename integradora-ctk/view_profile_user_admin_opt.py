import db
import admin_dashboard
import view_results_user_admin
import view_donation_user_admin
import view_coment_user_admin

def viewUsers_adminOpt(id, app):
    row = db.profileUsers_admin(id)

    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20)

    img = app.gifs(frTitle, "images/pvz_troll.gif", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Opciones")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)
    
    b1 = app.buttons(app.mainFr, "Strike")
    b1.configure(command = lambda:db.getAdv(id))
    b1.pack(pady = 5, padx = 100, fill = "x")
    
    b2 = app.buttons(app.mainFr, "Ver resultados")
    b2.configure(command = lambda:view_results_user_admin.shResults(app, id))
    b2.pack(pady = 5, padx = 100, fill = "x")
    
    b3 = app.buttons(app.mainFr, "Ver donaciones")
    b3.configure(command = lambda:view_donation_user_admin.shDonate(app, id))
    b3.pack(pady = 5, padx = 100, fill = "x")
    
    b4 = app.buttons(app.mainFr, "Ver comentarios")
    b4.configure(command = lambda:view_coment_user_admin.shComent(app, id))
    b4.pack(pady = 5, padx = 100, fill = "x")
    
    b5 = app.buttons(app.mainFr, "Eliminar cuenta")
    b5.configure(command = lambda:db.deleteUser(app, id))
    b5.pack(pady = 5, padx = 100, fill = "x")
    
    back = app.buttons(app.mainFr, "Atrás")
    back.configure(command = lambda:admin_dashboard.dasboardPage(app))
    back.pack(pady = 5, padx = 100, fill = "x")