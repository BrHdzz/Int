import tkinter as tk
import db
import dashboard_page
import obj

def shResults(app):
    app.deletePage(app.mainFr)

    row = db.getProgress()

    mongo = db.printMongo()

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20, ipadx = 5, ipady = 5)

    img = app.gifs(frTitle, "images/pvz_troll.gif", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Retro... Progreso")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    frPro = app.frames(app.mainFr)
    frPro.columnconfigure(0, weight = 1)
    frPro.columnconfigure(1, weight = 1)
    frPro.configure(fg_color = "#1b1b1b", border_width = 1, border_color = "#ff00ea")
    frPro.pack(ipady = 5, ipadx = 5, fill = "x", padx = 90)
    
    a = app.labelTitle(frPro, "General")
    a.config(bg = "#1b1b1b", font = (obj.font.actual()["family"], 25, "bold"))
    a.grid(pady = 5, padx = 5, row = 0, column = 0, sticky = "ew")
    
    b = app.labelTxt(frPro, f"Experiencia: {row[0]} XP")
    b.config(bg = "#1b1b1b")
    b.grid(pady = 2, padx = 5, row = 1, column = 0)
    
    c = app.labelTxt(frPro, f"Precisión: {row[1]:.1f}%")
    c.config(bg = "#1b1b1b")
    c.grid(pady = 2, padx = 5, row = 2, column = 0)
    
    d = app.labelTitle(frPro, "Físico")
    d.config(bg = "#1b1b1b", font = (obj.font.actual()["family"], 25, "bold"))
    d.grid(pady = 5, padx = 5, row = 0, column = 1, sticky = "ew")
    
    e = app.labelTxt(frPro, f"Percisión inicial: {str(mongo[2][1]) + "%" if mongo is not None else "Sin resultados."}")
    e.config(bg = "#1b1b1b")
    e.grid(pady = 2, padx = 5, row = 1, column = 1)
    
    f = app.labelTxt(frPro, f"Precisión: {str(mongo[4][1]) + "%" if mongo is not None else "Sin resultados."}")
    f.config(bg = "#1b1b1b")
    f.grid(pady = 2, padx = 5, row = 2, column = 1)
    
    g = app.labelTxt(frPro, f"Tiempo promedio: {str(mongo[3][1]) + " segundos" if mongo is not None else "Sin resultados."}")
    g.config(bg = "#1b1b1b")
    g.grid(pady = 2, padx = 5, row = 3, column = 1)

    fr = app.frames(app.mainFr)
    fr.configure(fg_color = "#000")
    fr.pack(padx = 10, pady = 20)

    sc = app.scrollBars(fr)

    canva = app.canvas(fr, sc)

    sc.configure(command = canva.yview)
    sc.pack(side = tk.RIGHT, fill = tk.Y)

    canva.configure(yscrollcommand = sc.set, height = obj.root.winfo_height() - 550, width = obj.root.winfo_width() - 200)
    canva.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

    frC = app.framesTk(canva)
    frC.configure(bg = "#000")
    frC.pack(fill = "x")

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

    db.getRes(app, frC)
    
    back = app.buttons(app.mainFr, "Atrás")
    back.configure(command = lambda:dashboard_page.dasboardPage(app))
    back.pack(pady = 5, fill = "x", padx = 100)

    btns = [back]
    functions = [dashboard_page.dasboardPage]
    args = [(app,)]

    app.navegate(0, btns, functions, True, args)