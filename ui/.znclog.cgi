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
	DOT_WEBMODE=${DOT_WEBMODE-"auto"}
	DOT_URL_CONVERT=${DOT_URL_CONVERT-"yes"}
	DOT_TELETEXT=${DOT_TELETEXT-"no"}

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
        -x          Hide status changes (yes/no) [$DOT_HIDE_STATUS]
        -c          Which channel [$DOT_CHANNEL]
        -w          Web formatted or terminal mode (yes/no/auto) [$DOT_WEBMODE]
        -r          Reverse toggle [$DOT_REVERSE]
        -l          Convert URL:s to links toggle [$DOT_URL_CONVERT]
        -t          Convert URL:s to links toggle [$DOT_TELETEXT]

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
	while getopts hL:n:x:w:c:rltd OPTION; do
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
		c)
			CHANNEL="${OPTARG}"
			;;
		w)
			WEBMODE="${OPTARG}"
			;;
		r)
			if [ $DOT_REVERSE == "yes" ]; then
				REVERSE="no"
			else
				REVERSE="yes"
			fi
			;;
		l)
			if [ $DOT_URL_CONVERT == "yes" ]; then
				URL_CONVERT="no"
			else
				URL_CONVERT="yes"
			fi
			;;
		t)
			if [ $DOT_TELETEXT == "yes" ]; then
				TELETEXT="no"
			else
				TELETEXT="yes"
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

# Special handling of this variable breaking convention for these
# scripts.
WEBMODE=${WEBMODE-"${DOT_WEBMODE}"}
if [ "X${REMOTE_PORT}" != "X" -a  "X${WEBMODE}" == "Xauto" ]; then
	WEBMODE='yes'
fi
# ---------------------------------------------------------------

if [ "X${WEBMODE}" == "Xyes" ]; then
	if [ -t 0  -a  -t 1 ]; then
		#Has terminal on both stdin and stdout
		if [ $# -gt 0 ]; then
			#Running in TERMINAL as WEBMODE (test-mode)
			if [ "X${QUERY_STRING}" != "X" ]; then
				exec 3>&1 1>&2
				echo "QUERY_STRING [${QUERY_STRING}] cant be defined in"
				echo "terminal mode when arguments are passed"
				exec 1>&3 3>&-
				exit 1
			fi
			QUERY_STRING=$1
			for (( I=2 ; I<=$# ; I++ )); do
				QUERY_STRING="${QUERY_STRING}&$(eval echo \$${I})"
			done
		fi
	fi

	# Defining to empty string if not defined avoid spewing out environment
	QUERY_STRING=${QUERY_STRING-""}

	# Save the old internal field separator.
	OIFS="$IFS"

	# Set the field separator to & and parse the QUERY_STRING at the ampersand.
	IFS="${IFS}&"
	set $QUERY_STRING
	Args="$*"
	IFS="$OIFS"

	# Next parse the individual "name=value" tokens.

	# DAYS_BACK=""
	# HIDE_STATUS=""
	# REVERSE=""
	# CHANNEL=""

	for i in $Args ;do

		#Set the field separator to =
		IFS="${OIFS}="
		set $i
		IFS="${OIFS}"

		case $1 in
			days_back) DAYS_BACK="${2}"
				   ;;
			hide_status) HIDE_STATUS="${2}"
				   ;;
			reverse) REVERSE="${2}"
				   ;;
			url_convert) URL_CONVERT="${2}"
				   ;;
			teletext) TELETEXT="${2}"
				   ;;
			channel) CHANNEL="${2}"
				   ;;
			*)     echo "<hr>Warning:"\
						"<br>Unrecognized variable \'$1\' passed by FORM in QUERY_STRING.<hr>"
				   ;;

		esac
	done
fi



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
	URL_CONVERT=${URL_CONVERT-"${DOT_URL_CONVERT}"}
	TELETEXT=${TELETEXT-"${DOT_TELETEXT}"}

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
		echo "  WEBMODE=$WEBMODE"
		echo "  URL_CONVERT=$URL_CONVERT"
		echo "  TELETEXT=$TELETEXT"
		echo "  QUERY_STRING=$QUERY_STRING"
		echo
		exec 1>&3 3>&-
		exit 0
	fi

