# import main Flask class and request object
from flask import Flask, request
from pull import pull
from push import push

import json, requests, os,logging
# create the Flask app
app = Flask(__name__)


@app.route('/pull')
def query_pull():

    if 'proto' in request.args:
        pull_protocol = request.args.get('proto')
    else:
        return "Falta especificar protocolo ej: proto=http"

    if 'registry' in request.args:
        pull_registry = request.args.get('registry')
    else:
        return "Falta especificar registry ej: registry=myregistry.com:5000"
    
    if 'user' in request.args:
        pull_username = request.args.get('user')
    else:
        return "Falta especificar usuario ej: user=usuario"
    
    if 'pass' in request.args:
        pull_password = request.args.get('pass')
    else:
        return "Falta especificar password ej: pass=password"

    if 'pass' in request.args:
        pull_ignore_repos = request.args.getlist("ignore")
    else:
        pull_ignore_repos = []
        
    return pull(pull_protocol,pull_registry,pull_username,pull_password,pull_ignore_repos)


@app.route('/push')
def query_push():

    if 'registry' in request.args:
        registry = request.args.get('registry')
    else:
        return "Falta especificar registry ej: registry=myregistry.com:5000"
    
    if 'user' in request.args:
        username = request.args.get('user')
    else:
        return "Falta especificar usuario ej: user=usuario"
    
    if 'pass' in request.args:
        password = request.args.get('pass')
    else:
        return "Falta especificar password ej: pass=password"
    
    if 'old_registry' in request.args:
        old_registry = request.args.get('old_registry')
    else:
        return "Falta especificar el registry viejo ej: old_registry=old_myregistry.com:5000"
    
    return push(registry,username,password,old_registry)

@app.route('/help')
def query_help():
    msg= """        
        +++ PULL +++
        ARGS:
        protocol: http, https
        registry: registry server
        username: usuario del registry
        password: usuario del registry
        ignore: imagenes que no se desean migrar, se define un ignore por cada imagen

        Para realizar el pulleo de todas las imágenes y tags de un repo se debe
        de invocar /pull con los siguientes argumentos:
                        protocol, registry, username, password
        En caso de no querer pullear alguna imagen se debe de especificar con el argumento ignore.

        Ej: curl "http://127.0.0.1:5001/pull?proto=http&registry=docker.pruebas.com:5000&user=admin&pass=admin123&ignore=tomcat"

        +++ PUSH +++

        ARGS:
        registry: registry server
        username: usuario del registry
        password: usuario del registry
        old_registry: se debe especificar el registry viejo para el re-tageo de las imagenes

        Para realizar el push de todas las imágenes pulleadas anteriormente se debe
        de invocar /push con las siguientes argumentos del NUEVO registry:
                        protocol, registry, username, password, old_registry
        
        Ej: curl "http://127.0.0.1:5001/push?registry=docker.pruebas2.com:5000&user=admin&pass=admin123&old_registry=docker.pruebas.com:5000"
        """
    return msg

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5001)
