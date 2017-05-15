---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-20"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Before you begin

Before you install Cloudant&reg; Local, confirm that your system
meets the following requirements.
{:shortdesc}

*  You must be the root user, or have sudo privileges, to install
   Cloudant Local. If you are not the root user, prefix all
   commands with the `sudo` command.

*  If security restrictions prevent you from accessing
   third-party repositories, you must download and install the
   required third-party packages before you start the
   installation.

*  The Cloudant Local installation on RHEL/CentOS systems
   requires that you enable the EPEL repository.

   *  If the repository is not already enabled on your system,
      run this command to install and enable EPEL.

      ``` sh
      sudo yum -y install epel-release
      ```
      {:codeblock}
      
   *  When the installation is complete,
      you can remove EPEL with this command.

      ``` sh
      sudo yum erase epel-release
      ```
      {:codeblock}
