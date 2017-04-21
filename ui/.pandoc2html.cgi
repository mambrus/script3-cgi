# UI part of all pandoc2html tool
# This is not even a script, stupid and can't exist alone. It is purely
# meant for being included.

DEF_TMP_NAME="/tmp/${PANDOC2HTML_CGI_INFO}_inter"
PANDOC2HTML_DOTFILE=.pandoc2html

if ! [ -f ${HOME}/${PANDOC2HTML_DOTFILE} ]; then
	echo -n "ERROR $(basename $(readlink -f $0)): " 1>&2
	echo "File [$PANDOC2HTML_DOTFILE] in \$HOME missing! Please set-up..." 1>&2
	exit 1
fi

# Get user environment settings from dot-file
eval $(
	cat "${HOME}/${PANDOC2HTML_DOTFILE}" | \
	grep -vE '^#' | \
	grep -vE '^[[:space:]]*$' | \
	sed -E 's/^/export /'
)

function print_pandoc2html_help() {
			cat <<EOF
NAME
        $PANDOC2HTML_CGI_INFO - Blah blah

SYNOPSIS
        $PANDOC2HTML_CGI_INFO [options] filename

DESCRIPTION
        $PANDOC2HTML_CGI_INFO blah

    Something
        Blah

EXAMPLES
        $PANDOC2HTML_CGI_INFO -msmiffo

OPTIONS

    General options
        -h          This help

    Debugging and verbosity options
        -d          Output additional debugging info and additional
                    verbosity

OPERATION

    Blah

    Subsection:

        Blah

        * blaha

AUTHOR
        Written by Michael Ambrus, 2 Feb 2015

EOF
}
	while getopts hm:d OPTION; do
		case $OPTION in
		h)
			if [ -t 1 ]; then
				print_pandoc2html_help $0 | less -R
			else
				print_pandoc2html_help $0
			fi
			exit 0
			;;
		d)
			PANDOC2HTML_DEBUG="yes"
			;;
		?)
			echo "Syntax error: options" 1>&2
			echo "For help, type: $PANDOC2HTML_CGI_INFO -h" 1>&2
			exit 2
			;;

		esac
	done
	shift $(($OPTIND - 1))

#	if [ $# -ne 1 ]; then
#		echo "Syntax error: arguments" \
#			"$PANDOC2HTML_CGI_INFO number of arguments should be exactly one:" \
#			"input filename" 1>&2
#		echo "For help, type: $PANDOC2HTML_CGI_INFO -h" 1>&2
#		exit 2
#	fi


#Actuating defaults if needed
	PANDOC2HTML_DEBUG=${PANDOC2HTML_DEBUG-"no"}

	if [ $PANDOC2HTML_DEBUG == "yes" ]; then
		exec 3>&1 1>&2
		echo "Variables:"
		echo "  PANDOC2HTML_DEBUG=$PANDOC2HTML_DEBUG"
		echo "  PANDOC2HTML_DIR=$PANDOC2HTML_DIR"
		echo
		exec 1>&3 3>&-
	fi

