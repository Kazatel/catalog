#Project2

Project2 is html project builded based on Flask.
Users can log in via google or facebook and can add new games. 
Edit and delete only own games.


#Installation

Before we start , download required applications and files.

Requirements
  * Vagrant - tool for building and managing virtual machine environments
    (https://www.vagrantup.com/)
  * VirtualBox - is a cross-platform virtualization software.
    (https://www.virtualbox.org/)
  * Udacity vagrant file - preconfigured configuration file for vagrant installation
    (https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile)


Install Vagrant
  double click on downloaded vagrant file and follow GUI in order
  to select installation folder and complete the installation.

Install VirtualBox
  double click on downloaded virtual box file and follow GUI in order
  to select installation folder and complete the installation.

Create new folder called project1 and copy vagrant file into it.

  mkdir Project2
  cd Project2
  ls   # to check if vargrant file is inside the folder

Install virtual server
  enter Project2 folder, make sure that vagrant file is presented.
  Use the command "vagrant up" to install and setup virtual machine

  vagrant up

  Some usefull vagrant commands
    to check your virtual machines
      vagrant global-status

    to access virtual machine
      vagrant ssh <id>
      vagrant ssh 20c6a19

    to shutdown vagrant machine
      vagrant halt <id>
      vagrant halt 20c6a19

Install project2
  from your computer
  unzip "project2_tm480h_att.zip" and all files into /Project2/vagrant/catalog folder


Setup database
  from virtual machine run commands
  python database_setup.py   # to create games.db file
  python lotsofmenus.py 	 # to load genre table and some db items



#USAGE

  from virtual machines enter the /vagrant/catalog folder and use command

  python project2.py
 
  open page http://localhost:8000/ in your favorite browser
 
  you may do
	use login button to log in via google or facebook.
    add new game by clickin on add game button.
    eddit and delete only games you have been added.
    browse games added by other
	
  home page show last 5 recently added games
  
  as a last you may view JSON output 
  http://localhost:8000//game/<int:game_id>/JSON
  http://localhost:8000//genre/<int:genre_id>/JSON
