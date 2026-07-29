import coments_page
import tkinter as tk
import db

def comentsPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.config(bg = "#000")
    frTitle.pack(pady = 20)

    img = app.images(frTitle, "images/how_bro.png", 100, 100)
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
    sc.pack(side = tk.RIGHT, fill = tk.Y)

    txt = app.texts(fr, sc)
    txt.config(height = 15)
    txt.pack(side = tk.TOP, fill = tk.X)
    
    back = app.buttons(app.mainFr, "Publicar")
    back.config(width = 70, command = lambda:db.coments(txt.get("1.0", "end-1c"), app))
    back.pack(pady = 5)
    
    back = app.buttons(app.mainFr, "Atrás")
    back.config(width = 70, command = lambda:coments_page.comentsPage(app))
    back.pack(pady = 5)