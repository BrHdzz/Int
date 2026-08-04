import dashboard_page
import db

def results(app, misses, score, id, xp):
    app.deletePage(app.mainFr)

    money = score / 10
    total = money + misses
    acc = 100 - ((misses * 100) / total)
    xpT = int(xp * (acc / 100))

    fr = app.frames(app.mainFr)
    fr.configure(fg_color = "#000")
    fr.pack(fill = "both", expand = True)

    label = app.labelTitle(fr, "Resultados")
    label.configure(bg = "#000")
    label.pack(pady = 10)

    missL = app.labelTxt(fr, f"Fallos: {misses}")
    missL.pack(pady = 5)

    scoL = app.labelTxt(fr, f"Puntaje: {score}")
    scoL.pack(pady = 5)

    accL = app.labelTxt(fr, f"Precisión: {acc:.1f}%")
    accL.pack(pady = 5)

    xpL = app.labelTxt(fr, f"Experiencia: + {xpT}XP")
    xpL.pack(pady = 5)

    gif = app.gifs(fr, "images/asian_guy.gif", 278, 100)
    gif.pack(pady = 10)

    db.insertResultAct(xpT, acc, id)

    back = app.buttons(fr, "Aceptar")
    back.configure(command = lambda:dashboard_page.dasboardPage(app))
    back.pack(fill = "x", padx = 100, pady = 10)