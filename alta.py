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
#creamos el document root del usuario junto al index.html    
        os.system("mkdir /var/www/%s" %nombre)
        os.system("cp /home/vagrant/index.html /var/www/%s"%nombre)
#crearemos el nuevo virtualhost
                virtual_host="/home/vagrant/virtual_host"
                modolectura=open(virtual_host, "r")
                modoescritura = open(virtual_host+'.mod', "w")
                buff = modolectura.read()
                char1='%nombre%'
                rbuff = buff.replace(char1, nombre)
                modoescritura.write(rbuff)
                modolectura.close()
                modoescritura.close()
#movemos plantilla a sites-available
                os.system("mv /home/vagrant/virtual_host.mod /etc/apache2/sites-available/www.%s"%ndominio)
#activamos el modulo y reiniciamos apache
                activar=os.system("a2ensite www.%s"%ndominio)
                reiniciar=os.system("service apache2 restart")

