import mysql.connector
from tkinter import messagebox
import re
from datetime import datetime
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

def signin(name, passwd, uname, mail):
    conn = connectSQL()

    if conn == None:
        return
    
    cur = conn.cursor()

    try:
        cur.execute("select username, email from user where username = %s or email = %s", (uname, mail))
        
        if not name or not passwd or not uname or not mail:
            messagebox.showerror("Error", f"Complete todos los campos.")
        elif not len(passwd) in range (8, 21):
            messagebox.showerror("Error", f"La contraseña debe tener de 8 a 20 caracteres.")
        elif len(uname) > 15:
            messagebox.showerror("Error", f"El nombre de usuario debe tener máximo 15 caracteres.")
        elif not re.match(r'^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$', mail):
            messagebox.showerror("Error", f"Dirección de correo electrónico no válida")
        elif cur.fetchone():
            messagebox.showerror("Error", f"Nombre de usuario o correo en uso.")
        else:
            date = datetime.now()

            cryp_pass = bcrypt.hashpw(bytes(passwd, "utf-8"), bcrypt.gensalt(12)).decode("utf-8")

            cur.execute("select passw from passwd where passw = %s", (passwd,))

            if cur.fetchone():
                messagebox.showerror("Error", f"Ingrese una contraseña más segura.")
            else:
                cur.execute("insert into user (name, passwd, username, email, date_, role) values (%s, %s, %s, %s, %s, 0)", (name, cryp_pass, uname, mail, date.date()))

                cur.execute("select id from user where username = %s", (uname,))

                iduser = cur.fetchone()

                cur.execute("insert into progress (xp, accurate, id_user) values (0, 0, %s)", (iduser[0],))
                
                conn.commit()
                messagebox.showinfo("Errorn't", f"Cuenta creada correctamente.")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al crear usuario:\n{e}")
    finally:
        conn.close()

def login(user, passwd, app):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select * from user where username = %s", (user,))

        row = cur.fetchone()
        
        if not user or not passwd:
            messagebox.showerror("Error", f"Complete todos los campos.")
        elif row is None:
            messagebox.showerror("Error", f"Contraseña o usuario incorrectos.")
        else:
            passw = row[2]

            if bcrypt.checkpw(passwd.encode("utf-8"), passw.encode("utf-8")):
                if row[6] == 9999:
                    admin_dashboard.dasboardPage(app)
                elif row[6] == 0:
                    dashboard_page.dasboardPage(app)

                    with open("session.json", "w") as f:
                        json.dump({"id_user": row[0]}, f)

                conn.commit()
            else:
                messagebox.showerror("Error", f"Contraseña o Usuario incorrectos.")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al iniciar sesión:\n{e}")
    finally:
        conn.close()

def user_info(app):
    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            id_user = session["id_user"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            cur.execute("select name, username, email from user where id = %s", (id_user,))

            row = cur.fetchone()

            if row is None:
                messagebox.showerror("Error", f"Error al encontrar usuario.")
            else:
                user_name = row[0]
                user_username = row[1]
                user_email = row[2]

                profile_page.profilePage(app, user_name, user_username, user_email)
            
            conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al encontrar usuario.\n{e}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", f"Error al encontrar usuario.")

def alter_user_info(app, attribute, index):
    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            id_user = session["id_user"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            if not attribute:
                messagebox.showerror("Error", f"Complete todos los campos.")
            else:
                if index == 1: cur.execute("update user set name = %s where id = %s", (attribute, id_user))
                elif index == 2:
                    cur.execute("select * from user where username = %s", (attribute,))

                    row = cur.fetchone()

                    if row: return messagebox.showerror("Error", f"Nombre de usuario no disponible.")
                    else: cur.execute("update user set username = %s where id = %s", (attribute, id_user))
                elif index == 3:
                    if not re.match(r'^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$', attribute):
                        return messagebox.showerror("Error", f"Dirección de correo electrónico no válida.")
                    else: cur.execute("update user set email = %s where id = %s", (attribute, id_user))
                else:

                    cur.execute("select passw from passwd where passw = %s", (attribute,))

                    if cur.fetchone():
                        messagebox.showerror("Error", f"Ingrese una contraseña más segura.")
                    else:
                        cur.execute("select passwd from user where id = %s", (id_user,))

                        row = cur.fetchone()

                        if row[0]:
                            if bcrypt.checkpw(attribute.encode("utf-8"), row[0].encode("utf-8")):
                                return messagebox.showerror("Error", f"La contraseña no puede ser la misma.")
                            else:
                                cryp_pass = bcrypt.hashpw(bytes(attribute.encode("utf-8")), bcrypt.gensalt(12)).decode("utf-8")
                                cur.execute("update user set passwd = %s where id = %s", (cryp_pass, id_user))
                
                conn.commit()

                messagebox.showinfo("Errorn't", f"Datos guardados.")

                dashboard_page.dasboardPage(app)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al modificar usuario.\n{e}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", f"Error al modificar usuario.")

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
            id_user = session["id_user"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            cur.execute("insert into premium (payment_method, amount, id_user) values (%s, %s, %s)", (method, amount, id_user))
            
            conn.commit()

            return "Operación Terminada."
        except mysql.connector.Error as e:
            return f"Error al completar transacción.\n{e}"
        finally:
            conn.close()
    else:
        return f"Error al completar transacción."

def coments(txt, app):
    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            id_user = session["id_user"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            if not txt: messagebox.showerror("Error", f"Ingrese un comentario.")
            else:
                cur.execute("insert into message (description, date_, id_user, del) values (%s, %s, %s, 0)", (txt, datetime.now().date(), id_user))
            
                conn.commit()

                messagebox.showinfo("Errorn't", "Comentario publicado.")

                dashboard_page.dasboardPage(app)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al publicar comentario.\n{e}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Error al publicar comentario.")

def showComents(parent):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select m.del, m.description, m.date_, u.username from message m inner join user u on (m.id_user = u.id)")

        row = cur.fetchall()

        for i in row:
            fr = tk.LabelFrame(parent, text = f"{i[3]} ({i[2]})", border = 2, bg = "#000", fg = "#cb6ce6", highlightcolor = "#5e17eb", font = ("Inter", (var_config.fontSizeText - 1)))
            fr.pack(ipady = 2, ipadx = 5, pady = 10)

            if i[0] == 0:
                tk.Label(fr, text = f"{i[1]}", bg = "#000000", fg = "#ffffff", font = ("Inter", var_config.fontSizeText), width = 70, anchor = "w", justify = "left").pack()
            elif i[0] == 1:
                tk.Label(fr, text = f"{i[1]}", bg = "#000000", fg = "#555555", font = ("Inter", var_config.fontSizeText, "italic"), width = 70, anchor = "w", justify = "left").pack()

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
                    tk.Label(fr, text = f"{row[i][1]}", bg = "#000000", fg = "#ffffff", font = ("Inter", var_config.fontSizeText), width = 70, anchor = "w", justify = "left").grid(row = 0, column = 0, padx = 5)

                    btn.append(app.buttons(fr, "Eliminar"))
                    btn[i].config(command = lambda id = row[i][0]:deleteComents(id, app))
                    btn[i].grid(padx = 5, row = 0, column = 1)

                    btn2.append(app.buttons(fr, "Ver perfil"))
                    btn2[i].config(command = lambda id = row[i][5]:view_profile_user_admin.viewUsers_admin(id, app))
                    btn2[i].grid(padx = 5, row = 0, column = 2)
                elif row[i][3] == 1:
                    tk.Label(fr, text = f"{row[i][1]}", bg = "#000000", fg = "#888888", font = ("Inter", var_config.fontSizeText, "italic"), width = 70, anchor = "w", justify = "left").grid(row = 0, column = 0, padx = 5)

                    btn.append(app.buttons(fr, "Eliminar"))
                    btn[i].config(state = "disabled")
                    btn[i].grid(padx = 5, row = 0, column = 1)

                    btn2.append(app.buttons(fr, "Ver perfil"))
                    btn2[i].config(command = lambda id = row[i][5]:view_profile_user_admin.viewUsers_admin(id, app))
                    btn2[i].grid(padx = 5, row = 0, column = 2)
        else:
            lb = app.labelTxt(parent, f"Sin resultados.")
            lb.pack(pady = 10)
        
        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al cargar comentarios:\n{e}")
    finally:
        conn.close()

def deleteComents(coment_id, app):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        if cur.execute("update message set description = 'Este mensage fue eliminado por el admin.', del = 1 where id = %s", (coment_id,)):
            messagebox.showinfo("eladmintienezida", f"Comentario eliminado.")
        else:
            messagebox.showerror("Error", f"Error al borrar comentario.")

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

                tk.Label(fr, text = f"{row[i][1]}", bg = "#000000", fg = "#ffffff", font = ("Inter", var_config.fontSizeText), width = 70, anchor = "w", justify = "left").grid(row = 0, column = 0, padx = 5)

                btn.append(app.buttons(fr, "Ver perfil"))
                btn[j].config(command = lambda id = row[i][0]:view_profile_user_admin.viewUsers_admin(id, app))
                btn[j].grid(padx = 5, row = 0, column = 1)

                j = j + 1

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al cargar comentarios:\n{e}")
    finally:
        conn.close()

def profileUsers_admin(id_user):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        idu = id_user

        cur.execute("select u.id, u.name, u.username, u.date_, u.email, u.tick, p.xp, p.accurate from user u inner join progress p on (p.id_user = %s) where u.id = %s", (id_user, idu))

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

def getAdv(id):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select tick from user where id = %s", (id,))

        row = cur.fetchone()

        if row:
            cur.execute("update user set tick = %s where id = %s", ((row[0] + 1), id))

            messagebox.showinfo("Finalizado", f"El usuario recibió un toque.")
        else:
            messagebox.showerror("Error", f"Error al dar toque.")

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al dar toque:\n{e}")
    finally:
        conn.close()

def getRes_admin(app, id, parent):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select r.xp, r.accurate, r.date_, a.name from result r inner join activity a on (a.id = r.id_activity) where id_user = %s", (id,))

        row = cur.fetchall()

        if row:
            for i in range(len(row)):
                fr = app.labelFrames(parent, f"Resultado")
                fr.pack(ipady = 2, ipadx = 5, pady = 10)
                
                lb = app.labelTxt(fr, f"XP: {row[i][0]}\nPresición: {row[i][1]}%\nFecha: {row[i][2]}\nActividad: {row[i][3]}")
                lb.config(width = 70, anchor = "w", justify = "left")
                lb.pack()
        else:
            lb = app.labelTxt(parent, f"Sin resultados.")
            lb.pack(pady = 10)

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al mostrar resultados:\n{e}")
    finally:
        conn.close()

def getDonation_admin(app, id, parent):
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select payment_method, amount from premium where id_user = %s", (id,))

        row = cur.fetchall()

        if row:
            for i in range(len(row)):
                fr = app.labelFrames(parent, f"Donación")
                fr.pack(ipady = 2, ipadx = 5, pady = 10)
                
                lb = app.labelTxt(fr, f"Cnatidad (MXN): ${row[i][1]}\nMétodo de Pago: {row[i][0]}")
                lb.config(width = 70, anchor = "w", justify = "left")
                lb.pack()
        else:
            lb = app.labelTxt(parent, f"Sin resultados.")
            lb.pack(pady = 10)

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al mostrar resultados:\n{e}")
    finally:
        conn.close()

def getComent_admin(app, id, parent):
    btn = []
    
    try:
        conn = connectSQL()

        if conn == None:
            return
        
        cur = conn.cursor()

        cur.execute("select description, date_, del, id from message where id_user = %s", (id,))

        row = cur.fetchall()

        if row:
            for i in range(len(row)):
                fr = tk.LabelFrame(parent, text = f"Fecha: {row[i][1]}", border = 2, bg = "#000", fg = "#cb6ce6", highlightcolor = "#5e17eb", font = ("Inter", (var_config.fontSizeText - 1)))
                fr.pack(ipady = 2, ipadx = 5, pady = 10)

                if row[i][2] == 0:
                    tk.Label(fr, text = f"{row[i][0]}", bg = "#000000", fg = "#ffffff", font = ("Inter", var_config.fontSizeText), width = 70, anchor = "w", justify = "left").grid(row = 0, column = 0, padx = 5)

                    btn.append(app.buttons(fr, "Eliminar"))
                    btn[i].config(command = lambda id = row[i][4]:deleteComents(id, app))
                    btn[i].grid(padx = 5, row = 0, column = 1)
                elif row[i][2] == 1:
                    tk.Label(fr, text = f"{row[i][0]}", bg = "#000000", fg = "#888888", font = ("Inter", var_config.fontSizeText, "italic"), width = 70, anchor = "w", justify = "left").grid(row = 0, column = 0, padx = 5)

                    btn.append(app.buttons(fr, "Eliminar"))
                    btn[i].config( state = "disabled")
                    btn[i].grid(padx = 5, row = 0, column = 1)
        else:
            lb = app.labelTxt(parent, f"Sin resultados.")
            lb.pack(pady = 10)

        conn.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al mostrar resultados:\n{e}")
    finally:
        conn.close()

'''def deleteAcc(app):
    if os.path.exists("session.json"):
        with open("session.json") as f:
            session = json.load(f)
            id_user = session["id_user"]

        try:
            conn = connectSQL()

            if conn == None:
                return
            
            cur = conn.cursor()

            if cur.execute("delete from ")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al eliminar usuario.\n{e}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", f"Error al eliminar usuario.")'''