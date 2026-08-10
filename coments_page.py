import dashboard_page
import coment_page
import tkinter as tk
import db
import obj

def comentsPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20, ipady = 5, ipadx = 5)

    img = app.gifs(frTitle, "images/nerding_speech_bubble.gif", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Comentarios")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)
    
    coment = app.buttons(app.mainFr, "Dejar un Comentario")
    coment.configure(command = lambda:coment_page.comentsPage(app))
    coment.pack(pady = 5, fill = "x", padx = 100)
    
    back = app.buttons(app.mainFr, "Atrás")
    back.configure(command = lambda:dashboard_page.dasboardPage(app))
    back.pack(pady = 5, fill = "x", padx = 100)

    fr = app.frames(app.mainFr)
    fr.configure(fg_color = "#000")
    fr.pack(padx = 10, pady = 20)

    sc = app.scrollBars(fr)

    canva = app.canvas(fr, sc)

    sc.configure(command = canva.yview)
    sc.pack(side = tk.RIGHT, fill = tk.Y)

    canva.configure(yscrollcommand = sc.set, height = 350, width = obj.root.winfo_width() - 200)
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

    db.showComents(frC)

    btns = [coment, back]
    functions = [coment_page.comentsPage, dashboard_page.dasboardPage]
    args = [(app,), (app,)]

    app.navegate(0, btns, functions, True, args)