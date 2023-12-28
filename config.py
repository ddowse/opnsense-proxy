# Intervall to send a report in seconds
intervall = 600 # Seconds 
# Path to the file with the keywords
acl_file = "/usr/local/etc/squid/acl/monitor"
# Path to the file to store a global log ( needs logrotate )
monitor_log = "/var/log/monitor.log"
# Path to the file with the loglines of squid
squid_log = "/var/log/squid/access.log"

# Mailserver - StartSSL
# Check with your Hosting or Internetprovider for details
smtp_server = "smtpserver"
port = "587" 
sender = "from@example.org"
recipient = "to@example.org"
password = "Password"

