import dashboard_page
import db

def results(app, misses, score, id, xp):
    app.deletePage(app.mainFr)

    money = score / 10
    total = money + misses if money + misses > 0 else 1
    acc = 100 - ((misses * 100) / total) if money + misses > 0 else 0.0
    xpT = int(xp * (acc / 100))

    title = "¡Perfecto!" if acc == 100 else "¡Buen trabajo!" if 100 > acc >= 80 else "Buen intento" if 80 > acc >= 60 else "Bien" if 60 > acc >= 40 else "Hay que practicar" if 30 > acc > 0 else "¿Qué pasó?"

    fr = app.frames(app.mainFr)
    fr.configure(fg_color = "#000")
    fr.pack(fill = "both", expand = True)

    label = app.labelTitle(fr, title)
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