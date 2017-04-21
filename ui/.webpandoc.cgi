# UI part of all webpandoc tool
# This is not even a script, stupid and can't exist alone. It is purely
# meant for being included.

DEF_TMP_NAME="/tmp/${PANDOC2HTML_CGI_INFO}_inter"
PANDOC2HTML_DOTFILE=.webpandoc

if ! [ -f ${HOME}/${PANDOC2HTML_DOTFILE} ]; then
	echo -n "ERROR $(basename $(readlink -f $0)): " 1>&2
	echo "File ${HOME}/${PANDOC2HTML_DOTFILE} (i.e. [$PANDOC2HTML_DOTFILE] in \$HOME) missing! Please set-up..." 1>&2
	exit 1
fi

# Get user environment settings from dot-file
eval $(
	cat "${HOME}/${PANDOC2HTML_DOTFILE}" | \
	grep -vE '^#' | \
	grep -vE '^[[:space:]]*$' | \
	sed -E 's/^/export /'
)

#Hard-coded defaults of default. 2 stage over-ridden if not set via DOT-file
#Step 1
	DOT_PANDOC2HTML_LOGFILE=${DOT_PANDOC2HTML_LOGFILE-"/tmp/webpandoc_log"}
	DOT_WEBMODE=${DOT_WEBMODE-"auto"}
	DOT_URL_CONVERT=${DOT_URL_CONVERT-"yes"}
	DOT_HELP_ON_NOARG=${DOT_HELP_ON_NOARG-"yes"}
	DOT_WEBHELP=${DOT_WEBHELP-"no"}
	DOT_EXEC_PATH=${DOT_EXEC_PATH-"/usr/bin"}
	DOT_WORK_DIR=${DOT_WORK_DIR-"/tmp/webpandoc"}
	DOT_STANDALONE=${DOT_STANDALONE="yes"}
	DOT_OFORMAT=${DOT_OFORMAT-"html"}
	DOT_IFORMAT=${DOT_IFORMAT-"markdown"}

function print_webpandoc_help() {
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
        Written by Michael Ambrus, 2 Feb 2017

EOF
}

	while getopts hf:t:D:sHL:x:w:rltdX OPTION; do
		case $OPTION in
		h)
			if [ -t 1 ]; then
				print_znclog_help $0 | less -R
			else
				print_znclog_help $0
			fi
			exit 0
			;;
		f)
			IFORMAT="${OPTARG}"
			;;
		t)
			OFORMAT="${OPTARG}"
			;;
		D)
			WORKDIR="${OPTARG}"
			;;
		s)
			STANDALONE="yes"
			;;
		L)
			PANDOC2HTML_LOGFILE="${OPTARG}"
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
			PANDOC2HTML_DEBUG="yes"
			;;
		?)
			echo "Syntax error: options" 1>&2
			echo "For help, type: $PANDOC2HTMLLOG_CGI_INFO -h" 1>&2
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

	# Parse first. I.e. if QUERY_STRING also exists, it will have presidency
	# where in conflict
	if [ "X${PATH_INFO}" != "X" ]; then

		RPATH_INFO=$(
			echo $PATH_INFO | \
			cut -f1 -d":" | \
			sed -Ee 's/(.*)(\/.*$)/\1/'
		)
		NPATHS=$(echo $RPATH_INFO | sed -Ee 's/\//\n/g' | wc -l)
		URIN=$(sed -e 's/.*://' <<< ${PATH_INFO} | cut -f1 -d"?")


		case $NPATHS in
		1)
			PROTO=$(cut -f2 -d"/" <<< ${PATH_INFO})
			;;
		2)
			IFORMAT=$(cut -f2 -d"/" <<< ${PATH_INFO})
			PROTO=$(cut -f3 -d"/" <<< ${PATH_INFO})
			;;
		3)
			IFORMAT=$(cut -f2 -d"/" <<< ${PATH_INFO})
			OFORMAT=$(cut -f3 -d"/" <<< ${PATH_INFO})
			PROTO=$(cut -f4 -d"/" <<< ${PATH_INFO})
			;;
		*)
			echo "Content-type: text/html"
			echo ""
			echo "<hr>Error:"\
				"<br>Unrecognized PATH_INFO depth: [$PATH_INFO]<hr>"
			exit 1
			;;
		esac

		#Note PATH_INFO strips consecutive "/" so work-around needed
		case $(tr '[:upper:]' '[:lower:]' <<< $PROTO) in
		http:|https:)
			EXTRA="/"
			;;
		file:)
			EXTRA="//"
			;;
		esac

		URI="${PROTO}${EXTRA}${URIN}"

		unset PROTO
		unset URIN
		unset EXTRA
		unset RPATH_INFO
		unset NPATHS
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
				oformat) OFORMAT="${2}"
					   ;;
				iformat) IFORMAT="${2}"
					   ;;
				standalone) STANDALONE="${2}"
					   ;;
				teletext) TELETEXT="${2}"
					   ;;
				webmode) WEBMODE2="${2}"
					   ;;
				debug) PANDOC2HTML_DEBUG="${2}"
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
	PANDOC2HTML_DEBUG=${PANDOC2HTML_DEBUG-"no"}


#Final variable deduction
#Step 2
	PANDOC2HTML_LOGFILE=${PANDOC2HTML_LOGFILE-"${DOT_PANDOC2HTML_LOGFILE}"}
	URL_CONVERT=${URL_CONVERT-"${DOT_URL_CONVERT}"}
	THIS_SERVER=${THIS_SERVER-"${DOT_THIS_SERVER}"}
	WEBHELP=${WEBHELP-"${DOT_WEBHELP}"}
	TELETEXT=${TELETEXT-"${DOT_TELETEXT}"}
	WEBMODE2=${WEBMODE2-"no"}
	EXEC_PATH=${EXEC_PATH-"${EXEC_PATH}"}
	WORK_DIR=${WORK_DIR-"$DOT_WORK_DIR"}
	STANDALONE=${STANDALONE="$DOT_STANDALONE"}
	OFORMAT=${OFORMAT-"$DOT_OFORMAT"}
	IFORMAT=${IFORMAT-"$DOT_IFORMAT"}

	if [ $PANDOC2HTML_DEBUG == "yes" ]; then
		#exec 3>&1 1>&2

		#Note the two below will not be debugged correctly
		#as they are needed for formatting output
		WEBMODE=yes
		TELETEXT=no

		page_header "Debug env-vars:"

		(
			OFORMAT=$(tr '[:upper:]' '[:lower:]' <<< ${OFORMAT})
			IFORMAT=$(tr '[:upper:]' '[:lower:]' <<< ${IFORMAT})

			echo "  PANDOC2HTML_DEBUG: [$PANDOC2HTML_DEBUG]"
			echo "  PANDOC2HTML_LOGFILE: [$PANDOC2HTML_LOGFILE]"
			echo "  WEBMODE: [$WEBMODE]"
			echo "  WEBMODE2: [$WEBMODE2]"
			echo "  URL_CONVERT: [$URL_CONVERT]"
			echo "  WEBHELP: [$WEBHELP]"
			echo "  HELP_ON_NOARG: [$HELP_ON_NOARG]"
			echo "  TELETEXT: [$TELETEXT]"
			echo
			echo "  WORKDIR: [${WORKDIR}]"
			echo "  STANDALONE: [${STANDALONE}]"
			echo "  OFORMAT: [${OFORMAT}]"
			echo "  IFORMAT: [${IFORMAT}]"
			echo "  URI: [${URI}]"
			echo
			echo "  QUERY_STRING: [$QUERY_STRING]"
			echo "  PATH_INFO: [$PATH_INFO]"
			echo
		) | cnvrt_eol

		page_footer
		#exec 1>&3 3>&-
		exit 0
	fi

