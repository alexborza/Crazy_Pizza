from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.secret_key = "Secret Key"


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titlu = db.Column(db.String(100))
    pret = db.Column(db.String(100))
    ingrediente = db.Column(db.String(100))
    poza = db.Column(db.String(100))

    def __init__(self, titlu, pret, ingrediente, poza):
        self.titlu = titlu
        self.pret = pret
        self.ingrediente = ingrediente
        self.poza = poza


class Recenzii(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100))
    recenzie = db.Column(db.String(100))

    def __init__(self, nume, recenzie):
        self.nume = nume
        self.recenzie = recenzie


class Mesaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100))
    prenume = db.Column(db.String(100))
    email = db.Column(db.String(100))
    subiect = db.Column(db.String(100))
    mesaj = db.Column(db.String(100))

    def __init__(self, nume, prenume, email, subiect, mesaj):
        self.nume = nume
        self.prenume = prenume
        self.email = email
        self.subiect = subiect
        self.mesaj = mesaj

@app.route('/get-pizza/<int:id>', methods=['GET', 'POST'])
def GetPizza(id):
    pizza = Data.query.filter_by(id=id).first()
    if request.method == 'POST':
        return render_template("editare.html", pizza=pizza)


class Rezervare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100))
    hours = db.Column(db.String(100))
    nume = db.Column(db.String(100))
    telefon = db.Column(db.String(100))
    persoane = db.Column(db.String(100))


    def __init__(self, data, hours, nume, telefon, persoane):
        self.data = data
        self.hours = hours
        self.nume = nume
        self.telefon = telefon
        self.persoane = persoane



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logare_admin')
def Index():
    all_data = Data.query.all()

    return render_template("admin.html", pizze=all_data)

@app.route('/meniu')
def meniu():
    all_data = Data.query.all()

    return render_template("meniu.html", photos=all_data)

@app.route('/upload')
def upload():
    target = os.path.join(APP_ROOT, 'static/images')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)


@app.route('/upload1')
def upload1():
    target = os.path.join(APP_ROOT, 'static/images')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file1"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)


def VerificaRezervare():
    rezervare = Rezervare.query.all()

    return rezervare


def VerificaPizza():
    pizze = Data.query.all()

    return pizze


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        titlu = request.form['titlu']
        pret = request.form['pret']
        ingrediente = request.form['ingrediente']
        upload()
        for file in request.files.getlist("file"):
            poza = file.filename

        pizze = VerificaPizza()
        for pizza in pizze:
            if titlu.lower() == pizza.titlu.lower():
                flash("Exista deja o pizza cu acest nume!")
                return redirect(url_for('Index'))

        my_data = Data(titlu, pret, ingrediente, poza)
        db.session.add(my_data)
        db.session.commit()

        flash("O noua Pizza a fost adaugata cu succes!")

        return redirect(url_for('Index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.titlu = request.form['titlu']
        my_data.pret = request.form['pret']
        my_data.ingrediente = request.form['ingrediente']
        upload()
        for file in request.files.getlist("file"):
            my_data.poza = file.filename

        db.session.commit()
        flash("Inregistrarea a fost modificata!")

        return redirect(url_for('Index'))



@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Inregistrarea a fost stearsa!")

    return redirect(url_for('Index'))


@app.route('/inserare_recenzie', methods=["POST"])
def inserare_recenzie():
    if request.method == "POST":
        nume = request.form['nume']
        recenzie = request.form['recenzieText']

        my_recenzie = Recenzii(nume, recenzie)
        db.session.add(my_recenzie)
        db.session.commit()
        return index()


@app.route('/inserare_rezervare', methods=["POST"])
def inserare_rezervare():
    if request.method == "POST":
        count = 0
        data = request.form['data']
        hours = request.form['hours']
        nume = request.form['nume']
        telefon = request.form['telefon']
        persoane = request.form['persoane']

        rezervare_data = VerificaRezervare()
        for rezervare in rezervare_data:
            if data == rezervare.data:
                if hours == rezervare.hours:
                    count = count + 1

        if count > 3:
            flash("Nu mai avem mese disponibile la aceasta ora")
            return redirect(url_for('rezervare'))


        if hours == "hour-select":
            flash("Inregistrarea nu a fost adaugata!")
            return redirect(url_for('rezervare'))
        else:
            my_rezervare = Rezervare(data, hours, nume, telefon, persoane)
            db.session.add(my_rezervare)
            db.session.commit()
            flash("Rezervarea a fost facuta cu succes!")
            return redirect(url_for('rezervare'))


@app.route('/logare_admin', methods=['GET', 'POST'])
def logare_admin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username == "alexandru" and password == "borza":
            return Index()
        else:
            flash('Credentiale Invalide')
            return redirect(url_for('logare'))


@app.route('/contact_message', methods=["POST"])
def contact_message():
    if request.method == "POST":
        nume = request.form['nume']
        prenume = request.form['prenume']
        email = request.form['email']
        subiect = request.form['subiect']
        mesaj = request.form['message']

        my_message = Mesaje(nume, prenume, email, subiect, mesaj)
        db.session.add(my_message)
        db.session.commit()
        flash('Mesajul a fost trimis!')
        return redirect(url_for('contact'))


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/recenzie')
def recenzie():
    all_data = Recenzii.query.all()

    return render_template("recenzie.html", recenzii=all_data)

@app.route('/mesaje')
def mesaje():
    all_data = Mesaje.query.all()

    return render_template("mesaje.html", mesaje=all_data)


@app.route('/logare')
def logare():
    return render_template('logare.html')


@app.route('/rezervare')
def rezervare():
    return render_template('rezervare.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/editare')
def editare():
    return render_template('editare.html')


if __name__ == "__main__":
    app.run(debug=True)