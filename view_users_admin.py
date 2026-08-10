import tkinter as tk
import db
import admin_dashboard
import obj

def viewUsers_admin(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20, ipadx = 5, ipady = 5)

    img = app.gifs(frTitle, "images/monkeys.gif", 100, 150)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Usuarios")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    fr = app.frames(app.mainFr)
    fr.configure(fg_color = "#000")
    fr.pack(padx = 10, pady = 20)

    sc = app.scrollBars(fr)

    canva = app.canvas(fr, sc)

    sc.configure(command = canva.yview)
    sc.pack(side = tk.RIGHT, fill = tk.Y)

    canva.configure(yscrollcommand = sc.set, height = 400, width = 1200)
    canva.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

    frC = app.framesTk(canva)
    frC.configure(bg = "#000")
    frC.pack()

    canva.create_window(0, 0, window = frC, anchor = "nw")

    def scroll(event):
        canva.bind_all("<MouseWheel>", mousewheel)
    
    def noscroll(event):
        canva.unbind_all("<MouseWheel>")
    
    def mousewheel(event):
        canva.yview_scroll(int(- 1 * (event.delta / 120)), "units")
    
    frC.bind("<Configure>", lambda e:canva.config(scrollregion = canva.bbox("all")))
    canva.bind("<Enter>", scroll)
    canva.bind("<Leave>", noscroll)

    db.showUsers_admin(frC, app)
    
    back = app.buttons(app.mainFr, "Atrás")
    back.configure(command = lambda:admin_dashboard.dasboardPage(app))
    back.pack(pady = 5, fill = "x", padx = 100)

    btns = [back]
    functions = [admin_dashboard.dasboardPage]
    args = [(app,)]

    app.navegate(0, btns, functions, True, args)