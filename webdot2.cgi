#!/bin/bash
# Author: Michael Ambrus (ambrmi09@gmail.com)
# 2017-04-21

# The tricky part in this script is handling the arguments...

if [ -z $WEBDOT2_CGI ]; then

WEBDOT2_CGI="webdot2.cgi"


function webdot2() {
	local FNAME=$1

	ENGINE=$(tr '[:upper:]' '[:lower:]' <<< ${ENGINE})
	FORMAT=$(tr '[:upper:]' '[:lower:]' <<< ${FORMAT})

	unset QUERY_STRING
	unset PATH_INFO

	echo "$EXEC_PATH/webdot.cgi ${URI}.${ENGINE}.${FORMAT}" >> \
		"$WEBDOT2_LOGFILE"
	$EXEC_PATH/webdot.cgi "${URI}.${ENGINE}.${FORMAT}"
}


# ATTENTION: FUNDAMENTAL SETTINGS FOLLOW
# THESE MAKE ASSUMPTIONS. PLEASE CHECK!

HOME=${HOME-"$(dirname $(dirname $(echo $PWD)))"}
USER=${USER-"$(basename $(echo $HOME))"}
PATH=${PATH-"${HOME}/bin:$PATH"}

#Script root directory.
WEBDOT2_DIR=$(dirname $(readlink -f $0))
export PATH=${WEBDOT2_DIR}:$PATH

WEBDOT2_CGI_INFO=${WEBDOT2_CGI}
source ${WEBDOT2_DIR}/funcs/html.sh
source ${WEBDOT2_DIR}/ui/.webdot2_webhelp.cgi
source ${WEBDOT2_DIR}/ui/.webdot2.cgi
set -o pipefail


if [ "X${WEBHELP}" == "Xyes" ]; then
	page_header "web log: Help"
	print_webhelp  | \
		cnvrt_urls2links | \
		cnvrt_eol
	page_footer
else
	if [ "X${WEBMODE2}" == "Xraw" ]; then
		echo "Content-type: text/html"
		echo ""
		webdot2
	else
		webdot2
	fi
fi

exit 0

fi
