import os,logging, sys

logging.basicConfig(filename='app.log',filemode='a',format='%(asctime)s - %(message)s', level=logging.INFO)

def docker_login(username, password, registry):
    print("Docker login")
    logging.info('*** Docker login ***')

    check = os.system("docker login --username={0} --password={1} {2}".format(username,password,registry))
    if check >0:
        logging.error("Error en el login del registry {0}".format(registry))
    
    return check

def retag_images(registry,old_registry):
    images = []
    for l in list(dict.fromkeys(os.popen("docker images | awk '{ if( FNR>1 ) { print $1 } }' | grep -w "+old_registry).read().split('\n'))):
        if l != '':
            images.append(l)
    for i in images:

        for t in list(dict.fromkeys(os.popen("docker images "+i+"| awk '{ if( FNR>1 ) { print $2 } }'").read().split('\n'))):
            if t != '':
                os.system("docker tag {0}:{1}  {2}:{3}".format(i,t,str(registry+"/"+i.split("/")[1]),t))


def push_images(registry):
    global count
    count = 0
    images = []
    for l in list(dict.fromkeys(os.popen("docker images | awk '{ if( FNR>1 ) { print $1 } }' | grep -w "+registry).read().split('\n'))):
        if l != '':
            images.append(l)
    for i in images:
        logging.info("Haciendo push de {0} ".format(i)) 
        os.system("docker push {0}".format(i))
        count = count+1
        
def push(registry, username, password, old_registry):
    docker = docker_login(username, password, registry)
    if docker >0:
        return "Eror en el login"
    retag_images(registry, old_registry)
    push_images(registry)

    return "Se subieron {0} imagenes".format(count)