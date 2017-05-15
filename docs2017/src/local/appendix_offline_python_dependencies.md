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

# Installing Python dependencies

After you transfer the third-party dependencies, you must
transfer the Python dependencies from the online system.
{:shortdesc}

>   **Note:** You must apply these steps to each platform in your environment.

1.  Download and install the `pip2pi` Python module to create a local PyPI repository.
    
    ``` sh
    pip install pip --upgrade
    pip install pip2pi
    ```
    {:codeblock}

2.  Create a text file named `requirements.txt`.

3.  Add the Python module to the `requirements.txt` file.

    ``` sh
    pip==9.0.1
    virtualenv==15.0.3
    wheel==0.29.0
    ```
    {:codeblock}

4.  Download and create the `PyPi` simple repository.
    
    ``` sh
    mkdir cloudant-python-deps
    pip2pi cloudant-python-deps -r requirements.txt
    ```
    {:codeblock}

5.  Bundle the PyPI repository into a compressed (tar) file.

    ``` sh
    tar -czvf cloudant-python-deps.tar.gz cloudant-python-deps
    ```
    {:codeblock}

6.  Copy the files to the offline system.

    ``` sh
    scp cloudant-python-deps.tar.gz offline.system.com:/tmp
    ```
    {:codeblock}

7.  Log in to the offline system.

8.  Setup the local PyPI repository.

    ``` sh
    cd /tmp
    tar -xvf cloudant-python-deps.tar.gz
    
    mkdir ~/.pip
    echo "[global]" > ~/.pip/pip.conf
    echo "index-url = file:///tmp/cloudant-python-deps/simple" >> ~/.pip/pip.conf
    ```
    {:codeblock}
