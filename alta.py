import os
import MySQLdb
import sys
import string
#solicitamos el nombre
nombre = (sys.argv[1])
ndominio = (sys.argv[2])
#establecemos conexion con base de datos
base = MySQLdb.connect(host="hosting.zakardo.com", user="root", passwd="usuario", db="hosting")
cursor=base.cursor()
#buscamos la existencia del usuario mediante mysql
busquedausuario="select nombre from usuarios where nombre='%s';" %nombre
cursor.execute(busquedausuario)
busqueda_usuario = cursor.fetchone()
consultadominio="select ndominio from usuarios where ndominio='%s';" %ndominio
cursor.execute(consultadominio)
consulta_dominio = cursor.fetchone()
if busqueda_usuario !=None or consulta_dominio !=None:
        print "nombre de usuario o dominio existente"
        sys.exit
else:
        print "facil"


