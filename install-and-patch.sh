#!/bin/sh
echo "Install files and patching..."
cp /usr/local/opnsense/service/templates/OPNsense/Proxy/squid.conf /var/backups/proxy-squid.conf.`date +%s`
cp actions_parental-monitor.conf /usr/local/opnsense/service/conf/actions.d/
cp parental-monitor.py /usr/local/bin/parental-monitor.py

patch /usr/local/opnsense/service/templates/OPNsense/Proxy/squid.conf < squid.conf.patch

configctl template reload OPNsense/Proxy
