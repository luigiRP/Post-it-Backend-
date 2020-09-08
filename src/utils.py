from flask import jsonify, url_for
from email.utils import parseaddr
from datetime import datetime

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img style="max-height: 80px" src='https://ucarecdn.com/3a0e7d8b-25f3-4e2f-add2-016064b04075/rigobaby.jpg' />
        <h1>Rigo welcomes you to your API!!</h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p>Start working on your proyect by following the <a href="https://github.com/4GeeksAcademy/flask-rest-hello/blob/master/docs/_QUICK_START.md" target="_blank">Quick Start</a></p>
        <p>Remember to specify a real endpoint path like: </p>
        <ul style="text-align: left;">"""+links_html+"</ul></div>"

#El parametro data_user a utilizar puede tomar cualquier nombre, no es el mismo de Main, lo llamamos igual para

def validation_username(data_user):
    username = data_user.get("username")
    #validando el largo de username y que username contenga solo letras y numeros
    return len(username) > 6 and username.isalnum()

def validation_email(data_user):
    email = data_user.get("email")
    lista_email = parseaddr(email)
    #validando email
    return lista_email[1] == email
    
def validation_name(data_user):
    name = data_user.get("name")
    #validando el largo de name, que contenga solo letras y no contenga espacios   
    return len(name) > 0 and name.isalpha() and name.istitle() 
    #and len(name.split()) > 0 o " " in name

def validation_password(data_user):
    password = data_user.get("password")
    #validando que la contraseña sea de 8 o mas digitos, tenga mayusculas, minusculas y numeros
    return len(password) > 7

def validation_date(posting):
    date = posting.get("date")
    #validando formato fecha y hora
    try:
        valid_datetime = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False