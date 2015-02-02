#!/bin/bash
# Author: Michael Ambrus (ambrmi09@gmail.com)
# 2015-02-02

if [ -z $ZNCLOG_CGI ]; then

ZNCLOG_CGI="znclog.cgi"


function znclog() {
	local FNAME=$1
}

source s3.ebasename.sh
if [ "$ZNCLOG_CGI" == $( ebasename $0 ) ]; then
	#Not sourced, do something with this.

	#Script root directory.
	ZNCLOG_DIR=$(dirname $(readlink -f $0))
	export PATH=${ZNCLOG_DIR}:$PATH

	ZNCLOG_CGI_INFO=${ZNCLOG_CGI}
	#source .cgi.ui..znclog.cgi
	source ${ZNCLOG_DIR}/ui/.znclog.cgi
	set -o pipefail

	znclog "${FNAME}" > "${DEF_TMP_NAME}_out" && \
		mv "${DEF_TMP_NAME}_out" ${1}

	exit $?
fi

fi
