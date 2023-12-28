#!/bin/sh
echo "Copying files ..."
cp /usr/local/opnsense/service/templates/OPNsense/Proxy/squid.conf /var/backups/proxy-squid.conf.`date +%s`
cp actions_parental-monitor.conf /usr/local/opnsense/service/conf/actions.d/
cp parental-monitor.py /usr/local/bin/parental-monitor.py
cp 90-parental-monitor  /usr/local/etc/rc.syshook.d/start/

echo "Patching files ..."
patch /usr/local/opnsense/service/templates/OPNsense/Proxy/squid.conf < squid.conf.patch
configctl template reload OPNsense/Proxy

echo "Configuration changed. Restarting local service: configd"
service configd restart
echo "Done"
echo 'To start the "Parental Monitor" now, type "configctl parental-monitor start"'
