import os
import MySQLdb
import sys
import string
from random import choice
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
                ac = modolectura.read()
                char1='%nombre%'
                acf = ac.replace(char1, nombre)
                modoescritura.write(acf)
                modolectura.close()
		modoescritura.close()
#movemos plantilla a sites-available
                os.system("mv /home/debian/virtual_host.mod /etc/apache2/sites-available/www.%s.conf"%ndominio)    
#activamos el modulo y reiniciamos apache
                activar=os.system("a2ensite www.%s"%ndominio)
                reiniciar=os.system("service apache2 restart")
#insertamos el usuario en mysql
                consultauid="select max(uid) from usuarios;"
                cursor.execute(consultauid)
                consulta_uid = cursor.fetchone()
#generamos una contrasenna aleatoria
                def GenPasswd(n):
                         return ''.join([choice(string.letters + string.digits) for i in range(n)])
                clave=GenPasswd(8)
                print"esta es tu contrasenna para el usuario %s ftp:"%nombre, clave

#si la tabla esta vacia introduce el 7001
                if consulta_uid[0] == None:
                        conuid=str("7001")
                        usermysql="insert into usuarios values('"+ nombre+"'," +"PASSWORD('"+clave+"'),"+conuid+","+conuid+","+"'/var/www/"+nombre+"',"+"'/bin/false1',"+"1,'"+ndominio+"');"
			cursor.execute(usermysql)
                        base.commit()
#cambiamos el propietario de la carpeta /var/www
                        os.system("chown -R "+conuid+":"+conuid+" "+"/var/www/%s" %nombre)
#en caso contrario le suma uno al numero maximo de la tabla
                else:
                        conuid=consulta_uid[0]+1
                        conuidn=str(conuid)
                        usermysql="insert into usuarios values('"+ nombre+"'," +"PASSWORD('"+clave+"'),"+conuidn+","+conuidn+","+"'/var/www/"+nombre+"',"+"'/bin/false1',"+"1,'"+ndominio+"');"
			cursor.execute(usermysql)
                        base.commit()
#cambiamos el propietario de la carpeta /srv/www
			os.system("chown -R "+conuidn+":"+conuidn+" "+"/var/www/%s" %nombre)
#creamos la nueva zona
		fichzona="/home/vagrant/zona"
                zonadominio=open(fichzona,"r")
                wzonadominio = open(fichzona+'.mod', "w")
                zonaac = zonadominio.read()
                var='%ndominio%'
                cambio = zonaac.replace(var, ndominio)
                wzonadominio.write(cambio)
                zonadominio.close()
                wzonadominio.close()
#abrimos el fichero modificado y modificamos el named.conf.local
                ficheromodificado=open("/home/vagrant/zona.mod","r")
                ficheromodificado1=ficheromodificado.read()
                p=open("/etc/bind/named.conf.local","a")
                p.write(ficheromodificado1)
                p.close()
                os.system("rm -r /home/vagrant/zona.mod")
#creamos el nuevo fichero de dominio
		ficherodominio="/home/vagrant/db.plantilla"
                dominio=open(ficherodominio, "r")
                filew = open(ficherodominio+'.mod', "w")
                ac = dominio.read()
                variable1='%ndominio%'
                acf = ac.replace(variable1, ndominio)
                filew.write(acf)
                dominio.close()
                filew.close()
#cambiamos de lugar y nombre
                 os.system("mv /home/debian/db.plantilla.mod /var/cache/bind/db.%s"%ndominio)
#reiniciamos bind
                reiniciar=os.system("service bind9 restart")
		print "usuario creado correctamente"
