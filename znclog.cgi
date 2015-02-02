#!/bin/bash
# Author: Michael Ambrus (ambrmi09@gmail.com)
# 2015-02-02

if [ -z $ZNCLOG_CGI ]; then

ZNCLOG_CGI="znclog.cgi"

function znclog() {
	if [ $DAYS_BACK == "infinite" ]; then
		local TAIL1="cat --"
	else
		local TAIL1="tail -n${DAYS_BACK}"
	fi

	for F in $(ls "${ZNC_LOG_DIRECTORY}" | grep -E '#bladerf.*\.log' | $TAIL1 ); do
		echo '===================================='
		CH_NAME=$(echo  $F | cut -f1 -d"_")
		LOG_DATE=$(echo $F | cut -f2 -d"_" | sed -E 's/\.log$//')
		echo "${CH_NAME} ${LOG_DATE}"
		echo '===================================='
		if [ $HIDE_STATUS == 'yes' ]; then
			cat "${ZNC_LOG_DIRECTORY}/${F}" | \
				grep -Ev '^\[.*\] \*\*\* .*:'
		else
			cat "${ZNC_LOG_DIRECTORY}/${F}"
		fi
	done
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

	znclog 

	exit $?
fi

fi
