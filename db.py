import mysql.connector
from tkinter import messagebox
import re
from datetime import datetime, timedelta
import bcrypt
import os
import json
import dashboard_page
import profile_page
import main_page
import tkinter as tk
import var_config
import admin_dashboard
import view_profile_user_admin
import view_results_user_admin
import obj

def connectSQL():
    try:
        return mysql.connector.connect(
            host = "127.0.0.1",
            user = "root",
            password = "",
            database = "integradora"
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al conectar.")
        return None

def signin(name, passwd, uname, mail,app):
    conn = connectSQL()

    if conn == None:
        return
    
    cur = conn.cursor()

    try:
        cur.execute("select username, email from user where username = %s or email = %s", (uname, mail))
        
        if not name or not passwd or not uname or not mail:
            messagebox.showerror("Error", f"Complete todos los campos.")
        elif len(uname) > 15:
            messagebox.showerror("Error", f"El nombre de usuario debe tener máximo 15 caracteres.")
        elif not re.search('[a-z]', uname[0]) or not re.search('[a-z0-9._]', uname):
            messagebox.showerror("Error", f"El nombre de usuario debe empezar con una letra y solo puede tener letras minúsculas y números..")
        elif not re.match(r'^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$', mail):
            messagebox.showerror("Error", f"Dirección de correo electrónico no válida")
        elif not len(passwd) in range (8, 21):
            messagebox.showerror("Error", f"La contraseña debe tener de 8 a 20 caracteres.")
        elif not re.search("[a-zA-Z0-9_.@#$%=]", passwd):
            messagebox.showerror("Error", f"La contraseña debe estar compuesta por letras mayúsculas o minúsculas, números o los carácteres: _.@#$%=")
        elif cur.fetchone():
            messagebox.showerror("Error", f"Nombre de usuario o correo en uso.")
        else:
            date = datetime.now()

            cryp_pass = bcrypt.hashpw(bytes(passwd, "utf-8"), bcrypt.gensalt(12)).decode("utf-8")

            cur.execute("select passw from passwd where passw = %s", (passwd,))

            if cur.fetchone():
                messagebox.showerror("Error", f"Ingrese una contraseña más segura.")
            else:
                cur.execute("insert into user (name, passwd, username, email, date_, role, strike) values (%s, %s, %s, %s, %s, 0, 0)", (name, cryp_pass, uname, mail, date.date()))

                cur.execute("select id from user where username = %s", (uname,))

                iduser = cur.fetchone()

                cur.execute("insert into progress (xp, accurate, id_user) values (0, 0, %s)", (iduser[0],))
                
                conn.commit()

                messagebox.showinfo("Completado", f"Cuenta creada correctamente.")

                main_page.mainPage(app)
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al crear usuario.\nRevise su conexión e intente más tarde.")
    finally:
        conn.close()

def login(user, passwd, app):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select username, passwd, role, strike, date_kick from user where username = %s", (user,))

        row = cur.fetchone()
        
        if not user or not passwd:
            messagebox.showerror("Error", f"Complete todos los campos.")
        elif row is None:
            messagebox.showerror("Error", f"Contraseña o usuario incorrectos.")
        else:
            if bcrypt.checkpw(passwd.encode("utf-8"), row[1].encode("utf-8")):
                if row[2] == 9999:
                    admin_dashboard.dasboardPage(app)
                elif row[2] == 0:
                    match row[3]:
                        case 0:
                            dashboard_page.dasboardPage(app)

                            with open("session.json", "w") as f:
                                json.dump({"username": user, "password": passwd}, f)
                        case 1:
                            dashboard_page.dasboardPage(app)

                            messagebox.showwarning("Alerta", "A ver si nos vamos comportando, ¿eh?")

                            with open("session.json", "w") as f:
                                json.dump({"username": row[0], "password": passwd}, f)
                        case 2:
                            if datetime.now().date() < row[4]:
                                messagebox.showwarning("Alerta", f"La cuenta se encuentra suspendida por mal comportamiento. Disponible a partir del día {row[5]}.")
                            else:
                                messagebox.showwarning("Alerta", "A ver si nos vamos comportando, ¿eh?")

                                dashboard_page.dasboardPage(app)

                                with open("session.json", "w") as f:
                                    json.dump({"username": row[0], "password": passwd}, f)
                        case 3:
                            messagebox.showwarning("Alerta", "No se puede acceder a la cuenta, si se trata de un error, por favor contacte al soporte.")
                        case _:
                            messagebox.showwarning("Alerta", "No se puede acceder a la cuenta, si se trata de un error, por favor contacte al soporte.")

                conn.commit()
            else:
                messagebox.showerror("Error", f"Contraseña o Usuario incorrectos.\nIntente más tarde.")

                if os.path.exists("session.json"):
                    os.remove("session.json")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al iniciar sesión.\nRevise su conexión e intente más tarde.")
    finally:
        conn.close()

def user_info(app):
    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            username = session["username"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            cur.execute("select name, username, email, strike from user where username = %s", (username,))

            row = cur.fetchone()

            if row is None:
                messagebox.showerror("Error", f"Error al encontrar usuario.")
            else:
                user_name = row[0]
                user_username = row[1]
                user_email = row[2]
                user_strike = row[3]

                profile_page.profilePage(app, user_name, user_username, user_email, user_strike)
            
            conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al encontrar usuario.\nRevise su conexión e intente más tarde.")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", f"Error al encontrar usuario.\nIntente más tarde.")

def alter_user_info(app, attribute, index):
    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            username = session["username"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            if not attribute:
                messagebox.showerror("Error", f"Complete todos los campos.")
            else:
                if index == 1: cur.execute("update user set name = %s where username = %s", (attribute, username))
                elif index == 2:
                    cur.execute("select * from user where username = %s", (attribute,))

                    row = cur.fetchone()

                    if row: return messagebox.showerror("Error", f"Nombre de usuario no disponible.")
                    elif not re.search('[a-z]', attribute[0]) or not re.search('[a-z0-9._]', attribute): return messagebox.showerror("Error", f"El nombre de usuario debe empezar con una letra y solo puede tener letras minúsculas y números.")
                    else:
                        cur.execute("update user set username = %s where username = %s", (attribute, username))
                        
                        session["username"] = attribute

                        with open("session.json", "w") as f:
                            json.dump(session, f, indent = 4)
                elif index == 3:
                    if not re.match(r'^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$', attribute):
                        return messagebox.showerror("Error", f"Dirección de correo electrónico no válida.")
                    else: cur.execute("update user set email = %s where username = %s", (attribute, username))
                else:
                    if len(attribute) >= 8 and len(attribute) <= 20:
                        if re.search("[a-zA-Z0-9_.@#$%=]", attribute):
                            cur.execute("select passw from passwd where passw = %s", (attribute,))

                            if cur.fetchone():
                                messagebox.showerror("Error", f"Ingrese una contraseña más segura.")
                            else:
                                cur.execute("select passwd from user where username = %s", (username,))

                                row = cur.fetchone()

                                if row[0]:
                                    if bcrypt.checkpw(attribute.encode("utf-8"), row[0].encode("utf-8")):
                                        return messagebox.showerror("Error", f"La contraseña no puede ser la misma.")
                                    else:
                                        cryp_pass = bcrypt.hashpw(bytes(attribute.encode("utf-8")), bcrypt.gensalt(12)).decode("utf-8")
                                        cur.execute("update user set passwd = %s where username = %s", (cryp_pass, username))
                        
                                        session["password"] = attribute

                                        with open("session.json", "w") as f:
                                            json.dump(session, f, indent = 4)
                        else:
                            messagebox.showerror("Error", f"La contraseña debe estar compuesta por letras mayúsculas o minúsculas, números o los carácteres: _.@#$%=")
                    else:
                        messagebox.showerror("Error", f"La contraseña debe tener de 8 a 20 caracteres.")
                conn.commit()

                messagebox.showinfo("Errorn't", f"Datos guardados.")

                dashboard_page.dasboardPage(app)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al modificar usuario.\nRevise su conexión e intente más tarde")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", f"Error al modificar usuario\nIntente más tarde.")

def logout(app):
    ans = messagebox.askquestion("Advertencia", "¿Seguro que quiere salir?")

    if ans == "yes":
        if os.path.exists("session.json"):
            os.remove("session.json")
        
        main_page.mainPage(app)

def donate(method, amount):
    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            username = session["username"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            cur.execute("select id from user where username = %s", (username,))

            id_user = cur.fetchone()

            if id_user:
                cur.execute("insert into premium (payment_method, amount, id_user) values (%s, %s, %s)", (method, amount, id_user[0]))

                conn.commit()

                return "Operación Terminada."
            else:
                return f"Error al completar la solicitud\nIntente más tarde."
        except mysql.connector.Error as e:
            return f"Error al completar transacción.\nRevise su conexión e intente más tarde."
        finally:
            conn.close()
    else:
        return f"Error al completar transacción.\nIntente más tarde."

def coments(txt, app):
    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            username = session["username"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            if not txt: messagebox.showerror("Error", f"Ingrese un comentario.")
            else:
                cur.execute("select id from user where username = %s", (username,))

                id_user = cur.fetchone()

                if id_user:
                    cur.execute("insert into message (description, date_, id_user, del) values (%s, %s, %s, 0)", (txt, datetime.now().date(), id_user[0]))
            
                    conn.commit()

                    messagebox.showinfo("Completado", "Comentario publicado.")

                    dashboard_page.dasboardPage(app)
                else:
                    messagebox.showinfo("Error", "No se pudo publicar su comentario.\nInténtelo de nuevo más tarde.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar.\nRevise su conexión e intente más tarde.")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "No se pudo publicar su comentario.\nInténtelo de nuevo más tarde.")

def showComents(parent):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select m.del, m.description, m.date_, u.username from message m inner join user u on (m.id_user = u.id)")

        row = cur.fetchall()

        if row:
            for i in row:
                fr = tk.LabelFrame(parent, text = f"{i[3]} ({i[2]})", border = 2, bg = "#000", fg = "#cb6ce6", highlightcolor = "#5e17eb", font = ("Inter", (var_config.fontSizeText - 1)))
                fr.pack(ipady = 2, ipadx = 5, pady = 10)

                if i[0] == 0:
                    tk.Label(fr, text = f"{i[1]}", bg = "#000000", fg = "#ffffff", font = ("Inter", var_config.fontSizeText), width = obj.root.winfo_reqwidth() - 675, anchor = "w", justify = "left", wraplength = obj.root.winfo_reqwidth() - 675).pack()
                elif i[0] == 1:
                    tk.Label(fr, text = f"{i[1]}", bg = "#000000", fg = "#555555", font = ("Inter", var_config.fontSizeText, "italic"), width = obj.root.winfo_reqwidth() - 675, anchor = "w", justify = "left", wraplength = obj.root.winfo_reqwidth() - 675).pack()
        else:
            tk.Label(parent, text = f"Sin resultados.", bg = "#000000", fg = "#555555", font = ("Inter", var_config.fontSizeText), width = 70, anchor = "w", justify = "left").pack()


        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al cargar comentarios:\n{e}")
    finally:
        conn.close()

def showComents_admin(parent, app):
    btn = []
    btn2 = []

    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select m.id, m.description, m.date_, m.del, u.username, u.id from message m inner join user u on (m.id_user = u.id)")

        row = cur.fetchall()

        if row:
            for i in range(len(row)):
                fr = tk.LabelFrame(parent, text = f"{row[i][4]}: {row[i][2]}", border = 2, bg = "#000", fg = "#cb6ce6", highlightcolor = "#5e17eb", font = ("Inter", (var_config.fontSizeText - 1)))
                fr.pack(ipady = 2, ipadx = 5, pady = 10)

                if row[i][3] == 0:
                    tk.Label(fr, text = f"{row[i][1]}", bg = "#000000", fg = "#ffffff", font = ("Inter", var_config.fontSizeText), width = obj.root.winfo_reqwidth() - 850, anchor = "w", justify = "left").grid(row = 0, column = 0, padx = 5)

                    btn.append(app.buttons(fr, "Eliminar"))
                    btn[i].configure(command = lambda id = row[i][1]:deleteComents(id, app))
                    btn[i].grid(padx = 5, row = 0, column = 1)

                    btn2.append(app.buttons(fr, "Ver perfil"))
                    btn2[i].configure(command = lambda id = row[i][4]:view_profile_user_admin.viewUsers_admin(id, app))
                    btn2[i].grid(padx = 5, row = 0, column = 2)
                elif row[i][3] == 1:
                    tk.Label(fr, text = f"{row[i][1]}", bg = "#000000", fg = "#888888", font = ("Inter", var_config.fontSizeText, "italic"), width = obj.root.winfo_reqwidth() - 850, anchor = "w", justify = "left").grid(row = 0, column = 0, padx = 5)

                    btn.append(app.buttons(fr, "Eliminar"))
                    btn[i].configure(state = "disabled")
                    btn[i].grid(padx = 5, row = 0, column = 1)

                    btn2.append(app.buttons(fr, "Ver perfil"))
                    btn2[i].configure(command = lambda id = row[i][4]:view_profile_user_admin.viewUsers_admin(id, app))
                    btn2[i].grid(padx = 5, row = 0, column = 2)
        else:
            lb = app.labelTxt(parent, f"Sin resultados.")
            lb.pack(pady = 10)
        
        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al cargar comentarios:\n{e}")
    finally:
        conn.close()

def deleteComents(coment, app):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()
        
        cur.execute("update message set description = 'Este mensage fue eliminado por el admin.', del = 1 where description = %s", (coment,))

        messagebox.showinfo("eladmintienezida", f"Comentario eliminado.")

        admin_dashboard.dasboardPage(app)

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al borrar comentario:\n{e}")
    finally:
        conn.close()

def showUsers_admin(parent, app):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select id, username, role from user")

        row = cur.fetchall()

        btn = []
        j = 0

        for i in range(len(row)):
            if row[i][2] == 0:
                fr = tk.LabelFrame(parent, text = f"id: {row[i][0]}", border = 2, bg = "#000", fg = "#cb6ce6", highlightcolor = "#5e17eb", font = ("Inter", (var_config.fontSizeText - 1)))
                fr.pack(ipady = 2, ipadx = 5, pady = 10)

                tk.Label(fr, text = f"{row[i][1]}", bg = "#000000", fg = "#ffffff", font = ("Inter", var_config.fontSizeText), width = obj.root.winfo_reqwidth() - 875, anchor = "w", justify = "left").grid(row = 0, column = 0, padx = 5)

                btn.append(app.buttons(fr, "Ver perfil"))
                btn[j].configure(command = lambda id = row[i][1]:view_profile_user_admin.viewUsers_admin(id, app))
                btn[j].grid(padx = 5, row = 0, column = 1)

                j = j + 1

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al cargar comentarios:\n{e}")
    finally:
        conn.close()

def profileUsers_admin(username):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select u.id, u.name, u.username, u.date_, u.email, u.strike, p.xp, p.accurate from user u inner join progress p on (p.id_user = u.id) where username = %s", (username,))

        row = cur.fetchone()

        if row:
            return row
        else:
            messagebox.showerror("Error", f"Error al mostrar usuario.")

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al mostrar usuario:\n{e}")
    finally:
        conn.close()

def getAdv(username):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select strike from user where username = %s", (username,))

        row = cur.fetchone()

        if row:
            if row[0] + 1 == 2:
                cur.execute("update user set strike = %s, date_kick = %s where username = %s", ((row[0] + 1), (datetime.today() + timedelta(days = 7)), username))
            else:
                cur.execute("update user set strike = %s where username = %s", ((row[0] + 1), username))

            messagebox.showinfo("Finalizado", f"El usuario recibió un strike.")
        else:
            messagebox.showerror("Error", f"Error al dar strike.")

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al dar strike:\n{e}")
    finally:
        conn.close()

def getRes_admin(app, user, parent):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select r.xp, r.accurate, r.date_, a.name from user u inner join result r on (r.id_user = u.id) inner join activity a on (a.id = r.id_activity) where username = %s", (user,))

        row = cur.fetchall()

        if row:
            for i in range(len(row)):
                fr = app.labelFrames(parent, f"{row[i][2]}")
                fr.pack(ipady = 5, ipadx = 5, pady = 10)
                
                lb = app.labelTxt(fr, f"XP: {row[i][0]}\nPresición: {row[i][1]}%\nActividad: {row[i][3]}")
                lb.config(anchor = "w", justify = "left", width = obj.root.winfo_reqwidth())
                lb.pack(padx = 100, fill = "x")
        else:
            lb = app.labelTxt(parent, f"Sin resultados.")
            lb.pack(pady = 10)

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al mostrar resultados:\n{e}")
    finally:
        conn.close()

def getDonation_admin(app, user, parent):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select d.payment_method, d.amount from user u inner join premium d on (d.id_user = u.id) where username = %s", (user,))

        row = cur.fetchall()

        if row:
            for i in range(len(row)):
                fr = app.labelFrames(parent, f"Donación")
                fr.pack(ipady = 2, ipadx = 5, pady = 10)
                
                lb = app.labelTxt(fr, f"Cantidad (MXN): ${row[i][1]}\nMétodo de Pago: {row[i][0]}")
                lb.config(anchor = "w", justify = "left", width = obj.root.winfo_reqwidth())
                lb.pack()
        else:
            lb = app.labelTxt(parent, f"Sin resultados.")
            lb.pack(pady = 10)

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al mostrar resultados:\n{e}")
    finally:
        conn.close()

def getComent_admin(app, user, parent):
    btn = []
    
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select m.description, m.date_, m.del from user u inner join message m on (m.id_user = u.id) where username = %s", (user,))

        row = cur.fetchall()

        if row:
            for i in range(len(row)):
                fr = tk.LabelFrame(parent, text = f"Fecha: {row[i][1]}", border = 2, bg = "#000", fg = "#cb6ce6", highlightcolor = "#5e17eb", font = ("Inter", (var_config.fontSizeText - 1)))
                fr.pack(ipady = 2, ipadx = 5, pady = 10)

                if row[i][2] == 0:
                    tk.Label(fr, text = f"{row[i][0]}", bg = "#000000", fg = "#ffffff", font = ("Inter", var_config.fontSizeText), width = obj.root.winfo_reqwidth() - 600, anchor = "w", justify = "left").grid(row = 0, column = 0, padx = 5)

                    btn.append(app.buttons(fr, "Eliminar"))
                    btn[i].configure(command = lambda des = row[i][0]:deleteComents(des, app))
                    btn[i].grid(padx = 5, row = 0, column = 1)
                elif row[i][2] == 1:
                    tk.Label(fr, text = f"{row[i][0]}", bg = "#000000", fg = "#888888", font = ("Inter", var_config.fontSizeText, "italic"), width = obj.root.winfo_reqwidth() - 600, anchor = "w", justify = "left").grid(row = 0, column = 0, padx = 5)

                    btn.append(app.buttons(fr, "Eliminar"))
                    btn[i].configure( state = "disabled")
                    btn[i].grid(padx = 5, row = 0, column = 1)
        else:
            lb = app.labelTxt(parent, f"Sin resultados.")
            lb.pack(pady = 10)

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al mostrar resultados:\n{e}")
    finally:
        conn.close()

def deleteUser(app, user):    
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        adv = messagebox.askquestion("Alerta", f"¿Seguro de proceder?\nEsta acción no se puede deshacer.")

        if adv == "yes":
            cur.execute("delete from user where username = %s", (user,))

            messagebox.showinfo("Hecho", f"La cuenta se ha eliminado.")

            if os.path.exists("session.json"):
                os.remove("session.json")
                main_page.mainPage(app)
            else:
                admin_dashboard.dasboardPage(app)

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al eliminar usuario:\n{e}")
    finally:
        conn.close()

def getRes(app, parent):
    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            username = session["username"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            cur.execute("select id from user where username = %s", (username,))
            row = cur.fetchone()

            cur.execute("select r.xp, r.accurate, r.date_, a.name from result r inner join activity a on (a.id = r.id_activity) where id_user = %s order by date_ desc", (row[0],))

            row = cur.fetchall()

            if row:
                for i in range(len(row)):
                    fr = app.labelFrames(parent, f"{row[i][2]}")
                    fr.pack(ipady = 2, ipadx = 5, pady = 10)
                    
                    lb = app.labelTxt(fr, f"Experiencia: {row[i][0]}XP\nPresición: {row[i][1]:.1f}%\nActividad: {row[i][3]}")
                    lb.config(anchor = "w", justify = "left", width = obj.root.winfo_reqwidth())
                    lb.pack()
            else:
                lb = app.labelTxt(parent, f"Sin resultados.")
                lb.pack(pady = 10)

            conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al mostrar resultados:\nRevise su conexión e intente más tarde.")
        finally:
            conn.close()

def getProgress():
    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            username = session["username"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            cur.execute("select p.xp, p.accurate from user u inner join progress p on (u.id = p.id_user) where username = %s", (username,))

            row = cur.fetchone()

            if row:
                return row
            else: messagebox.showerror("Error", f"Error al mostrar resultados.")

            conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al mostrar resultados:\n{e}")
        finally:
            conn.close()

def getActivity():
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select xp, name, description, difficult, path_game, id from activity")

        row = cur.fetchall()

        if row:
            return row
        else: messagebox.showerror("Error", f"Error al mostrar ejercicios.")

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al mostrar ejercicios:\n{e}")
    finally:
        conn.close()

def insertResultAct(xp, acc, id_a):
    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            username = session["username"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            cur.execute("select id from user where username = %s", (username,))

            idu = cur.fetchone()

            cur.execute("insert into result (xp, accurate, date_, id_user, id_activity) values (%s, %s, %s, %s, %s)", (xp, acc, datetime.now(), idu[0], id_a))

            cur.execute("select id, accurate, xp from progress where id_user = %s", (idu[0],))

            row = cur.fetchone()

            if row:
                if row[1] == 0:
                    cur.execute("update progress set accurate = %s, xp = %s where id_user = %s", (acc, (row[2] + xp), idu[0]))
                else:
                    cur.execute("update progress set accurate = %s, xp = %s where id_user = %s", (((row[1] + acc) / 2), (row[2] + xp), idu[0]))
            else: messagebox.showerror("Error", f"Error al actualizar progreso.")

            conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al actualizar datos:\n{e}")
        finally:
            conn.close()

def sh_passw(app, parent):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select passw from passwd")

        row = cur.fetchall()

        if row:
            for i in row:
                fr = app.frames(parent)
                fr.configure(fg_color = "#2b2b2b")
                fr.pack(pady = 5, ipadx = 10, ipady = 5)

                lb = app.labelTxt(fr, i[0])
                lb.config(bg = "#2b2b2b", width = obj.root.winfo_reqwidth() - 875, anchor = "w", justify = "left")
                lb.pack()
        else:
            fr = app.frames(parent)
            fr.configure(fg_color = "#2b2b2b")
            fr.pack(pady = 5, ipadx = 10, ipady = 5)

            lb = app.labelTxt(fr, "Sin resultados.")
            lb.config(bg = "#2b2b2b", width = obj.root.winfo_reqwidth() - 875, anchor = "w", justify = "left")
            lb.pack()


        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al obtener datos:\n{e}")
    finally:
        conn.close()

def insert_password(pssw, app):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        if pssw and len(pssw) in range(8, 21):
            cur.execute("insert into passwd (passw) values (%s)", (pssw,))

            conn.commit()

            messagebox.showinfo("nose", f"Contraseña añadida.")

            admin_dashboard.dasboardPage(app)
        else:
            messagebox.showerror("Error", f"Ingrese una contraseña válida.")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al añadir datos:\n{e}")
    finally:
        conn.close()