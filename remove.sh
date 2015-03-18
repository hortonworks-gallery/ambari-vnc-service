rm -rf /var/lib/ambari-server/resources/stacks/HDP/2.2/services/VNC
rm -rf /usr/eclipse*
rm -rf /usr/idea*
rm -rf /usr/spark-1.2*
rm -f ~/Desktop/eclipse
rm -f ~/Desktop/intellij.sh
service ambari-server restart
service ambari-agent restart

