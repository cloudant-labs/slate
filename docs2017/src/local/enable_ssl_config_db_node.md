---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-09"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Enabling SSL security on the database node

Configure the database node to use the SSL security files.
{:shortdesc}

<ol><li>Update the `/opt/cloudant/etc/local.ini` file on each database node.
<ol type="a"><li>Enable the `https` daemon by modifying the `httpsd` line in the `[daemons]` section.
<p>`[daemons]`<br>
`httpsd = {chttpd, start_link, [https]}`
</p>
</li>
<li>Provide links to the `ca.pem`, `serverX.key` and `serverX.pem` files.
<p>`[ssl]`<br>
`cacert_file = /<filelocation>/ca.pem`<br>
`cert_file = /<filelocation>/serverX.pem`<br>
`key_file = /<filelocation>/serverX.key`</p></li></ol>
<li>Save and close the `/opt/cloudant/etc/local.ini` file.</li>
<li>Restart Cloudant&reg; on the database node.
<p>**Note:** For more information about configuring Cloudant Local for SSL-based secure connections, see [Secure Socket Level Options ![External link icon](images/launch-glyph.svg "External link icon")](http://docs.couchdb.org/en/latest/config/http.html#secure-socket-level-options).
</p></li></ol>
