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

# Installing Red Hat dependencies

For Red Hat and CentOS platforms, you must bundle the
dependencies and transfer them to the offline system.
{:shortdesc}

<ol>
<li>Log in to your Red Hat online system to install the Red Hat dependencies.
<ol type="a"> 
<li>Install the EPEL repository.
<p>
```
yum install epel-release
```
</p></li>
<li>Run the Cloudant&reg; Self-Extracting Archive. See [Installing Cloudant Local packages](clinstall_extract_cl_install_packages.html).
<p>
`
./cloudant-<version>-<os>-<arch>.bin
`
</p></li>
</ol>
</li>
<li>Bundle the dependencies into a compressed (tar) file by running the following commands.
<p>
`yum install createrepo` <br>
`mkdir cloudant-deps` <br>
`yum reinstall -y --downloadonly --downloaddir=cloudant-deps cloudant-dbnode cloudant-lbnode iptables-services python2-pip` <br>
`createrepo cloudant-deps` <br>
`tar -czvf cloudant-deps.tar.gz cloudant-deps`
</p></li>
<li>Copy the file to the offline system.
<p>
`cp cloudant-deps.tar.gz offline.system.com:/tmp`</p></li>
<li>Log in to the offline system.</li>
<li>Set up the repository for the Cloudant&reg; dependencies.
<p>
`cd /tmp` <br>
`tar -xvf cloudant-deps.tar.gz`<br>
<br>
`echo "[cloudant-deps]" >> /etc/yum.repos.d/cloudant-deps.repo`<br>
`echo "name=IBM, Cloudant Dependencies" >> /etc/yum.repos.d/cloudant-deps.repo`<br>
`echo "baseurl=file:///tmp/cloudant-deps" >> /etc/yum.repos.d/cloudant-deps.repo`<br>
`echo "enabled = 1" >> /etc/yum.repos.d/cloudant-deps.repo`<br>
`echo "gpgcheck = 0" >> /etc/yum.repos.d/cloudant-deps.repo`<br>
<br>
`yum clean all`
</p>
</li></ol>
