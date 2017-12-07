# ![alt tag](images/apireference_icon.png) API Reference

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the API Reference topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/index.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

The Cloudant API reference is intended to be a comprehensive and living catalog of Cloudant's capabilities.
Contributions are welcome through [Cloudant Labs on GitHub](https://github.com/cloudant-labs/slate).
The API reference content is built with [Slate](https://github.com/tripit/slate).

#### For the cURL samples

There are three ways you can supply the username and password data for a request.

1.	The `-u $USERNAME` parameter on its own causes
cURL to ask you to enter your password interactively on the command line before performing the request. This option is used for the cURL examples in the Cloudant API reference.

2.	**[Caution: This option is not secure]** Entering the combination parameter `-u $USERNAME:$PASSWORD` as part of your command means that you are not asked to enter your password interactively.
However, a plain text copy of your password appears in the terminal log.
<br/>
<br/>
A variation of this method requires you to define a curl control file,
containing the following details:<br/>
	`--user "$USERNAME:$PASSWORD"`<br/>
	`--globoff`<br/>
	`--proto "=https"`<br/>
You can then define an 'alias' that enables the curl command to apply the control file,
for example:<br/>
	`alias acurl="curl -s --config <full_path_and_name_of_config_file> "`<br/>
Remember to exclude the control file from backups,
as it contains the password in clear text.

3.	**[Caution: This option is not secure]** For an `https` cURL request, you can supply the username and password as part of the URL:<br/>`... https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com ...`<br/>However, a plain text copy of your password appears in the terminal log.


