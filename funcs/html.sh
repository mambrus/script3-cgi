#!/bin/bash
# Author: Michael Ambrus (ambrmi09@gmail.com)
# 2015-02-14

#HTML helpers to cgi-scripts

# #1: Title if the page
function page_header() {
	local TITLE=$1

	if [ "${WEBMODE}" == "yes" ]; then
		echo "Content-type: text/html"
		echo ""

		echo '<html>'
		echo '<head>'
		echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
		echo "<title>${TITLE}</title>"
		echo '</head>'
		echo '<body>'
		echo '<pre>'
	fi
}

function cnvrt_special_chars() {
	if [ "${WEBMODE}" == "yes" ]; then
		cat -- | sed -e 's/</\&lt;/g' -e 's/>/\&gt;/g'
	else
		cat --
	fi
}

function cnvrt_urls2links() {
	if [ "${WEBMODE}" == "yes" ]; then
		cat --
	else
		cat --
	fi
}

function page_footer() {
	if [ "${WEBMODE}" == "yes" ]; then
		echo '</pre>'
		echo '</body>'
		echo '</html>'
	fi
}
