#!/bin/sh
#set -x 

# rename to settings
. /root/spcp.smtp

ACCESS_LOG="/var/log/squid/access.log"
BLACKLIST="/root/keywords"
REPORT_MAIL="/tmp/report_mail"

pull() {
cat $1 | awk '/'"$2"'/{print $1" "$2" "$3" "$4" "$6 }'
}

report() {
	echo "Sending..."
	smtp-cli --missing-modules-ok -4 \
	--server=$SMTP_HOST \
	--port=$SMTP_PORT \
	--hello-host=$SMTP_HELLO \
	--user=$SMTP_USER \
	--pass=$SMTP_AUTH \
	--mail-from=$SMTP_FROM \
	--rcpt-to=$SMTP_TO \
	--charset=UTF-8 \
	--subject="$1" \
	--body-plain=$REPORT_MAIL
}

i=`cat $BLACKLIST | wc -l`
if [ -s $ACCESS_LOG ]; then
	while [ "$i" -gt "0" ]; do
			x=0
			export KEYWORD=`sed -n "$i"p  $BLACKLIST`
  			#pull $ACCESS_LOG $KEYWORD | uniq -f 4
  			for z in `pull $ACCESS_LOG $KEYWORD | uniq -f 4`
			do 
				echo Match
				if [ $x -ne "5" ]; then 
				export z"$x"="$z"
  				x=`expr $x + 1`
				fi
			
				cat <<- EOF > $REPORT_MAIL
				IP=$z0
				HOSTNAME=$z1
				MAC=$z2
				DATE=$z3
				STRING=$z4
				KEYWORD=$KEYWORD
				EOF
				report "Match: HOST: $z1 (IP: $z0) Keyword: $KEYWORD"
			done
  	i=`expr $i - 1`
	done
fi 
# Rotate the logs, needs cleanup for older logs, too.
if [ -s $REPORT_MAIL ]; then
	rm $REPORT_MAIL
	echo "Rotating logs"
	/usr/local/sbin/squid -k rotate

else
	echo "No match found"
fi
