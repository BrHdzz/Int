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
                #messagebox.showinfo("Errorn't", f"Inicio de sesión exitoso.")

                with open("session.json", "w") as f:
                    json.dump({"id_user": row[0]}, f)
                
                dashboard_page.dasboardPage(app)

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