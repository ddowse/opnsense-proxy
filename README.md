## Smart parental control proxy

This is the repo for the private UpWork Project "Smart parental control proxy".  

To create and install your own CA (Certificate Authority) with OPNsense follow  
the instructions from the offical OPNsense Documentation.  

https://docs.opnsense.org/manual/how-tos/proxytransparent.html#step-4-ca-for-transparent-ssl

Download the CA Certificate and distribute it to your devices. In most cases a "double click"  
on the File will trigger a import dialog from your OS. 



Apply the patch by cloning this repo and cd into it. Then run

```
./patch.sh
configctl proxy restart
```

## Files

``` /var/log/monitor.log ```
``` /usr/local/etc/squid/acl/monitor ```

