#!/bin/sh

CONFIG_DIR=$HOME/.config/proxy

if [ ! -d $CONFIG_DIR ];then
mkdir -p $CONFIG_DIR
if [ ! -s $CONFIG_DIR/smtp.conf ]; then
echo "Missing SMTP configuration"
exit
fi
else
. $CONFIG_DIR/smtp.conf
fi

ACCESS_LOG=${1:-"/var/log/squid/access.log"}
BLACKLIST="$CONFIG_DIR/blacklist"
REPORT_MAIL="/tmp/report_mail"

pull() {
	cat $ACCESS_LOG | awk '/'"$1"'/{print $1" "$2" "$3" "$4" "$6 }' \
	| uniq -f 4
}

hits() {
	awk '/'"$1"'/{print $1" "$2" "$3" "$4" "$6 }' $ACCESS_LOG \
	| uniq -f 4 | wc -l
}

report() {
		#smtp-cli --missing-modules-ok -4 \
		smtp-cli --print-only --missing-modules-ok -4 \
		--server=$SMTP_HOST \
		--port=$SMTP_PORT \
		--hello-host=$SMTP_HELLO \
		--user=$SMTP_USER \
		--pass=$SMTP_AUTH \
		--mail-from=$SMTP_FROM \
		--rcpt-to=$SMTP_TO \
		--charset=UTF-8 \
		--subject="$1" \
		--body-plain=$REPORT_MAIL >/dev/null
}

if [ -s $BLACKLIST ]; then
s=`cat $BLACKLIST |  wc -l`
else
echo "Blacklist empty"
exit
fi

if [ -s $ACCESS_LOG ]; then
	while [ "$s" -gt "0" ]; 
	do
		export KEYWORD=`sed -n "$s"p  $BLACKLIST`
		s=`expr $s - 1`
		IFS=$'\n'
		echo "$KEYWORD `hits $KEYWORD` hits"
		for k in `pull $KEYWORD`
			do
			IFS=$' \t
'
			cat <<- EOF > $REPORT_MAIL
			IP=`echo $k | cut -f 1 -d" "`
			HOSTNAME=`echo $k | cut -f 2 -d" "`
			MAC=`echo $k | cut -f 3 -d" "`
			DATE=`echo $k | cut -f 4 -d" "`
			URL=`echo $k | cut -f 5 -d" "`
			EOF
			IP=`echo $k | cut -f 1 -d" "`
			HOSTNAME=`echo $k | cut -f 2 -d" "`

                       report "Match: $HOSTNAME (IP: $IP) Keyword: $KEYWORD"

		done
	done

else
	echo "No Accesslog found"
	exit
fi

if [ -s $REPORT_MAIL ]; then
rm $REPORT_MAIL
echo "Rotating logs"
/usr/local/sbin/squid -k rotate

else
echo "No match found"
fi

