#!/bin/bash
# Author: Michael Ambrus (ambrmi09@gmail.com)
# 2015-02-02

if [ -z $ZNCLOG_CGI ]; then

ZNCLOG_CGI="znclog.cgi"

function znclog() {
	local RC=1
	if [ $DAYS_BACK == "infinite" ]; then
		local TAIL1="cat --"
	else
		local TAIL1="tail -n${DAYS_BACK}"
	fi
	if [ $REVERSE == "yes" ]; then
		local REV=tac
	else
		local REV="cat --"
	fi

	local NR_LOGS=$(
		ls "${ZNC_LOG_DIRECTORY}" 2>/dev/null | \
		grep -E "#${CHANNEL}_.*\.log" | \
		wc -l
	)
	if [ "x${NR_LOGS}" == "x0" ]; then
		echo -n '=========1=========2=========3=========4'
		echo    '=========5=========6=========7=========8'
		echo    "No logs found for channel [#${CHANNEL}]"
		echo -n '=========1=========2=========3=========4'
		echo    '=========5=========6=========7=========8'
	fi

	for F in $(ls "${ZNC_LOG_DIRECTORY}" | grep -E "#${CHANNEL}_.*\.log" | $TAIL1 | $REV); do
		(
			echo -n '=========1=========2=========3=========4'
			echo    '=========5=========6=========7=========8'
			CH_NAME=$(echo  $F | cut -f1 -d"_")
			LOG_DATE=$(echo $F | cut -f2 -d"_" | sed -E 's/\.log$//')
			echo "${CH_NAME} ${LOG_DATE}"
			echo -n '=========1=========2=========3=========4'
			echo    '=========5=========6=========7=========8'

			if [ $HIDE_STATUS == 'yes' ]; then
				cat "${ZNC_LOG_DIRECTORY}/${F}" | \
					grep -Ev '^\[.*\] \*\*\* .*:'
			else
				cat "${ZNC_LOG_DIRECTORY}/${F}"
			fi
		) | $REV
		local RC=0
	done
	return $RC
}

if [ "${WEBMODE}" == "yes" ]; then
	export USER=mambrus
	export HOME=/home/$USER
	export PATH=${HOME}/bin:$PATH
fi

source s3.ebasename.sh
if [ "$ZNCLOG_CGI" == $( ebasename $0 ) ]; then
	#Not sourced, do something with this.

	#Script root directory.
	ZNCLOG_DIR=$(dirname $(readlink -f $0))
	export PATH=${ZNCLOG_DIR}/../s3:$PATH

	ZNCLOG_CGI_INFO=${ZNCLOG_CGI}
	#source .cgi.ui..znclog.cgi
	source ${ZNCLOG_DIR}/ui/.znclog.cgi
	source ${ZNCLOG_DIR}/funcs/html.sh
	set -o pipefail

	page_header "ZNC log @ ${SERVER_SIGNATURE}"

	znclog | \
		cnvrt_urls2links | \
		cnvrt_special_chars

	page_footer

	exit 0
fi

fi
