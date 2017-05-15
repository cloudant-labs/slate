---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-17"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Installing Cloudant Local packages

To install (or uninstall) Cloudant&reg; Local, you must be a root
user or use the `sudo` command.
{:shortdesc}


<ol>
<li>Download the self-extracting archive file for the OS version you want to
   install.</li>
<li>Ensure that the self-extracting archive file has executable permissions,
   and if not, change the mode to execute by running this command.
   <p><code>chmod +x cloudant-1.1.0-984-el6-x86_64.bin</code></p></li>
<li>Install the Cloudant Local packages (`cloudant-<version>-<os>-<arch>.bin`) and install CAST.
<ol type="a"><li>To install the Cloudant Local packages by using an interactive wizard, run the following command.
<p><code>./cloudant-1.1.0-984-el6-x86_64.bin</code></p></li>
<li>To install the Cloudant Local packages (`cloudant-<version>-<os>-<arch>.bin`) silently, and implicitly accept the IBM&reg; License Agreement, run the following command. The properties file you specify determines whether this instance of Cloudant Local is used for production or development purposes.
<p><code>./cloudant-1.1.0-984-el6-x86_64.bin -- -s</code></p></li></ol></li>
</ol>

