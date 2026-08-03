import dashboard_page
import secrets
import qrcode
import done_payment_page

def payPage(app, method, amount):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20, ipadx = 5, ipady = 5)

    img = app.images(frTitle, "images/poor.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Donación")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)
    
    label = app.labelTxt(app.mainFr, "Su contribución ayuda a otras personas día con día.")
    label.pack(pady = 20)

    if method == "BitCoin":
        addr = "bc1q" + secrets.token_hex(20)

        qr = qrcode.make(addr)
        qr.save("images/qr.png")
    elif method == "Monero":
        addr = "48" + secrets.token_hex(46)

        qr = qrcode.make(addr)
        qr.save("images/qr.png")
    
    label = app.labelTxt(app.mainFr, f"Dirección: {addr}")
    label.pack(pady = 20)

    qrImg = app.images(app.mainFr, "images/qr.png", 250, 250)
    qrImg.pack(pady = 15)
    
    back = app.buttons(app.mainFr, "Pagar")
    back.configure(command = lambda:done_payment_page.donePayPage(app, method, amount))
    back.pack(pady = 5, padx = 100, fill = "x")
    
    back = app.buttons(app.mainFr, "Atrás")
    back.configure(width = 70, command = lambda:dashboard_page.dasboardPage(app))
    back.pack(pady = 5, padx = 100, fill = "x")