import tkinter as tk
import db
import admin_dashboard

def comentsPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.config(bg = "#000")
    frTitle.pack(pady = 20)

    img = app.images(frTitle, "images/mario_dance.gif", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.config(bg = "#000")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Comentarios")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    fr = app.frames(app.mainFr)
    fr.config(bg = "#000")
    fr.pack(padx = 10, pady = 20)

    sc = app.scrollBars(fr)

    canva = app.canvas(fr, sc)

    sc.config(command = canva.yview)
    sc.pack(side = tk.RIGHT, fill = tk.Y)

    canva.config(yscrollcommand = sc.set, height = 400, width = 1200)
    canva.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

    frC = app.frames(canva)
    frC.config(bg = "#000")
    frC.pack()

    canva.create_window(0, 0, window = frC, anchor = "nw")

    frC.bind("<Configure>", lambda e:canva.configure(scrollregion = canva.bbox("all")))
    '''frC.bind("<Enter>", scroll)
    frC.bind("<Leave>", noscroll)

    def scroll(event):
        canva.bind_all("<MouseWheel>", mousewheel)

    def noscroll(event):
        canva.unbind_all("<MouseWheel>")

    def mousewheel(event):
        canva.yview_scroll(int(- 1 * (event.delta / 120)), "units")'''

    db.showComents_admin(frC, app)
    
    back = app.buttons(app.mainFr, "Atrás")
    back.config(width = 70, command = lambda:admin_dashboard.dasboardPage(app))
    back.pack(pady = 5)