#Project3

i. The IP address and SSH port
IP:	18.195.120.209
Port: 2200

ssh -i .ssh/grader_key grader@18.195.120.209 -p 2200

ii. The complete URL to your hosted web application.

http://tkazatelgames.tk/
if above is not working
http://18.195.120.209/


iii. A summary of software you installed and configuration changes made.

***LOCAL PC----------
echo "18.195.120.209 uda" >> /etc/hosts
chmod 400 ~/.ssh/LightsailDefaultKey-eu-central-1.pem
ssh -i ~/.ssh/LightsailDefaultKey-eu-central-1.pem ubuntu@uda
***------------------


*******************************************
#User Management 1 - Can you log into the server as the user grader using the submitted key?
*******************************************
sudo adduser grader			#passwd no matter

sudo ls /etc/sudoers.d/
	90-cloud-init-users  README
	
	
	***********************************
	#User Management 3 - Is the grader user given sudo access?
	***********************************
    sudo cp /etc/sudoers.d/90-cloud-init-users /etc/sudoers.d/grader
    
    sudo vi /etc/sudoers.d/grader
    	:%s/ubuntu/grader/

    sudo cat /etc/sudoers.d/grader

su - grader

sudo ls /etc/sudoers.d/		#test sudo permission


ssh-keygen			# passwd was not specified, I used "grader"

ls -l .ssh/

mv .ssh/id_rsa.pub .ssh/authorized_keys

chmod 700 .ssh
chmod 644 .ssh/authorized_keys

cat .ssh/id_rsa
	#copy and follow on bellow

***LOCAL PC----------

vi ~/.ssh/grader_key
chmod 400 ~/.ssh/grader_key
ssh -i ~/.ssh/grader_key grader@uda
***------------------

*******************************************
#User Management 2 - Is remote login of the root user disabled?
*******************************************
sudo vi /etc/ssh/sshd_config 
	#PermitRootLogin prohibit-password
	PermitRootLogin no


*******************************************
#Security 3 - Are the applications up-to-date?
*******************************************
sudo apt-get update
sudo apt-get upgrade


*******************************************
#Security 2 - Are users required to authenticate using RSA keys?  #have been set by default
*******************************************
sudo vi /etc/shh/sshd_config
	PasswordAuthentication no
	
	
*******************************************	
#Security 2 - Is SSH hosted on non-default port?
*******************************************	

***LOCAL PC BROWSER----------

https://lightsail.aws.amazon.com/ls/webapp/eu-central-1/instances/<your_instance>/networking
*add new port to lightsail firewall =>  
	Application = Custom, Protocol = TCP, Port = 2200
	Application = Custom, Protocol = TCP, Port = 123
***------------------

sudo vi /etc/ssh/sshd_config
	#Port 22
	Port 2200

sudo service ssh restart

***LOCAL PC----------
ssh -i .ssh/grader_key grader@uda
ssh: connect to host uda port 22: Connection refused

ssh -i .ssh/grader_key grader@uda -p 2200 
***------------------


*******************************************	
#Security 1 - Is the firewall configured to only allow for SSH, HTTP, and NTP?
*******************************************	

sudo ufw status
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2200/tcp
sudo ufw allow 80/tcp
sudo ufw allow 123/tcp
sudo ufw enable 
sudo ufw status

*******************************************	
#Application Functionality 1 - Is there a web server running on port 80?
*******************************************	

sudo apt-get install apache2

/etc/apache2/apache2.conf
sudo vi /etc/apache2/ports.conf   # pot 80 already in use



*******************************************	
#Application Functionality 2 - Has the database server been configured to properly serve data?
*******************************************	

sudo apt-get install postgresql postgresql-contrib libpq-dev

sudo vi /etc/postgresql/9.5/main/pg_hba.conf		#only local is allowed by default
	local   all             postgres                                peer
	local   all             all                                     peer
	host    all             all             127.0.0.1/32            md5
	host    all             all             ::1/128                 md5

sudo service postgresql start
 
sudo -u postgres -i
psql
CREATE USER catalog WITH PASSWORD grader;
ALTER USER catalog CREATEDB;
CREATE DATABASE catalog WITH OWNER catalog;
Connect to database $ 
\c catalog
REVOKE ALL ON SCHEMA public FROM public;
GRANT ALL ON SCHEMA public TO catalog;


*******************************************	
#Application Functionality 3 - Has the web server been configured to serve the Item Catalog application?
*******************************************	

sudo apt-get install libapache2-mod-wsgi python-dev

sudo a2enmod wsgi


sudo /etc/init.d/apache2 start
sudo /etc/init.d/apache2 stop



sudo apt-get install python-pip
sudo pip install virtualenv
sudo virtualenv venv
source venv/bin/activate
sudo chmod -R 777 venv

pip install flask
pip install httplib2
pip install requests
pip install sqlalchemy
pip install oauth2client
pip install psycopg2



mkdir /var/www/catalog
sudo chown grader:grader /var/www/catalog
cd /var/www/catalog
git clone https://github.com/Kazatel/catalog.git


sudo vi /var/www/catalog/catalog.wsgi
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/catalog/")

from catalog import app as application
application.secret_key = 'kazatel1'

sudo vi /etc/apache2/sites-enabled/catalog.conf

<VirtualHost *:80>
    ServerName 18.198.120.209
    ServerAlias ec2-13-232-240-16.ap-south-1.compute.amazonaws.com
    ServerAdmin grader@18.198.120.209
    WSGIDaemonProcess catalog python-path=/var/www/catalog:/var/www/catalog/venv/lib/python2.7/site-packages
    WSGIProcessGroup catalog
    WSGIScriptAlias / /var/www/catalog/catalog.wsgi
    <Directory /var/www/catalog/catalog/>
        Order allow,deny
        Allow from all
    </Directory>
    Alias /static /var/www/catalog/catalog/static
    <Directory /var/www/catalog/catalog/static/>
        Order allow,deny
        Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

cd /var/www/catalog/catalog
python database_setup.py
python lotsofmenus.py

sudo /etc/init.d/apache2 restart

iv. A list of any third-party resources you made use of to complete this project. 

https://www.codementor.io/abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft
https://modwsgi.readthedocs.io/en/develop/user-guides/virtual-environments.html
https://www.postgresql.org/docs/8.0/sql-createuser.html
http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/
