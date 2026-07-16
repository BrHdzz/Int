import tkinter as tk
import obj
import json
import os
import sigin_page
import login_page
import dashboard_page

def mainPage(app):
    app.deletePage(app.mainFr)

    label = app.labelTitle(app.mainFr, "Bienvenido")
    label.pack(pady = 5)

    img = app.images(app.mainFr, "images/main.png", 300, 300)
    img.pack(pady = 20)

    buttonFr = app.frames(app.mainFr)
    buttonFr.config(bg = "#000")
    buttonFr.pack(expand = True)

    singin = app.buttons(buttonFr, "Registrarse")
    singin.config(width = 20, command = lambda:sigin_page.signinPage(app))
    singin.grid(row = 0, column = 0, padx = 20)

    login = app.buttons(buttonFr, "Iniciar sesión")
    login.config(width = 20, command = lambda:login_page.loginPage(app))
    login.grid(row = 0, column = 1, padx = 20)
    
if __name__ == "__main__":
    app = obj.Window(obj.root, "Buenestar", "#000")

    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            id_user = session["id_user"]
        
        dashboard_page.dasboardPage(app)
    else:
        mainPage(app)

    obj.root.mainloop()