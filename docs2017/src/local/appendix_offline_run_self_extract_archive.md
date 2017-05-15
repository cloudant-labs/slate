---

copyright:
years: 2017
lastupdated: "2017-03-01"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Running the Cloudant self-extracting archive</title>

After you install all the dependencies on the offline system,
you must run the self-extracting archive.
{:shortdesc}

1.  Log in to the offline system.

2.  Transfer the self-extracting archive.

    ``` sh
    scp cloudant-version-os-arch.bin offline.system.com:/tmp
    ```
    {:codeblock}

3.  Run the self-extracting archive.

    ``` sh
    cd /tmp
    ./cloudant-<version>-<os>-<arch>.bin
    ```
    {:codeblock}

4.  Only perform this step on an Ubuntu system.</cmd>
    
    ``` sh
    cd /tmp
    dpkg -x python-apt* apt
    cp -r apt/usr/* /opt/cloudant/cast/venv
    ```
    {:codeblock}
