#!/bin/bash
# Author: Michael Ambrus (ambrmi09@gmail.com)
# 2017-04-21

if [ -z $PANDOC2HTML_CGI ]; then

PANDOC2HTML_CGI="pandoc2html.cgi"


function pandoc2html() {
	local FNAME=$1
}

source s3.ebasename.sh
if [ "$PANDOC2HTML_CGI" == $( ebasename $0 ) ]; then
	#Not sourced, do something with this.

	#Script root directory.
	PANDOC2HTML_DIR=$(dirname $(readlink -f $0))
	export PATH=${PANDOC2HTML_DIR}:$PATH

	PANDOC2HTML_CGI_INFO=${PANDOC2HTML_CGI}
	#source .cgi.ui..pandoc2html.cgi
	source ${PANDOC2HTML_DIR}/ui/.pandoc2html.cgi
	set -o pipefail

	pandoc2html "${FNAME}" > "${DEF_TMP_NAME}_out" && \
		mv "${DEF_TMP_NAME}_out" ${1}

	exit $?
fi

fi
