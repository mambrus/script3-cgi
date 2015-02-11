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
	sed -E 's/^/export DOT_/'
)

#Hard-coded defaults if not set via DOT-file
#Step 1
	DOT_ZNC_LOG_DIRECTORY=${DOT_ZNC_LOG_DIRECTORY-"${HOME}/.znc/users/$USER/networks/freenode/moddata/log/znc_log"}
	DOT_DAYS_BACK=${DOT_DAYS_BACK-"infinite"}
	DOT_HIDE_STATUS=${DOT_HIDE_STATUS-"no"}
	DOT_REVERSE=${DOT_REVERSE-"no"}
	DOT_CHANNEL=${DOT_CHANNEL-"#bladerf"}

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
        - Defaults within []
		- Toggle is in relation to environment variable if set or hard-coded
		  defaults

    General options
        -h          This help
        -L          Log directory [$DOT_ZNC_LOG_DIRECTORY]
        -n          Number of days back [$DOT_DAYS_BACK]
        -x          Hide status changes yes/no [$DOT_HIDE_STATUS]
        -c          Which channel [$DOT_CHANNEL]
        -r          Reverse toggle [$DOT_REVERSE]

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
	while getopts hL:n:x:c:rd OPTION; do
		case $OPTION in
		h)
			if [ -t 1 ]; then
				print_znclog_help $0 | less -R
			else
				print_znclog_help $0
			fi
			exit 0
			;;
		L)
			ZNC_LOG_DIRECTORY="${OPTARG}"
			;;
		n)
			DAYS_BACK="${OPTARG}"
			;;
		x)
			HIDE_STATUS="${OPTARG}"
			;;
		x)
			CHANNEL="${OPTARG}"
			;;
		r)
			if [ $DOT_REVERSE == "yes" ]; then
				REVERSE="no"
			else
				REVERSE="yes"
			fi
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


#Final variable deduction
#Step 2
	ZNC_LOG_DIRECTORY=${ZNC_LOG_DIRECTORY-"${DOT_ZNC_LOG_DIRECTORY}"}
	DAYS_BACK=${DAYS_BACK-"${DOT_DAYS_BACK}"}
	HIDE_STATUS=${HIDE_STATUS-"${DOT_HIDE_STATUS}"}
	REVERSE=${REVERSE-"${DOT_REVERSE}"}
	CHANNEL=${CHANNEL-"${DOT_CHANNEL}"}

	if [ $ZNCLOG_DEBUG == "yes" ]; then
		exec 3>&1 1>&2
		echo "Variables:"
		echo "  ZNCLOG_DEBUG=$ZNCLOG_DEBUG"
		echo "  ZNCLOG_DIR=$ZNCLOG_DIR"
		echo "  ZNC_LOG_DIRECTORY=$ZNC_LOG_DIRECTORY"
		echo "  DAYS_BACK=$DAYS_BACK"
		echo "  HIDE_STATUS=$HIDE_STATUS"
		echo "  REVERSE=$REVERSE"
		echo "  CHANNEL=$CHANNEL"
		echo
		exec 1>&3 3>&-
	fi

