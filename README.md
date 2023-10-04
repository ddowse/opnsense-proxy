##Smart parental control proxy

This is the repo for the private UpWork Project "Smart parental control proxy".  

To create and install your own CA (Certificate Authority) with OPNsense follow  
the instructions from the offical OPNsense Documentation.  

https://docs.opnsense.org/manual/how-tos/proxytransparent.html#step-4-ca-for-transparent-ssl

Download the CA Certificate and distribute it to your devices. In most cases a "double click"  
on the File will trigger a import dialog from your OS. 



Apply the patch by cloning this repo then run


```
cp patch-squid.conf /usr/local/opnsense/service/templates/OPNsense/Proxy/
cd cd /usr/local/opnsense/service/templates/OPNsense/Proxy
patch < patch-squid.conf
configctl template reload OPNsense/Sample
configctl proxy restart
```

#Squid Logformat

Example:

```
192.168.1.123 mypc.localdomain 00:00:00:00:00:00  01/Oct/2023:15:20:21  200 "https://www.bing.com/search?q=KEYWORD&qs=n&form=QBRE&sp=-1&lq=0&pq=keyword&sc=13-9&sk=&cvid=1C63DC3F2BE644429026D07CDF2EC8B4&ghsh=0&ghacc=0&ghpl="
```

