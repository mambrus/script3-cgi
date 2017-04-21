#!/bin/bash
# Author: Michael Ambrus (ambrmi09@gmail.com)
# 2017-04-21

if [ -z $WEBDOT2_CGI ]; then

WEBDOT2_CGI="webdot2.cgi"


function webdot2() {
	local FNAME=$1
}

source s3.ebasename.sh
if [ "$WEBDOT2_CGI" == $( ebasename $0 ) ]; then
	#Not sourced, do something with this.

	#Script root directory.
	WEBDOT2_DIR=$(dirname $(readlink -f $0))
	export PATH=${WEBDOT2_DIR}:$PATH

	WEBDOT2_CGI_INFO=${WEBDOT2_CGI}
	#source .cgi.ui..webdot2.cgi
	source ${WEBDOT2_DIR}/ui/.webdot2.cgi
	set -o pipefail

	webdot2 "${FNAME}" > "${DEF_TMP_NAME}_out" && \
		mv "${DEF_TMP_NAME}_out" ${1}

	exit $?
fi

fi
