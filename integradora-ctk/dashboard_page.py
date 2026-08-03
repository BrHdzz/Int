import donate_page
import aboutus_page
import coments_page
import results_user
import exercices_page
import db

def dasboardPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(ipady = 5, ipadx = 5, pady = 40)

    img = app.images(frTitle, "images/modo_bienestar.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "dashboard()")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    frButtonExercises = app.buttons(app.mainFr, "Ejercicios")
    frButtonExercises.configure(command = lambda:exercices_page.exercicesPage(app))
    frButtonExercises.pack(fill = "x", pady = 5, padx = 100)

    frButtonProfile = app.buttons(app.mainFr, "Perfil")
    frButtonProfile.configure(command = lambda:db.user_info(app))
    frButtonProfile.pack(fill = "x", pady = 5, padx = 100)

    frButtonProgress = app.buttons(app.mainFr, "Progreso")
    frButtonProgress.configure(command = lambda:results_user.shResults(app))
    frButtonProgress.pack(fill = "x", pady = 5, padx = 100)

    frButtonDonation = app.buttons(app.mainFr, "Donación")
    frButtonDonation.configure(command = lambda:donate_page.donatePage(app))
    frButtonDonation.pack(fill = "x", pady = 5, padx = 100)

    frButtonOptions = app.buttons(app.mainFr, "Acerca de")
    frButtonOptions.configure(command = lambda:aboutus_page.aboutUsPage(app))
    frButtonOptions.pack(fill = "x", pady = 5, padx = 100)

    frButtonComents = app.buttons(app.mainFr, "Comentarios")
    frButtonComents.configure(command = lambda:coments_page.comentsPage(app))
    frButtonComents.pack(fill = "x", pady = 5, padx = 100)