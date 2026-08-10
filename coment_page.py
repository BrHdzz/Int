import coments_page
import tkinter as tk
import db

def comentsPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20, ipadx = 5, ipady = 5)

    img = app.images(frTitle, "images/how_bro.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Comentarios")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    fr = app.frames(app.mainFr)
    fr.configure(fg_color = "#000")
    fr.pack(padx = 100, pady = 20, fill = "x", expand = True)

    sc = app.scrollBars(fr)
    sc.pack(side = tk.RIGHT, fill = tk.Y)

    args = [("", app), (app,)]

    txt = app.texts(fr, sc)
    txt.bind("<KeyRelease>", lambda e: print(args[0][0] + txt.get("1.0", "end-1c")))
    txt.configure(height = 15)
    txt.pack(side = tk.TOP, fill = tk.X)
    
    send = app.buttons(app.mainFr, "Publicar")
    send.configure(command = lambda:db.coments(txt.get("1.0", "end-1c"), app))
    send.pack(pady = 5, padx = 100, fill = "x")
    
    back = app.buttons(app.mainFr, "Atrás")
    back.configure(command = lambda:coments_page.comentsPage(app))
    back.pack(pady = 5, padx = 100, fill = "x")

    btns = [send, back]
    functions = [db.coments, coments_page.comentsPage]

    app.navegate(0, btns, functions, True, args)

def getTxt(txt):
    return txt.get("1.0", "end-1c")