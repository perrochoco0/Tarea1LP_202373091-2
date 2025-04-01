import re

users = {}
rules = {}
size_rule = None

SIZE_RULE = re.compile(r'^SIZE RULE (\d+)$')
NEW_RULE = re.compile(r'^NEW RULE (\w+) ([a-zA-Z0-9,]+)$')
ADD_TO_RULE = re.compile(r'^ADD_TO RULE (\w+) ([a-zA-Z0-9,]+)$')
REMOVE_FROM_RULE = re.compile(r'^REMOVE_FROM RULE (\w+) ([a-zA-Z0-9,]+)$')
DELETE_RULE = re.compile(r'^DELETE RULE (\w+)$')
NEW_PASSWORD = re.compile(r'^NEW PASSWORD FROM (\w+) (.+)$')
CHANGE_PASSWORD = re.compile(r'^CHANGE PASSWORD FROM (\w+) (.+) (.+)$')
SHOW_PASSWORD = re.compile(r'^SHOW PASSWORD FROM (\w+)$')
DELETE_PASSWORD = re.compile(r'^DELETE PASSWORD FROM (\w+)$')
FUSION = re.compile(r'^FUSION (\w+) (\w+) INTO (\w+)$')



def ejecutar(linea):
    
    if linea.startswith("SIZE RULE"):
        rule_size(linea)
        return
    
    elif linea.startswith("NEW RULE"):
        new_rule(linea)
        return

    elif linea.startswith("ADD_TO RULE"):
        add_to_rule(linea)
        return
    
    elif linea.startswith("REMOVE_FROM RULE"):
        remove_from_rule(linea)
        return
    
    elif linea.startswith("DELETE RULE"):
        delete_rule(linea)
        return
     
    elif linea.startswith("NEW PASSWORD FROM"):
        new_password(linea)
        return
    
    elif linea.startswith("CHANGE PASSWORD FROM"):
        change_password(linea)
        return
    #elif linea.startswith("SHOW PASSWORD FROM"):
        show_password(linea)
        return
    #elif linea.startswith("DELETE PASSWORD FROM"):
        delete_password(linea)
        return
    #elif linea.startswith("FUSION"):
        fusion(linea)
        return
    

# DEFINICION funcion de size rule
def rule_size(linea):
    match = re.match(SIZE_RULE, linea)
    try:
        size_rule=int(match.group(1))
        print("Regla de tamaño agregada con exito.")
    except:
        print("Error al tratar de ingresar regla de tamaño.")

#DEFINICION funcion que agrega nuevas reglas en el diccionario de reglas
def new_rule(linea):
    match = re.match(NEW_RULE, linea)
    try: 
        nombre = match.group(1)
        elems = match.group(2).split(",")
        if nombre not in rules:
            rules.update({nombre : elems})
            print("Se agrego la regla " + nombre + " con exito.")
        else:
            print("El nombre de la regla que se quiere ingresar ya existe.")
    except:
        print("Error en el formato al tratar de ingresar la nueva regla.")

#DEFINICION funcion que agrega elementos a una regla ya existente
def add_to_rule(linea):
    match = re.match(ADD_TO_RULE, linea)
    try:
        nombre = match.group(1)
        elems = match.group(2).split(",")
        if nombre in rules:
            new = rules[nombre] + elems
            rules[nombre] = new
            print("Elementos añadidos a la regla " + nombre + ".")
        else:
            print("La regla a la que se busca agregar no existe o el nombre esta mal escrito.")
    except:
        print("Error en el formato al tratar de añadir los elementos.")

#DEFINICION funcion que elimina elementos de una regla ya existente.
def remove_from_rule(linea):
    match = re.match(REMOVE_FROM_RULE, linea)
    
    try:
        nombre = match.group(1)
        elems = match.group(2).split(",")
        if nombre in rules:
            new = rules[nombre]

            for elem in elems:
                new.remove(elem)
            rules[nombre] = new
            print("Se extrajeron los elementos de la regla " + nombre + "con exito.")
        else:
            print("La regla a la que se busca eliminar elementos no existe o el nombre esta mal escrito.")
    except:
        print("Error en el formato al tratar de eliminar los elementos.")

#DEFINICION funcion que eliminar reglas junto a los elementos asociados.
def delete_rule(linea):
    match = re.match(DELETE_RULE, linea)
    try:
        nombre = match.group(1)

        if nombre in rules:
            del rules[nombre]
            print("Se elimino la regla " + nombre + " con exito.")
        else:
            print("La regla que se quiso eliminar no existe o el nombre esta mal escrito.")
    except:
        print("Error en el formato al tratar el eliminar la regla.")

#DEFINICION duncion que comprueba si un usuario puede ser registrado en base a su contraseña.
def new_password(linea):
    match = re.match(NEW_PASSWORD, linea)
    
    try:
        nombre = match.group(1)
        password = match.group(2)

        if test(password):
            users.update({nombre:password})
            print("La contraseña para el usuario " + nombre + " fue registrada.")
        elif test(password) == False:
            return

        if password.length() >= size_rule:
            size = True  
        
        if test(password) == True and size == True :
            users.update({nombre:password})
            print("La nueva contraseña para el usuario " + nombre + " fue registrada.")

        elif test(password) == True and size == False:
            print("La nueva contraseña cuenta con elementos no permitidos.")

        elif test(password) ==   False and size  == True:
            print("La nueva contraseña no cumple el largo minimo solicitiado.")

        else:
            print("La nueva contraseña cuenta con elementos no permitidos y no es del largo exigido")
    except:
        print("Error en el formato para ingreasar la contraseña")

def change_password(linea):
    match = re.match(CHANGE_PASSWORD, linea)
    try:
        nombre = match.group(1)
        old = match.group(2)
        new = match.group(3)
        if 


def test(password):
    general = True
    size = True

    if password.length() < size_rule:
        size = False
    
    for elems in rules.values():
        for elem in elems:
            if elem in password:
                general = False
                break
                
    
    if general and size:
        return True
    

def main():

    #abrir archivo logsansano
    #archivo = open("logSansano.txt")

    #crear archivo deregistro


    #for linea in archivo:
    #    ejecutar(linea)

    entrada = input()
    ejecutar(entrada)

    return

if __name__ == "__main__":
    main()