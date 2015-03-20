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
	DOT_NETWORK=${DOT_NETWORK-""}
	DOT_CHANNEL=${DOT_CHANNEL-"bladerf"}
	DOT_WEBMODE=${DOT_WEBMODE-"auto"}
	DOT_URL_CONVERT=${DOT_URL_CONVERT-"yes"}
	DOT_THIS_SERVER=${DOT_THIS_SERVER-"http://localhost"}
	DOT_TELETEXT=${DOT_TELETEXT-"no"}
	DOT_HELP_ON_NOARG=${DOT_HELP_ON_NOARG-"yes"}
	DOT_WEBHELP=${DOT_WEBHELP-"no"}

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
        -H          Web-help
        -L          Log directory [$DOT_ZNC_LOG_DIRECTORY]
        -n          Number of days back [$DOT_DAYS_BACK]
        -x          Hide status changes (yes/no) [$DOT_HIDE_STATUS]
        -N          Which network [$DOT_NETWORK]
        -c          Which channel [#$DOT_CHANNEL]
        -w          Web formatted or terminal mode (yes/no/auto) [$DOT_WEBMODE]
        -r          Reverse toggle [$DOT_REVERSE]
        -l          Convert URL:s to links toggle [$DOT_URL_CONVERT]
        -s          Server-name [$DOT_THIS_SERVER]
        -t          Toggle teletext-mode [$DOT_TELETEXT]
        -X          If no arguments, show web-help (toggle) [$DOT_HELP_ON_NOARG]

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


function print_webhelp() {
cat <<EOF

<h1>Help</h1>
<h2>Usage</h2>
To use <b>$(basename ${SCRIPT_NAME})</b> you follow standard CGI convention. I.e.:

proto://hostname/path-to-cgi/script<b>?</b>parameter1=value1<b>&</b>parameter2=value2<b>&</b>parameter3=value3

The order of the parameters does not matter. If any parameter is omitted,
the behaviour falls back on the default listed  below. If no parameters are
given, behaviour depends on configuration and can either show this help or
fall-back fully on all defaults.

<h2>Examples</h2>
${THIS_SERVER}${SCRIPT_NAME}?channel=$CHANNEL&days_back=$DAYS_BACK
${THIS_SERVER}${SCRIPT_NAME}?channel=$CHANNEL&reverse=$REVERSE&hide_status=$HIDE_STATUS&url_convert=$URL_CONVERT

<h2>Parameters</h2>
This script is influenced by the following parameters (default/given value
are in brackets).

<u>	network:     [<b>$DOT_NETWORK</b>      /   <b>$NETWORK</b>]      </u>
ZNC can be a bouncer for several different IRC-servers. The various
server-configurations are called "networks". If this bouncer tracks only one
network, this field can be left blank. If not, the network name must be
given or pre-set.

<u>	channel:     [<b>$DOT_CHANNEL</b>      /   <b>$CHANNEL</b>]      </u>
Which channel to list. Note that only those being monitored will sesult in
any output.

<u>	days_back:   [<b>$DOT_DAYS_BACK</b>    /   <b>$DAYS_BACK</b>]    </u>
How many days back to list for a certain channel

<u>	hide_status: [<b>$DOT_HIDE_STATUS</b>  /   <b>$HIDE_STATUS</b>]  </u>
Hide part/join messages.

<u>	reverse:     [<b>$DOT_REVERSE</b>      /   <b>$REVERSE</b>]      </u>
Reverse the output. I.e. last line on top. This can be useful if you refresh
often to look for recent changes as any delays or low bandwidth will not
affect the line youre most interested in. 

Use in combination with low <tt>days_back</tt> value and a client side
auto reload request gives almost "real-time" experience.

<u>	url_convert: [<b>$DOT_URL_CONVERT</b>  /   <b>$URL_CONVERT</b>]  </u>
Let server convert any pattern that loocks like a URL to a link.

<u>	teletext:    [<b>$DOT_TELETEXT</b>     /   <b>$TELETEXT</b>]     </u>
Text in logs are output as-is with minimal html overhead. Use with
<tt>url_convert=no</tt> for a near raw output.

<u>	webmode:    [<b>$DOT_WEBMODE</b>     /   <b>$WEBMODE2</b>]     </u>
Set this to <b>raw</b> for purely raw output. This mimics the case
where this cgi-script operates as a normal shell-script.

<i>Note:</i> Dont use this in a normal browser as it will not render. This
is a debug option and/or to be used with <tt>wget</tt> to get raw logs like
for example this:

<code>wget -O- 2>/dev/null \
   '${THIS_SERVER}${SCRIPT_NAME}?channel=$CHANNEL&days_back=$DAYS_BACK&webmode=raw' |\
   grep whatever

</code>

<u>	help:        [<b>$DOT_WEBHELP</b>      /   <b>$WEBHELP</b>]      </u>
This help. Note that you can combine this parameter with the others to
affect the example-links above.

I.e. if you remember only one parameter, say channel, you can regenerate
examples links that apply to that channel instead.

<h2>AUTHOR</h2>
Written by Michael Ambrus, 2 Feb 2015

EOF
}


	while getopts hHL:n:x:w:N:c:s:rltdX OPTION; do
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
		H)
			WEBHELP="yes"
			;;
		n)
			DAYS_BACK="${OPTARG}"
			;;
		x)
			HIDE_STATUS="${OPTARG}"
			;;
		N)
			NETWORK="${OPTARG}"
			;;
		c)
			CHANNEL="${OPTARG}"
			;;
		s)
			THIS_SERVER="${OPTARG}"
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

# Special handling of certain variables that influence fundamental
# behaviour. They break convention for these scripts. Normally all variables
# are finalized last in this file.
# -------------------------------------------------------------------------
WEBMODE=${WEBMODE-"${DOT_WEBMODE}"}
if [ "X${REMOTE_PORT}" != "X" -a  "X${WEBMODE}" == "Xauto" ]; then
	WEBMODE='yes'
fi
HELP_ON_NOARG=${HELP_ON_NOARG-"${DOT_HELP_ON_NOARG}"}
# -------------------------------------------------------------------------
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

	if [ "X${QUERY_STRING}" != "X" ]; then
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
		# NETWORK=""
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
				network) NETWORK="${2}"
					   ;;
				channel) CHANNEL="${2}"
					   ;;
				help|webhelp) WEBHELP="${2}"
					   ;;
				webmode) WEBMODE2="${2}"
					   ;;
				*)     echo "Content-type: text/html"
			           echo ""
				       echo "<hr>Error:"\
							"<br>Unrecognized variable \"$1\" passed by FORM in QUERY_STRING.<hr>"
				       exit 1
					   ;;

			esac
		done
	else if [ $HELP_ON_NOARG == 'yes' ]; then
		WEBHELP='yes'
	fi fi
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
	NETWORK=${NETWORK-"${DOT_NETWORK}"}
	CHANNEL=${CHANNEL-"${DOT_CHANNEL}"}
	URL_CONVERT=${URL_CONVERT-"${DOT_URL_CONVERT}"}
	THIS_SERVER=${THIS_SERVER-"${DOT_THIS_SERVER}"}
	WEBHELP=${WEBHELP-"${DOT_WEBHELP}"}
	TELETEXT=${TELETEXT-"${DOT_TELETEXT}"}
	WEBMODE2=${WEBMODE2-"no"}

	if [ $ZNCLOG_DEBUG == "yes" ]; then
		exec 3>&1 1>&2
		echo "Variables:"
		echo "  ZNCLOG_DEBUG=$ZNCLOG_DEBUG"
		echo "  ZNCLOG_DIR=$ZNCLOG_DIR"
		echo "  ZNC_LOG_DIRECTORY=$ZNC_LOG_DIRECTORY"
		echo "  DAYS_BACK=$DAYS_BACK"
		echo "  HIDE_STATUS=$HIDE_STATUS"
		echo "  REVERSE=$REVERSE"
		echo "  NETWORK=$NETWORK"
		echo "  CHANNEL=$CHANNEL"
		echo "  WEBMODE=$WEBMODE"
		echo "  WEBMODE2=$WEBMODE2"
		echo "  URL_CONVERT=$URL_CONVERT"
		echo "  THIS_SERVER=$THIS_SERVER"
		echo "  WEBHELP=$WEBHELP"
		echo "  HELP_ON_NOARG=$HELP_ON_NOARG"
		echo "  TELETEXT=$TELETEXT"
		echo "  QUERY_STRING=$QUERY_STRING"
		echo
		exec 1>&3 3>&-
		exit 0
	fi

