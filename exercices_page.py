import tkinter as tk
from tkinter import messagebox
import dashboard_page
import db
from games.catch_money import catch_money
from games.whack_mole import whack_mole
from games.fnf import fnf_game
import obj
from games.no_game import no_game

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
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(expand = True, ipadx = 5, ipady = 5)

    img = app.gifs(frTitle, "images/jobnt.gif", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Ejercicios")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    frMenu = app.frames(app.mainFr)
    frMenu.configure(fg_color = "#2b2b2b")
    frMenu.columnconfigure(1, weight = 1)
    frMenu.rowconfigure(0, weight = 1)
    frMenu.pack(expand = True, fill = "both", padx = 100)

    lf = tk.Button(frMenu, text = "◀", bg = "#2b2b2b", bd = 0, fg = "#38b6ff", activebackground = "#2b2b2b", command = lambda:ind(l, -1, app), font = ("Arial", 50), anchor = "e")
    lf.grid(column = 0, row = 0)

    frMenu2 = app.frames(frMenu)
    frMenu2.columnconfigure(0, weight = 1)
    frMenu2.rowconfigure(0, weight = 1)
    frMenu2.configure(fg_color = "#000", border_width = 2, border_color = "#858489")
    frMenu2.grid(padx = 50, pady = 10, column = 1, row = 0, sticky = "nsew")
    
    t = app.labelTitle(frMenu2, row[i][1])
    t.configure(fg = "#858489")
    t.grid(pady = 5, column = 0, row = 0)
    
    d = app.labelTxt(frMenu2, row[i][2])
    d.config(wraplength = obj.root.winfo_width() - 500)
    d.grid(pady = 5, column = 0, row = 1)
    
    x = app.labelTxt(frMenu2, f"XP: {row[i][0]}")
    x.grid(pady = 5, column = 0, row = 2)
    
    h = app.labelTxt(frMenu2, f"Dificultad: {'Fácil' if row[i][3] == 1 else 'Normal' if row[i][3] == 2 else 'Difícil'}")
    h.grid(pady = 5, column = 0, row = 3)

    ex = app.buttons(frMenu2, "Entrar")
    ex.configure(command = lambda:execute_game(row[i][4], app, row[i][0], row[i][5]))
    ex.grid(pady = 5, ipadx = 20)

    rg = tk.Button(frMenu, text = "▶", bg = "#2b2b2b", bd = 0, fg = "#38b6ff", activebackground = "#2b2b2b", command = lambda:ind(l, 1, app), font = ("Arial", 50), anchor = "w")
    rg.grid(column = 2, row = 0)

    back = app.buttons(app.mainFr, "Atrás")
    back.configure(command = lambda:dashboard_page.dasboardPage(app))
    back.pack(pady = 5, expand = True, fill = "x", padx = 100)

    btns = [ex, back]
    functions = [execute_game, dashboard_page.dasboardPage]
    args = [(row[i][4], app, row[i][0], row[i][5]), (app,)]

    app.navegate(0, btns, functions, True, args)

def execute_game(path, app, xp, id):
    match path:
        case "catch_money":
            r = catch_money.CatchMoney(app, xp, id)
            r.start()
        case "whack_mole":
            r = whack_mole.WhackMole(app, xp, id)
            r.start()
        case "fnf_game":
            fnf_game.start(app, xp, id)
        case "no_game":
            r = no_game.HandsTracking()
            messagebox.showwarning("NOTA:", "Si no puede realizar un ejercicio presione ESC para terminar.\n\nBAJAR LOS DEDOS NO ES LO MISMO QUE CERRAR EL PUÑO.\n\n\n\nSE RECOMIENDA SUBIR LAS DOS MANOS PARA EVITAR PROBLEMAS DE DETECCIÓN.")
            r.start(app, xp, id)