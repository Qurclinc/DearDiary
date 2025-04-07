from flask import Flask, render_template, request, redirect, flash, make_response, url_for, abort, session
from config import SECRET_KEY, REGISTER_AVAILABLE
import datetime as dt

from app.dbworker import get_db, FDataBase, g
import app.security as sec
from app.fileworker import FileWorker
from app.Crypter import Crypter

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
# app.config["DATABASE"] = DATABASE
app.config["DEBUG"] = False
app.permanent_session_lifetime = dt.timedelta(days=30)

crypter = Crypter()

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

logged = None
is_admin = None
@app.before_request
def logging():
    global logged
    global is_admin
    if "logged" in session:
        logged = True
        is_admin = session["is_admin"]
    else:
        logged = False
        is_admin = None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if is_admin:
            try:
                id = int(request.form["id"])
                dbase.removeCase(id)
            except Exception:
                pass
        else:
            abort(405)
    return render_template("index.html", header=True, logged=logged, is_admin=is_admin, caseList=dbase.caseList(), footer=True)

@app.route("/admin", methods=["GET", "POST"])
def adminPannel():
    global REGISTER_AVAILABLE
    if not(is_admin):
        abort(403)
    if request.method == "POST":
        reg_av = request.form.get("reg_av")
        if reg_av:
            REGISTER_AVAILABLE = True
        else:
            REGISTER_AVAILABLE = False
    return render_template("admin.html", header=False, logged=logged, status=REGISTER_AVAILABLE, users=dbase.getUsers())

@app.route("/faq")
def faq():
    return render_template("faq.html", header=True, logged=logged, footer=True)

@app.route("/responses")
def responses():
    abort(503)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not(dbase.checkUser(request.form["username"])):
            if dbase.auth(request.form["username"], sec.encrypt(request.form["passwd"])):
                id, username, is_admin = dbase.login(request.form["username"], sec.encrypt(request.form["passwd"]))
                session["id"] = id
                session["username"] = username
                session["is_admin"] = is_admin
                session["logged"] = True
                session.permanent = True
                return redirect(url_for("login"))
            else:
                flash("Неверный пароль!", category="error")
        else:
            flash("Пользователь не существует!", category="error")
    if logged:
        return redirect(url_for("index"))
    return render_template("login.html", header=True, no_footer=True)

@app.route("/register", methods=["GET", "POST"])
def register():
    if logged:
        return redirect(url_for("index"))
    if request.method == "POST":
        if REGISTER_AVAILABLE:
            if sec.validation_username(request.form["username"])[0]:
                if dbase.checkUser(request.form["username"]):
                    if request.form["passwd"] == request.form["passwd2"]:
                        passwd = request.form["passwd"]
                        if sec.validation_password(passwd)[0]:
                            flash("Регистрация прошла успешно!", category="success")
                            dbase.addUser(request.form["username"], sec.encrypt(passwd))
                            return redirect(url_for("login"))
                        else:
                            flash(sec.validation_password(passwd)[1], category="error")
                    else:
                        flash("Пароли не совпадают!", category="error")
                else:
                    flash("Имя пользователя занято!", category="error")
            else:
                flash(sec.validation_username(request.form["username"])[1], category="error")
        else:
            flash("Извините, данная опиця временно недоступна.", category="error")
            return make_response(render_template("register.html", header=True), 403)
    return render_template("register.html", header=True)

@app.route("/logout")
def logout():
    session.pop("logged")
    session.pop("username")
    session.pop("id")
    session.pop("is_admin")
    return redirect(url_for("login"))

@app.route("/add_case", methods=["GET", "POST"])
def add_case():
    if not(is_admin):
        abort(403)
    if request.method == "POST":
        res = dbase.addCase(request.form["title"], request.form["text"])
        flash(res[1], category="success" if res[0] else "error")
    return render_template("add_case.html", header=False, logged=logged, case_css=True, footer=True)

@app.route("/<case_id>")
def showCase(case_id):
    try:
        id = int(case_id[4:])
        title, text = dbase.getCase(id)
        text = text.strip().replace("\n", "<br/>")
        # fw = FileWorker()
        # text = fw.readFile(url)
    except ValueError:
        abort(404)
    return render_template("case.html", header=False, logged=logged, title=title, is_admin=is_admin, text=text, case_css=True, footer=True)

@app.route("/decrypt")
def decrypt_text():
    return render_template("crypt.html", logged=logged, page_type="decrypt")

@app.route("/encrypt")
def encrypt_text():
    if not(is_admin):
        abort(403)
    return render_template("crypt.html", logged=logged, page_type="encrypt")

@app.route("/api/v1/deardiary/decrypt", methods=["POST"])
def decrypt():
    data = request.get_json()
    text = data["text"]
    key = data["key"]
    try:
        decrypted_data = crypter.decrypt(text, key)
        return {"status": "success", "data": decrypted_data}
    except Exception:
        return {"status": "fail", "data": ""}, 400
    
@app.route("/api/v1/deardiary/encrypt", methods=["POST"])
def encrypt():
    if not(is_admin):
        abort(403)
    data = request.get_json()
    text = data["text"]
    key = data["key"]
    try:
        encrypted_data = crypter.encrypt(text, key)
        return {"status": "success", "data": encrypted_data}
    except Exception:
        return {"status": "fail", "data": ""}, 400

@app.route("/teapot")
def teapot():
    abort(418)

@app.teardown_appcontext
def exit_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()

@app.errorhandler(400)
def Forbidden(error):
    title = "400. Некорректный запрос."
    error_text = "Вероятно, в синтаксисе запроса содержится ошибка. Перепроверьте его еще раз."
    return render_template("error.html", title=title, error_text=error_text), 400

@app.errorhandler(403)
def Forbidden(error):
    title = "403. Доступ закрыт."
    error_text = "Данная страница доступна только для администраторов. Убедитесь, что вы вошли в аккаунт с соответствующими правами."
    return render_template("error.html", title=title, error_text=error_text), 403

@app.errorhandler(404)
def NotFound(error):
    title = "404. Не найдено."
    error_text = "Данная страница не найдена. Если адрес был введён вручную, убедитесь что сделали это корректно."
    return render_template("error.html", title=title, error_text=error_text), 404

@app.errorhandler(405)
def NotFound(error):
    title = "405. Недопустимый метод."
    error_text = "Данный запрос никак не обрабатывается сервером или у вас недостаточно прав на его использование."
    return render_template("error.html", title=title, error_text=error_text), 405

@app.errorhandler(418)
def Forbidden(error):
    title = "418. Время чая."
    error_text = "Сам нашёл или кто подсказал?)))"
    return render_template("error.html", title=title, error_text=error_text), 418

@app.errorhandler(500)
def Forbidden(error):
    title = "500. Внутренняя ошибка."
    error_text = "Запрос вызвал внутреннюю ошибку сервера."
    return render_template("error.html", title=title, error_text=error_text), 500

@app.errorhandler(501)
def Forbidden(error):
    title = "501. Недопустимый запрос."
    error_text = "Сервер не имеет возможности обработать такой запрос."
    return render_template("error.html", title=title, error_text=error_text), 501

@app.errorhandler(502)
def Forbidden(error):
    title = "502. Ошибочный шлюз."
    error_text = "Нет ответа от вышестоящего сервера."
    return render_template("error.html", title=title, error_text=error_text), 502

@app.errorhandler(503)
def ServiceUnavailable(error):
    title = "503. Сервис недоступен."
    error_text = "Данная страница временно недоступна. Пожалуйста, попробуйте повторить запрос позднее."
    return render_template("error.html", title=title, error_text=error_text), 503

@app.errorhandler(504)
def Forbidden(error):
    title = "504. Превышено время ожидания."
    error_text = "Превышено время ожидания ответа от вышестоящего сервера."
    return render_template("error.html", title=title, error_text=error_text), 504

if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)