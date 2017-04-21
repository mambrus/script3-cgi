
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

<h2>CGI hints</h2>

A beginner's guide to CGI scripting:
http://www.anaesthetist.com/mnm/cgi/Findex.htm#index.htm

<h2>Arguments passed to this script</h2>

<h3>QUERY_STRING</h3>
[$QUERY_STRING]

<h3>PATH_INFO</h3>
[$PATH_INFO]


<h2>AUTHOR</h2>
Written by Michael Ambrus, 21 March 2017

EOF
}
