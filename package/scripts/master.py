import sys, os, pwd, signal, time
from resource_management import *
from subprocess import call

class Master(Script):
  def install(self, env):
    # Install packages listed in metainfo.xml
    self.install_packages(env)
    self.configure(env)
    import params

    Execute('yum groupinstall -y Desktop')
    Execute('mv /etc/sysconfig/vncservers /etc/sysconfig/vncservers.bak')
    Execute('echo VNCSERVERS=\\"1:root\\" > /etc/sysconfig/vncservers')
    Execute('echo VNCSERVERARGS[1]=\\"-geometry '+params.vnc_geometry+'\\" >> /etc/sysconfig/vncservers')
    Execute('echo "'+params.vnc_password+'\n'+params.vnc_password+'\n\n" | vncpasswd')


    if params.install_eclipse:
        Execute('cd /usr')
        Execute('wget http://www.gtlib.gatech.edu/pub/eclipse/technology/epp/downloads/release/luna/SR1/eclipse-java-luna-SR1-linux-gtk-x86_64.tar.gz')
        Execute('tar -zxvf eclipse-java-luna-SR1-linux-gtk-x86_64.tar.gz -C /usr/')

    if params.install_intellij:
        Execute('cd /usr')
        Execute('wget http://download-cf.jetbrains.com/idea/ideaIC-14.0.2.tar.gz')
        Execute('tar -zxvf ideaIC-14.0.2.tar.gz -C /usr/')

  def configure(self, env):
    import params
    env.set_params(params)

  def stop(self, env):
    Execute('/sbin/service   vncserver stop')
      
  def start(self, env):
    import params
    Execute('/sbin/service   vncserver start')
    time.sleep(5)

    #create eclipse desktop link if doesn't exist
    if (params.install_eclipse and not os.path.exists('~/Desktop/eclipse')):
        #create Desktop dir if it does not exist
        if not os.path.exists('~/Desktop'):
            os.makedirs('~/Desktop')
        Execute('ln -s /usr/eclipse/eclipse ~/Desktop/eclipse')

    #create intellij desktop link if doesn't exist
    if (params.install_intellij and not os.path.exists('~/Desktop/intellij.sh')):
        #create Desktop dir if it does not exist
        if not os.path.exists('~/Desktop'):
            os.makedirs('~/Desktop')
        Execute('echo "export JAVA_HOME=/usr/jdk64/jdk1.7.0_67" > ~/Desktop/intellij.sh')
        Execute('echo "/usr/idea-IC-139.659.2/bin/idea.sh" >> ~/Desktop/intellij.sh')
        Execute('chmod 755 ~/Desktop/intellij.sh')

  def status(self, env):
    Execute('/sbin/service   vncserver status')


if __name__ == "__main__":
  Master().execute()
