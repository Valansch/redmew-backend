#! /bin/bash

url='https://discordapp.com/api/webhooks/376086949276155914/6J7kBDzbjFwVmpAFsnnzcoHKrVqErZGtTTfnTXO0XD8XF0-Ah_NrSzNIn8UGWK8KfWEk'
while inotifywait --quiet --quiet -e modify log/log.log; do
	msg=`tail -n1 log/log.log | cut -d' ' -f4- | sed 's/[^][ :a-zA-Z0-9]/x/g'`
	echo $msg
	curl --data-urlencode "content=$msg" $url
done
