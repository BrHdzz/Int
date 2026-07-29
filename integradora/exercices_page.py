import tkinter as tk
import dashboard_page
import db
from games.catch_money import catch_money

i = 0

def ind(l, x, app):
    global i

    if i < 0:
        i = l
    elif i > l:
        i = 0
    else:
        i += x

    exercicesPage(app)

def exercicesPage(app):
    app.deletePage(app.mainFr)

    row = db.getActivity()

    l = len(row) - 2

    global i

    frTitle = app.frames(app.mainFr)
    frTitle.config(bg = "#000")
    frTitle.pack(expand = True)

    img = app.images(frTitle, "images/modo_bienestar.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.config(bg = "#000")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Ejercicios")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    frMenu = app.frames(app.mainFr)
    frMenu.config(bg = "#2b2b2b")
    frMenu.columnconfigure(1, weight = 1)
    frMenu.rowconfigure(0, weight = 1)
    frMenu.pack(expand = True, fill = "both", padx = 100)

    lf = tk.Button(frMenu, text = "◀", bg = "#2b2b2b", bd = 0, fg = "#38b6ff", activebackground = "#2b2b2b", command = lambda:ind(l, -1, app), font = ("Arial", 50), anchor = "e")
    lf.grid(column = 0, row = 0)

    frMenu2 = app.frames(frMenu)
    frMenu2.columnconfigure(0, weight = 1)
    frMenu2.rowconfigure(0, weight = 1)
    frMenu2.config(bg = "#000", highlightbackground = "#858489", highlightthickness = 2)
    frMenu2.grid(padx = 50, pady = 10, column = 1, row = 0, sticky = "nsew")
    
    t = app.labelTitle(frMenu2, row[i][1])
    t.config(fg = "#858489")
    t.grid(pady = 5, column = 0, row = 0)
    
    d = app.labelTxt(frMenu2, row[i][2])
    d.grid(pady = 5, column = 0, row = 1)
    
    x = app.labelTxt(frMenu2, f"XP: {row[i][0]}")
    x.grid(pady = 5, column = 0, row = 2)
    
    h = app.labelTxt(frMenu2, f"Descripción: {row[i][3]}")
    h.grid(pady = 5, column = 0, row = 3)

    ex = app.buttons(frMenu2, "Entrar")
    ex.config(command = lambda:execute_game(row[i][4], app, row[i][0], row[i][5]))
    ex.grid(pady = 5)

    rg = tk.Button(frMenu, text = "▶", bg = "#2b2b2b", bd = 0, fg = "#38b6ff", activebackground = "#2b2b2b", command = lambda:ind(l, 1, app), font = ("Arial", 50), anchor = "w")
    rg.grid(column = 2, row = 0)

    frButtonComents = app.buttons(app.mainFr, "Atrás")
    frButtonComents.config(command = lambda:dashboard_page.dasboardPage(app))
    frButtonComents.pack(pady = 5, expand = True, fill = "x", padx = 100)

def execute_game(path, app, xp, id):
    match path:
        case "catch_money":
            r = catch_money.CatchMoney(app, xp, id)
            r.start()