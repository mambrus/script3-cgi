#!/bin/bash
# Author: Michael Ambrus (ambrmi09@gmail.com)
# 2015-02-02

if [ -z $TEMPLATE_CGI ]; then

TEMPLATE_CGI="template.cgi"


function template() {
	local FNAME=$1
}

source s3.ebasename.sh
if [ "$TEMPLATE_CGI" == $( ebasename $0 ) ]; then
	#Not sourced, do something with this.

	#Script root directory.
	TEMPLATE_DIR=$(dirname $(readlink -f $0))
	export PATH=${TEMPLATE_DIR}:$PATH

	TEMPLATE_CGI_INFO=${TEMPLATE_CGI}
	#source .cgi.ui..template.cgi
	source ${TEMPLATE_DIR}/ui/.template.cgi
	set -o pipefail

	template "${FNAME}" > "${DEF_TMP_NAME}_out" && \
		mv "${DEF_TMP_NAME}_out" ${1}

	exit $?
fi

fi
