import re

users = {}
rules = {}
size_rule = None

#crear archivo resultado
resultado = open("Resultados.txt",'w')

SIZE_RULE = re.compile(r'^SIZE RULE (\d+)$')
NEW_RULE = re.compile(r'^NEW RULE ([a-zA-Z][a-zA-Z0-9]*) ([0-9,]+)$')
ADD_TO_RULE = re.compile(r'^ADD_TO RULE ([a-zA-Z][a-zA-Z0-9]*) ([0-9,]+)$')
REMOVE_FROM_RULE = re.compile(r'^REMOVE_FROM RULE ([a-zA-Z][a-zA-Z0-9]*) ([0-9,]+)$')
DELETE_RULE = re.compile(r'^DELETE RULE ([a-zA-Z][a-zA-Z0-9]*)$')
NEW_PASSWORD = re.compile(r'^NEW PASSWORD FROM ([a-zA-Z][a-zA-Z0-9]*) ([a-zA-Z0-9]+)$')
CHANGE_PASSWORD = re.compile(r'^CHANGE PASSWORD FROM ([a-zA-Z][a-zA-Z0-9]*) ([a-zA-Z0-9]+) ([a-zA-Z0-9]+)$')
SHOW_PASSWORD = re.compile(r'^SHOW PASSWORD FROM ([a-zA-Z][a-zA-Z0-9]*)$')
DELETE_PASSWORD = re.compile(r'^DELETE PASSWORD FROM ([a-zA-Z][a-zA-Z0-9]*)$')
FUSION = re.compile(r'^FUSION ([a-zA-Z][a-zA-Z0-9]*) ([a-zA-Z][a-zA-Z0-9]*) INTO ([a-zA-Z][a-zA-Z0-9]*)$')

'''
***
linea : string
...
***
None
***
Funcion que determina que comando se debe ejecutar segun lo que se indique en linea
'''
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
    
    elif linea.startswith("SHOW PASSWORD FROM"):
        show_password(linea)
        return
    
    elif linea.startswith("DELETE PASSWORD FROM"):
        delete_password(linea)
        return
    
    elif linea.startswith("FUSION"):
        fusion(linea)
        return
    
'''
***
linea : string
...
***
None
***
Funcion que determina el valor de rule_size
''' 
def rule_size(linea):
    match = re.match(SIZE_RULE, linea)
    try:
        global size_rule
        size_rule=int(match.group(1))
    
        resultado.write("Regla de tamaño agregada con exito.\n")
    except:
        resultado.write("Error al tratar de ingresar regla de tamaño.\n")

'''
***
linea : string
...
***
None
***
Funcion que agrega nuevas reglas en el diccionario de reglas
''' 
def new_rule(linea):
    match = re.match(NEW_RULE, linea)
    try: 
        nombre = match.group(1)
        elems = match.group(2).split(",")
        if nombre not in rules:
            rules.update({nombre : elems})
            resultado.write("Se agrego la regla " + nombre + " con exito.\n")
        else:
            resultado.write("El nombre de la regla que se quiere ingresar ya existe.\n")
    except:
        resultado.write("Error en el formato al tratar de ingresar la nueva regla.\n")

'''
***
linea : string
...
***
None
***
Funcion que agrega elementos a una regla ya existente
''' 
def add_to_rule(linea):
    match = re.match(ADD_TO_RULE, linea)
    try:
        nombre = match.group(1)
        elems = match.group(2).split(",")
        if nombre in rules:
            new = rules[nombre] + elems
            rules[nombre] = new
            resultado.write("Elementos añadidos a la regla " + nombre + ".\n")
        else:
            resultado.write("La regla a la que se busca agregar no existe o el nombre esta mal escrito.\n")
    except:
        resultado.write("Error en el formato al tratar de añadir los elementos.\n")

'''
***
linea : string
...
***
None
***
Funcion que elimina elementos de una regla ya existente
''' 
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
            resultado.write("Se extrajeron los elementos de la regla " + nombre + "con exito.\n")
        else:
            resultado.write("La regla a la que se busca eliminar elementos no existe o el nombre esta mal escrito.\n")
    except:
        resultado.write("Error en el formato al tratar de eliminar los elementos.\n")

'''
***
linea : string
...
***
None
***
Funcion que eliminar reglas junto a los elementos asociados
''' 
def delete_rule(linea):
    match = re.match(DELETE_RULE, linea)
    try:
        nombre = match.group(1)

        if nombre in rules:
            del rules[nombre]
            resultado.write("Se elimino la regla " + nombre + " con exito.\n")
        else:
            resultado.write("La regla que se quiso eliminar no existe o el nombre esta mal escrito.\n")
    except:
        resultado.write("Error en el formato al tratar el eliminar la regla.\n")

'''
***
linea : string
...
***
None
***
Funcion que comprueba si un usuario puede ser registrado en base a su contraseña
''' 
def new_password(linea):
    match = re.match(NEW_PASSWORD, linea)
    try:
        
        nombre = match.group(1)
        password = match.group(2)
        
        flag = test(password)
        
        if flag == True:
            if nombre not in users:
                users.update({nombre:password})
                resultado.write("La contraseña para el usuario " + nombre + " fue correctamente registrada.\n")
            else: 
                resultado.write("El usuario ya esta registrado.\n")
        elif flag == False:
            return

    except:
        resultado.write("Error en el formato para ingreasar la contraseña.\n")

'''
***
linea : string
...
***
None
***
Funcion que actualiza la contraseña de un usuario ya registrado en condicion de las reglas actuales
''' 
def change_password(linea):
    match = re.match(CHANGE_PASSWORD, linea)
    try:
        nombre = match.group(1)
        old = match.group(2)
        new = match.group(3)
        if nombre not in users:
            resultado.write("Usuario no encontrado en el registro.\n")
            return
        if test(new):
            users[nombre] = new
            resultado.write("Contraseña de " + nombre + " actualizada con exito.\n")    
        else:
            resultado.write("La nueva contraseña no cumple los requisitos (se conservara la anterior).\n")
    except:
        resultado.write("Error en el formato para cambiar cotraeña.\n")

'''
***
linea : string
...
***
None
***
Funcion que muestra/registra la contraseña del usuario
''' 
def show_password(linea):
    match = re.match(SHOW_PASSWORD, linea)
    try:
        nombre = match.group(1)
        if nombre in users:
            resultado.write(users[nombre])
        else:
            resultado.write("El usuario no se encuentra registrado.\n")
    except:
        resultado.write("Error en el formato para mostrar la contraseña.\n")

'''
***
linea : string
...
***
None
***
Funcion que elimina la contraseña del usuario 
''' 
def delete_password(linea):
    match = re.match(DELETE_PASSWORD, linea)
    try:
        nombre = match.group(1)
        if nombre in users:
            del users[nombre]
            resultado.write("Contraseña del usuario " + nombre + " eliminada.\n")
        else:
            resultado.write("El usuario no se encuentra registrado.\n")

    except:
        resultado.write("Error en el formato para mostrar la contraseña.\n")        

'''
***
linea : string
...
***
None
***
Fusion que concatena dos contraseñas ya registradas y se la asigna a un usuario
''' 
def fusion(linea):
    match = re.match(FUSION, linea)
    try:
        pri = match.group(1)
        sec = match.group(2)
        ter = match.group(3)
        
        if pri and sec in users:
            if ter in users:
                users[ter] = users[pri] + users[sec] 
                resultado.write("Fusion exitosa.\n")
            else:
                resultado.write("El tercer nombre de usuario no se encuentra registrado.\n")
        else:
            resultado.write("Uno de los primeros nombres de usuario no se encuentraregistrado.\n")
    except:
        resultado.write("Error en el formato de la fusion.\n")

'''
***
linea : string
...
***
bool
***
Funcion que verifica que ñas contraseñas cumplas las condiciones
''' 
def test(password):
    general = True
    size = True
    
    if size_rule != None:
        if len(password) < size_rule:
            size = False
    
    for elems in rules.values():
        for elem in elems:
            if elem in password:
                general = False
                break
    
    if general and size == True:
        return True
        
    elif general == False and size == True:
        resultado.write("La nueva contraseña cuenta con elementos no permitidos.\n")
        return False
    
    elif general ==  True and size  == False:
        resultado.write("La nueva contraseña no cumple el largo minimo solicitiado.\n")
        return False
    
    else:
        resultado.write("La nueva contraseña cuenta con elementos no permitidos y no es del largo exigido.\n")
        return False

def main():

    try:
        #abrir y leer archivo logsansano
        archivo = open("logSansano.txt",'r')
        lineas = archivo.readlines()
        for linea in lineas:
            ejecutar(linea)    
        archivo.close()
        
    except:
        resultado.write("El archivo no fue encontrado en le directorio.")
    
    resultado.close()
    return

if __name__ == "__main__":
    main()
