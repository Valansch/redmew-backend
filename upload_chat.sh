#! /bin/bash

url='https://discordapp.com/api/webhooks/376086949276155914/6J7kBDzbjFwVmpAFsnnzcoHKrVqErZGtTTfnTXO0XD8XF0-Ah_NrSzNIn8UGWK8KfWEk'
while inotifywait --quiet --quiet -e modify log/log.log; do
	tail -n1 log/log.log | cut -d' ' -f4- | curl --data-urlencode content@- $url
done
