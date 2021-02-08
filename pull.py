#!/usr/bin/env python3
import json, requests, os,logging, sys

logging.basicConfig(filename='app.log',filemode='a',format='%(asctime)s - %(message)s', level=logging.INFO)


def get_json(url,username,password):
    response = requests.get(url,
                        auth=requests.auth.HTTPBasicAuth(
                            username, password))
    return response.json()

def get_tags(image, registry, protocol,username,password):
    url = protocol + "://" + registry + "/v2/"+ image + "/tags/list"
    j = get_json(url,username,password)
    tags = []
    for tag in j["tags"]:
        tags.append(tag)
    return tags

def pull_image(image, registry, protocol, username, password):
    tags = get_tags(image,registry, protocol, username, password)

    logging.info("*** Pull de {0} con las tags: {1} ***".format(image,tags))

    for t in tags:
        cmd = "docker pull {0}/{1}:{2}".format(registry,image,t)
        os.system(cmd)


def docker_login(username, password, registry):

    logging.info('Docker login')

    check = os.system("docker login --username={0} --password={1} {2}".format(username,password,registry))
    if check >0:
        logging.error("Error en el login del registry {0}".format(registry))
    
    return check
def pull(protocol, registry, username, password, ignore_repo):
    count=0
    docker = docker_login(username,password,registry)
    if docker >0:
        return "Error en el login"        
    logging.info("obteniendo imagenes")
    
    url = protocol + "://" + registry + "/v2/_catalog"
    j = get_json(url,username,password)
    for image in j["repositories"]:
       if image not in ignore_repo:
          pull_image(image,registry, protocol, username, password)
          count=count+1
        
    return "Se pullearon {0} imagenes".format(count)