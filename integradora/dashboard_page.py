import tkinter as tk
import donate_page
import aboutus_page
import coments_page
import results_user
import db

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
    
    label = app.labelTitle(frTitle2, "dashboard()")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    frMenu = app.frames(app.mainFr)
    frMenu.config(bg = "#000")
    frMenu.pack(pady = 20)

    frButtonExercises = app.buttons(frMenu, "Ejercicios")
    frButtonExercises.config(width = 50)
    frButtonExercises.pack(pady = 5)

    frButtonProfile = app.buttons(frMenu, "Perfil")
    frButtonProfile.config(width = 50, command = lambda:db.user_info(app))
    frButtonProfile.pack(pady = 5)

    frButtonProgress = app.buttons(frMenu, "Progreso")
    frButtonProgress.config(width = 50, command = lambda:results_user.shResults(app))
    frButtonProgress.pack(pady = 5)

    frButtonDonation = app.buttons(frMenu, "Donación")
    frButtonDonation.config(width = 50, command = lambda:donate_page.donatePage(app))
    frButtonDonation.pack(pady = 5)

    frButtonOptions = app.buttons(frMenu, "Acerca de")
    frButtonOptions.config(width = 50, command = lambda:aboutus_page.aboutUsPage(app))
    frButtonOptions.pack(pady = 5)

    frButtonOptions = app.buttons(frMenu, "Comentarios")
    frButtonOptions.config(width = 50, command = lambda:coments_page.comentsPage(app))
    frButtonOptions.pack(pady = 5)