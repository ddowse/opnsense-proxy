#!/bin/sh
cp /usr/local/opnsense/service/templates/OPNsense/Proxy/squid.conf /root/proxy-squid.conf.`date +%s`-BACKUP
patch /usr/local/opnsense/service/templates/OPNsense/Proxy/squid.conf < squid.conf.patch
configctl template reload OPNsense/Proxy
