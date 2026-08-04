import tkinter as tk
import db
import admin_dashboard
import obj

def shDonate(app, user):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20, ipadx = 5, ipady = 5)

    img = app.images(frTitle, "images/no_aifon.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Donaciones")
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

    canva.configure(yscrollcommand = sc.set, height = 400, width = obj.root.winfo_width()- 200)
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

    db.getDonation_admin(app, user, frC)
    
    back = app.buttons(app.mainFr, "Atrás")
    back.configure(command = lambda:admin_dashboard.dasboardPage(app))
    back.pack(pady = 5, padx = 100, fill = "x")