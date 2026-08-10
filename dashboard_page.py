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

    a = app.buttons(app.mainFr, "Ejercicios")
    a.configure(command = lambda:exercices_page.exercicesPage(app))
    a.pack(fill = "x", pady = 5, padx = 100)

    b = app.buttons(app.mainFr, "Perfil")
    b.configure(command = lambda:db.user_info(app))
    b.pack(fill = "x", pady = 5, padx = 100)

    c = app.buttons(app.mainFr, "Progreso")
    c.configure(command = lambda:results_user.shResults(app))
    c.pack(fill = "x", pady = 5, padx = 100)

    d = app.buttons(app.mainFr, "Donación")
    d.configure(command = lambda:donate_page.donatePage(app))
    d.pack(fill = "x", pady = 5, padx = 100)

    e = app.buttons(app.mainFr, "Acerca de")
    e.configure(command = lambda:aboutus_page.aboutUsPage(app))
    e.pack(fill = "x", pady = 5, padx = 100)

    f = app.buttons(app.mainFr, "Comentarios")
    f.configure(command = lambda:coments_page.comentsPage(app))
    f.pack(fill = "x", pady = 5, padx = 100)

    btns = [a, b, c, d, e, f]

    functions = [
        exercices_page.exercicesPage,
        db.user_info,
        results_user.shResults,
        donate_page.donatePage,
        aboutus_page.aboutUsPage,
        coments_page.comentsPage
    ]
    
    args = [(app,), (app,), (app,), (app,), (app,), (app,)]

    app.navegate(0, btns, functions, True, args)