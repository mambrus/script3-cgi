# UI part of all webdot2 tool
# This is not even a script, stupid and can't exist alone. It is purely
# meant for being included.

DEF_TMP_NAME="/tmp/${WEBDOT2_CGI_INFO}_inter"
WEBDOT2_DOTFILE=.webdot2

if ! [ -f ${HOME}/${WEBDOT2_DOTFILE} ]; then
	echo -n "ERROR $(basename $(readlink -f $0)): " 1>&2
	echo "File ${HOME}/${WEBDOT2_DOTFILE} (i.e. [$WEBDOT2_DOTFILE] in \$HOME) missing! Please set-up..." 1>&2
	exit 1
fi

# Get user environment settings from dot-file
eval $(
	cat "${HOME}/${WEBDOT2_DOTFILE}" | \
	grep -vE '^#' | \
	grep -vE '^[[:space:]]*$' | \
	sed -E 's/^/export /'
)

#Hard-coded defaults of default. 2 stage over-ridden if not set via DOT-file
#Step 1
	DOT_WEBDOT2_LOGFILE=${DOT_WEBDOT2_LOGFILE-"/tmp/webdot2_log"}
	DOT_WEBMODE=${DOT_WEBMODE-"auto"}
	DOT_URL_CONVERT=${DOT_URL_CONVERT-"yes"}
	DOT_HELP_ON_NOARG=${DOT_HELP_ON_NOARG-"yes"}
	DOT_WEBHELP=${DOT_WEBHELP-"no"}
	DOT_EXEC_PATH=${DOT_EXEC_PATH-"/usr/bin"}

function print_webdot2_help() {
			cat <<EOF
NAME
        $WEBDOT2_CGI_INFO - Blah blah

SYNOPSIS
        $WEBDOT2_CGI_INFO [options] filename

DESCRIPTION
        $WEBDOT2_CGI_INFO blah

    Something
        Blah

EXAMPLES
        $WEBDOT2_CGI_INFO -msmiffo

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
        Written by Michael Ambrus, 2 Feb 2017

EOF
}

	while getopts hHL:x:w:rltdX OPTION; do
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
			WEBDOT2_LOGFILE="${OPTARG}"
			;;
		H)
			WEBHELP="yes"
			;;
		x)
			EXEC_PATH="${OPTARG}"
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
		X)
			if [ $DOT_HELP_ON_NOARG == "yes" ]; then
				HELP_ON_NOARG="no"
			else
				HELP_ON_NOARG="yes"
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
			WEBDOT2_DEBUG="yes"
			;;
		?)
			echo "Syntax error: options" 1>&2
			echo "For help, type: $WEBDOT2LOG_CGI_INFO -h" 1>&2
			exit 2
			;;

		esac
	done
	shift $(($OPTIND - 1))

# -------------------------------------------------------------------------
WEBMODE=${WEBMODE-"${DOT_WEBMODE}"}
if [ "X${REMOTE_PORT}" != "X" -a  "X${WEBMODE}" == "Xauto" ]; then
	WEBMODE='yes'
fi
HELP_ON_NOARG=${HELP_ON_NOARG-"${DOT_HELP_ON_NOARG}"}

# -------------------------------------------------------------------------
if [ "X${WEBMODE}" == "Xyes" ] ; then
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


	if [ "X${QUERY_STRING}" = "X" ] && [ "X${PATH_INFO}" = "X" ] ; then
		if [ $HELP_ON_NOARG == 'yes' ]; then
			WEBHELP='yes'
		fi
	fi

	# Parse first. I.e. if QUERY_STRING also exists, it will have presidence
	# where in conflict
	if [ "X${PATH_INFO}" != "X" ]; then
		ENGINE=$(cut -f2 -d"/" <<< ${PATH_INFO})
		FORMAT=$(cut -f3 -d"/" <<< ${PATH_INFO})

		PROTO=$(cut -f4 -d"/" <<< ${PATH_INFO})
		URIN=$(sed -e 's/.*://' <<< ${PATH_INFO} | cut -f1 -d"?")

		#Note PATH_INFO strips consecutive "/" so work-around needed
		case $(tr '[:upper:]' '[:lower:]' <<< $PROTO) in
		http:|https:)
			EXTRA="/"
			;;
		file:)
			EXTRA="/"
			;;

		esac

		URI="${PROTO}${EXTRA}${URIN}"

		unset PROTO
		unset URIN
		unset EXTRA
	fi

	if [ "X${QUERY_STRING}" != "X" ]; then
		# Save the old internal field separator.
		OIFS="$IFS"

		# Set the field separator to & and parse the QUERY_STRING at the ampersand.
		IFS="${IFS}&"
		set $QUERY_STRING
		Args="$*"
		IFS="$OIFS"

		# Next parse the individual "name=value" tokens.

		for i in $Args ;do

			#Set the field separator to =
			IFS="${OIFS}="
			set $i
			IFS="${OIFS}"

			case $(tr '[:upper:]' '[:lower:]' <<< $1) in
				uri) URI="${2}"
					   ;;
				engine) ENGINE="${2}"
					   ;;
				format) FORMAT="${2}"
					   ;;
				url_convert) URL_CONVERT="${2}"
					   ;;
				teletext) TELETEXT="${2}"
					   ;;
				webmode) WEBMODE2="${2}"
					   ;;
				debug) WEBDOT2_DEBUG="${2}"
					   ;;
				*)     echo "Content-type: text/html"
			           echo ""
				       echo "<hr>Error:"\
							"<br>Unrecognized variable \"$1\" passed by FORM in QUERY_STRING=[$QUERY_STRING].<hr>"
				       exit 1
					   ;;

			esac
		done
	fi
fi


#Actuating defaults if needed
	WEBDOT2_DEBUG=${WEBDOT2_DEBUG-"no"}


#Final variable deduction
#Step 2
	WEBDOT2_LOGFILE=${WEBDOT2_LOGFILE-"${DOT_WEBDOT2_LOGFILE}"}
	URL_CONVERT=${URL_CONVERT-"${DOT_URL_CONVERT}"}
	THIS_SERVER=${THIS_SERVER-"${DOT_THIS_SERVER}"}
	WEBHELP=${WEBHELP-"${DOT_WEBHELP}"}
	TELETEXT=${TELETEXT-"${DOT_TELETEXT}"}
	WEBMODE2=${WEBMODE2-"no"}
	EXEC_PATH=${EXEC_PATH-"${EXEC_PATH}"}

	if [ $WEBDOT2_DEBUG == "yes" ]; then
		#exec 3>&1 1>&2

		#Note the two below will not be debugged correctly
		#as they are needed for formatting output
		WEBMODE=yes
		TELETEXT=no

		page_header "Debug env-vars:"

		(
			ENGINE=$(tr '[:upper:]' '[:lower:]' <<< ${ENGINE})
			FORMAT=$(tr '[:upper:]' '[:lower:]' <<< ${FORMAT})

			echo "  WEBDOT2_DEBUG: [$WEBDOT2_DEBUG]"
			echo "  WEBDOT2_LOGFILE: [$WEBDOT2_LOGFILE]"
			echo "  WEBMODE: [$WEBMODE]"
			echo "  WEBMODE2: [$WEBMODE2]"
			echo "  URL_CONVERT: [$URL_CONVERT]"
			echo "  WEBHELP: [$WEBHELP]"
			echo "  HELP_ON_NOARG: [$HELP_ON_NOARG]"
			echo "  TELETEXT: [$TELETEXT]"
			echo
			echo "  ENGINE: [${ENGINE}]"
			echo "  FORMAT: [${FORMAT}]"
			echo "  URI: [${URI}]"
			echo "  PROTO: [$PROTO]"
			echo "  URIN: [$URIN]"
			echo "  URIN: //"
			echo "  will exec: $EXEC_PATH/webdot.cgi ${URI}.${ENGINE}.${FORMAT}"
			echo
			echo "  QUERY_STRING: [$QUERY_STRING]"
			echo "  PATH_INFO: [$PATH_INFO]"
			echo
		) | cnvrt_eol

		page_footer
		#exec 1>&3 3>&-
		exit 0
	fi

