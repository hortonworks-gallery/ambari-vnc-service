import sys, os, pwd, signal, time, glob
from resource_management import *
from subprocess import call

class Master(Script):

  def get_homedir(self, user):
    result = self.read_passwdfile()
    for data in result:
      (username, encrypwd, uid, gid, gecos, homedir, usershell) = data.split(':')
      if user == username:
        return homedir

  def read_passwdfile(self):
    passwdfile = open('/etc/passwd', 'r')
    data = []
    for i in passwdfile.readlines():
      data.append(i[:-1]) #remove trailing '\n'
    passwdfile.close()
    return data 
    
  def install(self, env):
    # Install packages listed in metainfo.xml
    self.install_packages(env)

    import params


    Execute('echo "installing Desktop" >> '+params.log_location)
    Execute('yum groupinstall -y Desktop >> '+params.log_location)
    Execute('mv /etc/sysconfig/vncservers /etc/sysconfig/vncservers.bak >> '+params.log_location, ignore_failures=True)

    self.configure(env)
    Execute('echo "Desktop install complete" >> '+params.log_location)
    
    if params.install_mvn:
        Execute('echo "Installing mvn..." >> '+params.log_location)      
        Execute('curl -o /etc/yum.repos.d/epel-apache-maven.repo https://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo')
        Execute('yum -y install apache-maven >> '+params.log_location)      
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

    #write out contents
    content=InlineTemplate(params.template_config)    
    File(format("/etc/sysconfig/vncservers"), content=content, owner='root',group='root', mode=0644)
    
    #set vnc password
    Execute('echo "'+str(params.vnc_password)+'\n'+str(params.vnc_password)+'\n\n" | vncpasswd')
    

  def stop(self, env):
    self.configure(env) 
    Execute('service vncserver stop')
    Execute('rm -f /var/lock/subsys/Xvnc', ignore_failures=True)      
    Execute('rm -f /tmp/.X*', ignore_failures=True)      
    
      
  def start(self, env):
    import params
    self.configure(env)
    
    Execute('rm -rf /var/lock/subsys/Xvnc', ignore_failures=True)
    Execute('rm -rf /tmp/.X*', ignore_failures=True)      
    
    home_dir = self.get_homedir(params.vnc_user)
    Execute('echo home_dir: ' + str(home_dir))
    
    pid_file = glob.glob(home_dir + '/.vnc/*.pid')[0]
    Execute('echo pid_file: ' + pid_file)
        
    Execute('service vncserver start')
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
        Execute('echo "export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk.x86_64" > ~/Desktop/intellij.sh')
        Execute('echo "/usr/idea-IC-*/bin/idea.sh" >> ~/Desktop/intellij.sh')
        Execute('chmod 755 ~/Desktop/intellij.sh')

   
				
  def status(self, env):
    import params
    home_dir = get_homedir(params.vnc_user)
    pid_file = glob.glob(home_dir + '/.vnc/*.pid')[0]
    check_process_status(pid_file)     
    #Execute('service vncserver status')


    

if __name__ == "__main__":
  Master().execute()
