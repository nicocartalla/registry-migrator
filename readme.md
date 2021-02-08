### Registry migrator

Servicio rest en docker basado en flask para migrar las imágenes de un registry a uno nuevo.

Se utiliza docker in docker para no realizar el pull de las imagenes en el host

### Modo de uso
   
    docker-compose build
	docker-compose up -d

Los endpoint disponibles son `/pull` `/push` `/help` donde este último muestra el siguiente mensaje:
 

> **+++ PULL +++**
> 
> ARGS:
> 
> protocol: http, https
> 
> registry: registry server
> 
> username: usuario del registry
> 
> password: usuario del registry
> 
> ignore: imagenes que no se desean migrar, se define un ignore por cada
> imagen
> 
>   
> 
> Para realizar el pulleo de todas las imágenes y tags de un repo se
> debe
> 
> de invocar /pull con los siguientes argumentos:
> 
> protocol, registry, username, password
> 
> En caso de no querer pullear alguna imagen se debe de especificar con
> el argumento ignore.
> 
>   
> 
> Ej: `curl "http://127.0.0.1:5001/pull?proto=http&registry=docker.pruebas.com:5000&user=admin&pass=admin123&ignore=tomcat"`
> 
>   
> 
> **+++ PUSH +++**
> 
>   
> 
> ARGS:
> 
> registry: registry server
> 
> username: usuario del registry
> 
> password: usuario del registry
> 
> old_registry: se debe especificar el registry viejo para el re-tageo
> de las imagenes
> 
>   
> 
> Para realizar el push de todas las imágenes pulleadas anteriormente se
> debe
> 
> de invocar /push con las siguientes argumentos del NUEVO registry:
> 
> protocol, registry, username, password, old_registry
> 
> Ej: `curl "http://127.0.0.1:5001/push?registry=docker.pruebas2.com:5000&user=admin&pass=admin123&old_registry=docker.pruebas.com:5000"`

"""
