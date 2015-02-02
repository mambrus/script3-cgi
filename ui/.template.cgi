# UI part of all template tool
# This is not even a script, stupid and can't exist alone. It is purely
# meant for being included.

DEF_TMP_NAME="/tmp/${TEMPLATE_CGI_INFO}_inter"
TEMPLATE_DOTFILE=.template

if ! [ -f ${HOME}/${TEMPLATE_DOTFILE} ]; then
	echo -n "ERROR $(basename $(readlink -f $0)): " 1>&2
	echo "File [$TEMPLATE_DOTFILE] in \$HOME missing! Please set-up..." 1>&2
	exit 1
fi

# Get user environment settings from dot-file
eval $(
	cat "${HOME}/${TEMPLATE_DOTFILE}" | \
	grep -vE '^#' | \
	grep -vE '^[[:space:]]*$' | \
	sed -E 's/^/export /'
)

function print_template_help() {
			cat <<EOF
NAME
        $TEMPLATE_CGI_INFO - Blah blah

SYNOPSIS
        $TEMPLATE_CGI_INFO [options] filename

DESCRIPTION
        $TEMPLATE_CGI_INFO blah

    Something
        Blah

EXAMPLES
        $TEMPLATE_CGI_INFO -msmiffo

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
				print_template_help $0 | less -R
			else
				print_template_help $0
			fi
			exit 0
			;;
		d)
			TEMPLATE_DEBUG="yes"
			;;
		?)
			echo "Syntax error: options" 1>&2
			echo "For help, type: $TEMPLATE_CGI_INFO -h" 1>&2
			exit 2
			;;

		esac
	done
	shift $(($OPTIND - 1))

#	if [ $# -ne 1 ]; then
#		echo "Syntax error: arguments" \
#			"$TEMPLATE_CGI_INFO number of arguments should be exactly one:" \
#			"input filename" 1>&2
#		echo "For help, type: $TEMPLATE_CGI_INFO -h" 1>&2
#		exit 2
#	fi


#Actuating defaults if needed
	TEMPLATE_DEBUG=${TEMPLATE_DEBUG-"no"}

	if [ $TEMPLATE_DEBUG == "yes" ]; then
		exec 3>&1 1>&2
		echo "Variables:"
		echo "  TEMPLATE_DEBUG=$TEMPLATE_DEBUG"
		echo "  TEMPLATE_DIR=$TEMPLATE_DIR"
		echo
		exec 1>&3 3>&-
	fi

