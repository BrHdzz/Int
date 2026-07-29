import tkinter as tk
import donate_page
import aboutus_page
import coments_page
import results_user
import exercices_page
import db

def dasboardPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.config(bg = "#000")
    frTitle.pack(expand = True)

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
    frMenu.columnconfigure(0, weight = 1)
    frMenu.rowconfigure(0, weight = 1)
    frMenu.pack(expand = True, fill = "x", padx = 100)

    frButtonExercises = app.buttons(frMenu, "Ejercicios")
    frButtonExercises.config(command = lambda:exercices_page.exercicesPage(app))
    frButtonExercises.grid(row = 0, column = 0, sticky = "nsew", pady = 5)

    frButtonProfile = app.buttons(frMenu, "Perfil")
    frButtonProfile.config(command = lambda:db.user_info(app))
    frButtonProfile.grid(row = 1, column = 0, sticky = "nsew", pady = 5)

    frButtonProgress = app.buttons(frMenu, "Progreso")
    frButtonProgress.config(command = lambda:results_user.shResults(app))
    frButtonProgress.grid(row = 2, column = 0, sticky = "nsew", pady = 5)

    frButtonDonation = app.buttons(frMenu, "Donación")
    frButtonDonation.config(command = lambda:donate_page.donatePage(app))
    frButtonDonation.grid(row = 3, column = 0, sticky = "nsew", pady = 5)

    frButtonOptions = app.buttons(frMenu, "Acerca de")
    frButtonOptions.config(command = lambda:aboutus_page.aboutUsPage(app))
    frButtonOptions.grid(row = 4, column = 0, sticky = "nsew", pady = 5)

    frButtonComents = app.buttons(frMenu, "Comentarios")
    frButtonComents.config(command = lambda:coments_page.comentsPage(app))
    frButtonComents.grid(row = 5, column = 0, sticky = "nsew", pady = 5)