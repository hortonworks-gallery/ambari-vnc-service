import sys, os, pwd, signal, time
from resource_management import *
from subprocess import call

class Master(Script):
  def install(self, env):
    # Install packages listed in metainfo.xml
    self.install_packages(env)
    self.configure(env)
    import params


    #params.log_location

    Execute('echo "installing Desktop" >> '+params.log_location)
    Execute('yum groupinstall -y Desktop >> '+params.log_location)
    Execute('mv /etc/sysconfig/vncservers /etc/sysconfig/vncservers.bak >> '+params.log_location)
    Execute('echo VNCSERVERS=\\"1:root\\" > /etc/sysconfig/vncservers')
    Execute('echo VNCSERVERARGS[1]=\\"-geometry '+params.vnc_geometry+'\\" >> /etc/sysconfig/vncservers')
    Execute('echo "'+params.vnc_password+'\n'+params.vnc_password+'\n\n" | vncpasswd')
    Execute('echo "Desktop install complete" >> '+params.log_location)
    
    if params.install_mvn:
        Execute('echo "Installing mvn..." >> '+params.log_location)      
        Execute('mkdir /usr/share/maven')
        Execute('wget '+params.mvn_location+' -O /usr/share/maven/maven.tar.gz  >> '+params.log_location)
        Execute('tar xvzf /usr/share/maven/maven.tar.gz -C /usr/share/maven  >> '+params.log_location)
        Execute('ln -s /usr/share/maven/apache-maven-*/ /usr/share/maven/latest')
        Execute("echo 'M2_HOME=/usr/share/maven/latest' >> ~/.bashrc")
        Execute("echo 'M2=$M2_HOME/bin' >> ~/.bashrc")
        Execute("echo 'PATH=$PATH:$M2' >> ~/.bashrc")
        Execute("echo maven install complete  >> "+params.log_location)         

    if params.install_eclipse:
        Execute('echo "Installing eclipse..." >> '+params.log_location)     
        Execute('wget ' +params.eclipse_location+' -O /usr/eclipse.tar.gz  >> '+params.log_location)
        Execute('tar -zxvf /usr/eclipse.tar.gz -C /usr/  >> '+params.log_location)
        Execute('echo  eclipse install complete  >> '+params.log_location)        

    if params.install_intellij:
        Execute('echo "Installing intelliJ..."  >> '+params.log_location)    
        Execute('wget '+params.intellij_location+' -O  /usr/ideaIC.tar.gz  >> '+params.log_location)
        Execute('tar -zxvf /usr/ideaIC.tar.gz -C /usr/  >> '+params.log_location)
        Execute('echo "intelliJ install complete"  >> '+params.log_location)    
        
    if params.install_spark:
        Execute('echo "Installing spark..."  >> '+params.log_location)
        Execute('wget '+params.spark_location+' -O  /usr/spark-1.2.tgz  >> '+params.log_location)
        Execute('tar xvfz /usr/spark-1.2.tgz -C /usr/  >> '+params.log_location)  
        Execute('mv `find /usr  -maxdepth 1 -type d -name "spark-*"` /usr/spark-1.2')          

        Execute('echo "export SPARK_HOME=/usr/spark-1.2"  >> ~/.bashrc')      
        Execute('echo "export YARN_CONF_DIR=/etc/hadoop/conf" >> ~/.bashrc')
        Execute('echo "spark.driver.extraJavaOptions -Dhdp.version=2.2.0.0-2041" > /usr/spark-1.2/conf/spark-defaults.conf')        
        Execute('echo "spark.yarn.am.extraJavaOptions -Dhdp.version=2.2.0.0-2041" >> /usr/spark-1.2/conf/spark-defaults.conf')        
        Execute('echo Spark install complete  >> '+params.log_location)        

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
        Execute('echo "/usr/idea-IC-*/bin/idea.sh" >> ~/Desktop/intellij.sh')
        Execute('chmod 755 ~/Desktop/intellij.sh')

  def status(self, env):
    Execute('/sbin/service   vncserver status')


if __name__ == "__main__":
  Master().execute()
