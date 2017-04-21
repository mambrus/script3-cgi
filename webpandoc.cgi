#!/bin/bash
# Author: Michael Ambrus (ambrmi09@gmail.com)
# 2017-04-21

# The tricky part in this script is handling the arguments...

if [ -z $WEBPANDOC_CGI ]; then

WEBPANDOC_CGI="webpandoc.cgi"


function webpandoc() {
	local FNAME=$1

	OIFORMAT=$(tr '[:upper:]' '[:lower:]' <<< ${OIFORMAT})
	IFORMAT=$(tr '[:upper:]' '[:lower:]' <<< ${IFORMAT})
	
	if [ $STANDALONE == "yes" ]; then
		SFLAG='-s'
	fi

	unset QUERY_STRING
	unset PATH_INFO

#	echo "wget -O - ${URI} | $EXEC_PATH/pandoc ${SFLAG} -f ${IFORMAT} -t ${OFORMAT} -o-" >> \
#		"$WEBPANDOC_LOGFILE"

	echo "Content-type: text/html"
	echo ""
	wget -O - ${URI} | $EXEC_PATH/pandoc ${SFLAG} -f ${IFORMAT} -t ${OFORMAT} -o-
}


# ATTENTION: FUNDAMENTAL SETTINGS FOLLOW
# THESE MAKE ASSUMPTIONS. PLEASE CHECK!

HOME=${HOME-"$(dirname $(dirname $(echo $PWD)))"}
USER=${USER-"$(basename $(echo $HOME))"}
PATH=${PATH-"${HOME}/bin:$PATH"}

#Script root directory.
WEBPANDOC_DIR=$(dirname $(readlink -f $0))
export PATH=${WEBPANDOC_DIR}:$PATH

WEBPANDOC_CGI_INFO=${WEBPANDOC_CGI}
source ${WEBPANDOC_DIR}/funcs/html.sh
source ${WEBPANDOC_DIR}/ui/.webpandoc_webhelp.cgi
source ${WEBPANDOC_DIR}/ui/.webpandoc.cgi
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
		webpandoc
	else
		webpandoc
	fi
fi

exit 0

fi

