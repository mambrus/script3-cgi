#!/bin/bash
# Author: Michael Ambrus (ambrmi09@gmail.com)
# 2015-02-14

#HTML helpers to cgi-scripts

# #1: Title if the page
function page_header() {
	local TITLE=$1

	if [ "X${WEBMODE}" == "Xyes" ]; then
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
	if [ "X${WEBMODE}" == "Xyes" ]; then
		cat -- | sed -e 's/</\&lt;/g' -e 's/>/\&gt;/g'
	else
		cat --
	fi
}
#<a href="http://www.w3schools.com">Visit W3Schools.com!</a>
function cnvrt_urls2links() {
	if [ "X${WEBMODE}" == "Xyes" -a "X${URL_CONVERT}" == "Xyes" ]; then
		cat -- | \
			sed -E 's/(http[s]?:\/\/)([[:graph:]]+)/<a href="\1\2">\1\2<\/a>/g'
			
			#sed -E 's/(http[s]?:\/\/)(.*)([[:space:]])/<a href="\1\2">\1\2<\/a>\3/'
	else
		cat --
	fi
}

function page_footer() {
	if [ "X${WEBMODE}" == "Xyes" ]; then
		echo '</pre>'
		echo '</body>'
		echo '</html>'
	fi
}
