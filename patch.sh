#!/bin/sh
cp /usr/local/opnsense/service/templates/OPNsense/Proxy/squid.conf /var/backups/proxy-squid.conf.`date +%s`
patch /usr/local/opnsense/service/templates/OPNsense/Proxy/squid.conf < squid.conf.patch
configctl template reload OPNsense/Proxy
