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

    if params.install_mvn:
        Execute('mkdir /usr/share/maven')
        Execute('cd /usr/share/maven')
        Execute('wget --directory-prefix=/usr/share/maven http://mirrors.koehn.com/apache/maven/maven-3/3.2.5/binaries/apache-maven-3.2.5-bin.tar.gz')
        Execute('tar xvzf /usr/share/maven/apache-maven-3.2.5-bin.tar.gz -C /usr/share/maven')
        Execute('ln -s /usr/share/maven/apache-maven-3.2.5/ /usr/share/maven/latest')
        Execute('echo "M2_HOME=/usr/share/maven/latest" >> ~/.bashrc')
        Execute('echo "M2=$M2_HOME/bin" >> ~/.bashrc')
        Execute('echo "PATH=$PATH:$M2" >> ~/.bashrc')
        Execute('export M2_HOME=/usr/share/maven/latest')
        Execute('export M2=$M2_HOME/bin')
        Execute('export PATH=$PATH:$M2')


    if params.install_eclipse:
        Execute('cd /usr')
        Execute('wget http://ftp.osuosl.org/pub/eclipse//technology/epp/downloads/release/luna/SR1a/eclipse-java-luna-SR1a-linux-gtk-x86_64.tar.gz')
        Execute('tar -zxvf eclipse*.tar.gz -C /usr/')

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
    desktop = '/root/Desktop'
    #create eclipse desktop link if doesn't exist
    if (params.install_eclipse and not os.path.exists(desktop + '/eclipse')):
        #create Desktop dir if it does not exist
        if not os.path.exists(desktop):
            os.makedirs(desktop)
        Execute('ln -s /usr/eclipse/eclipse ~/Desktop/eclipse')

    #create intellij desktop link if doesn't exist
    if (params.install_intellij and not os.path.exists(desktop + '/intellij.sh')):
        #create Desktop dir if it does not exist
        if not os.path.exists(desktop):
            os.makedirs(desktop)
        Execute('echo "export JAVA_HOME=/usr/jdk64/jdk1.7.0_67" > ~/Desktop/intellij.sh')
        Execute('echo "/usr/idea-IC-139.659.2/bin/idea.sh" >> ~/Desktop/intellij.sh')
        Execute('chmod 755 ~/Desktop/intellij.sh')

  def status(self, env):
    Execute('/sbin/service   vncserver status')


if __name__ == "__main__":
  Master().execute()
