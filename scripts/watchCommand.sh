FILE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )/../script-output/commandPipe";

tail -n0 -f $FILE
