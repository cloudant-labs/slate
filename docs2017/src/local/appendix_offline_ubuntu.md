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

# Installing Ubuntu dependencies

Retrieve the Ubuntu dependencies from the Ubuntu online system.
{:shortdesc}

1.  Log in to the Ubuntu online system.

2.  Retrieve the dependencies required by the self-extracting archive/CAST tool.
    
    ``` sh
    apt-get update
    apt-get download apt-offline python-apt
    dpkg -i apt-offline*
    apt-offline set cast-deps.sig --install-packages openjdk-6-jre python-pip iptables-persistent python-pip-whl fgetty runit curl
    apt-offline get cast-deps.sig --no-checksum -d cloudant-deps
    ```
    {:codeblock}

3.  Run the self-extracting archive.
    
    ``` sh
    ./cloudant-<version>-<os>-<arch>.bin
    ```
    {:codeblock}

4.  Retrieve the remaining dependencies that are required by the self-extracting archive/CAST tool.
    
    ``` sh
    apt-offline set cloudant-deps.sig --install-packages cloudant-lbnode cloudant-dbnode
    apt-offline get cloudant-deps.sig --no-checksum -d cloudant-deps
    rm cloudant-deps/*cloudant*
    tar -czvf cloudant-deps.tar.gz cloudant-deps
    ```
    {:codeblock}

5.  Copy the self-extracting archive and all its dependencies to the offline system.
    
    ``` sh
    scp python-apt* offline.system.com:/tmp
    scp cloudant-deps.tar.gz offline.system.com:/tmp
    scp cloudant-version-os-arch.bin offline.system.com:/tmp
    ```
    {:codeblock}

6.  Log in to the offline system.

7.  Install the Cloudant dependencies.
    
    ``` sh
    cd /tmp
    tar -xvf cloudant-deps.tar.gz
    dpkg -i cloudant-deps/*
    ```
    {:codeblock}
