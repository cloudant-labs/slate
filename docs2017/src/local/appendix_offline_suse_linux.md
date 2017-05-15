---

copyright:
  years: 2015, 2017
lastupdated: "2017-03-01"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Installing SUSE dependencies

You must bundle the SUSE dependencies and transfer them to the
offline system.
{:shortdesc}
<ol>
<li>Log in to your SUSE online system to install the SUSE dependencies.
<ol type="a">
<li>Download `pip-9.0.1.tar.gz` file from [https://pypi.python.org/pypi/pip ![External link icon](images/launch-glyph.svg "External link icon")](https://pypi.python.org/pypi/pip).</li>
<li>Install `python-pip`.
<p>`tar -xvf pip-9.0.1.tar.gz`<br>
`cd pip-9.0.1.tar.gz`<br>
`python setup.py install`
</p></li>
<li>Run the Cloudant&reg; Self-Extracting Archive.
<p>`./cloudant-<version>-<os>-<arch>.bin`</p></li>
</ol></li>
<li>Download and bundle the dependencies into a compressed (tar)
    file by running the following commands.
<p>`zypper -n install createrepo`<br>
`mkdir cloudant-deps`<br>
`zypper --pkg-cache-dir=cloudant-deps download java-1_7_0-openjdk java-1_7_0-openjdk-headless java-1_7_0-openjdk-devel curl rsyslog lcms2 timezone-java python-setuptools python-base python-pip python-setuptools`<br>
`createrepo cloudant-deps`<br>
`tar -czvf cloudant-deps.tar.gz cloudant-deps`</p>    </li>
<li>Copy the compressed (tar) file to the offline system.
<p>`scp cloudant-deps.tar.gz <offline.system.com>:/tmp`<br>
`scp pip-9.0.1.tar.gz <offline.system.com>:/tmp`</p></li>
<li>Log in to the offline system.</li>
<li>Set up the repository for the Cloudant dependencies.
<p>`cd /tmp`<br>
`tar -xvf cloudant-deps.tar.gz`<br>
`zypper -n addrepo —no-gpgcheck /tmp/cloudant-deps cloudant-deps`<br>
`zypper refresh`<br>
`zypper install python-pip`<br>
`tar -xvf pip-9.0.1.tar.gz`<br>
`cd pip-9.0.1`<br>
`python setup.py install`</p></li>
</ol>