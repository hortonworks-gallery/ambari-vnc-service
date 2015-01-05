import sys, os, pwd, signal
from resource_management import *
from subprocess import call

class Master(Script):
  def install(self, env):
    # Install packages listed in metainfo.xml
    self.install_packages(env)
    self.configure(env)
    import params

    Execute('yum install -y tigervnc-server firefox')
    Execute('yum groupinstall -y Desktop')
    Execute('mv /etc/sysconfig/vncservers /etc/sysconfig/vncservers.bak')
    Execute('echo VNCSERVERS=\\"1:root\\" > /etc/sysconfig/vncservers')
    Execute('echo VNCSERVERARGS[1]=\\"-geometry '+params.vnc_geometry+'\\" >> /etc/sysconfig/vncservers')
    Execute('echo "'+params.vnc_password+'\n'+params.vnc_password+'\n\n" | vncpasswd')


    if params.install_eclipse:
        Execute('cd /usr')
        Execute('wget http://www.gtlib.gatech.edu/pub/eclipse/technology/epp/downloads/release/luna/SR1/eclipse-java-luna-SR1-linux-gtk-x86_64.tar.gz')
        Execute('tar -zxvf eclipse-java-luna-SR1-linux-gtk-x86_64.tar.gz -C /usr/')
        Execute('ln -s /usr/eclipse/eclipse /usr/bin/eclipse')
	#Execute('ln -s /usr/eclipse/eclipse ~/Desktop/eclipse')

  def configure(self, env):
    import params
    env.set_params(params)

  def stop(self, env):
    Execute('/sbin/service   vncserver stop')
      
  def start(self, env):
    Execute('/sbin/service   vncserver start')

  def status(self, env):
    Execute('/sbin/service   vncserver status')


if __name__ == "__main__":
  Master().execute()
