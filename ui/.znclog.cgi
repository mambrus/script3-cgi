# UI part of all znclog tool
# This is not even a script, stupid and can't exist alone. It is purely
# meant for being included.

DEF_TMP_NAME="/tmp/${ZNCLOG_CGI_INFO}_inter"
ZNCLOG_DOTFILE=.znclog

if ! [ -f ${HOME}/${ZNCLOG_DOTFILE} ]; then
	echo -n "ERROR $(basename $(readlink -f $0)): " 1>&2
	echo "File [$ZNCLOG_DOTFILE] in \$HOME missing! Please set-up..." 1>&2
	exit 1
fi

# Get user environment settings from dot-file
eval $(
	cat "${HOME}/${ZNCLOG_DOTFILE}" | \
	grep -vE '^#' | \
	grep -vE '^[[:space:]]*$' | \
	sed -E 's/^/export /'
)

function print_znclog_help() {
			cat <<EOF
NAME
        $ZNCLOG_CGI_INFO - Blah blah

SYNOPSIS
        $ZNCLOG_CGI_INFO [options] filename

DESCRIPTION
        $ZNCLOG_CGI_INFO blah

    Something
        Blah

EXAMPLES
        $ZNCLOG_CGI_INFO -msmiffo

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
				print_znclog_help $0 | less -R
			else
				print_znclog_help $0
			fi
			exit 0
			;;
		d)
			ZNCLOG_DEBUG="yes"
			;;
		?)
			echo "Syntax error: options" 1>&2
			echo "For help, type: $ZNCLOG_CGI_INFO -h" 1>&2
			exit 2
			;;

		esac
	done
	shift $(($OPTIND - 1))

#	if [ $# -ne 1 ]; then
#		echo "Syntax error: arguments" \
#			"$ZNCLOG_CGI_INFO number of arguments should be exactly one:" \
#			"input filename" 1>&2
#		echo "For help, type: $ZNCLOG_CGI_INFO -h" 1>&2
#		exit 2
#	fi


#Actuating defaults if needed
	ZNCLOG_DEBUG=${ZNCLOG_DEBUG-"no"}

	if [ $ZNCLOG_DEBUG == "yes" ]; then
		exec 3>&1 1>&2
		echo "Variables:"
		echo "  ZNCLOG_DEBUG=$ZNCLOG_DEBUG"
		echo "  ZNCLOG_DIR=$ZNCLOG_DIR"
		echo
		exec 1>&3 3>&-
	fi

