# Installing and using the local build tool

## Changelog

### 2017-04-19

Updated VirtualBox requirement to 5.1.18.
Updated Vagrant image to latest Bluemix build tool.
Updated Vagrant image with latest security patches.

### 2017-03-13

Updated VirtualBox requirement to 5.1.16.

### 2017-03-08

Updated Vagrant image to latest Bluemix build tool.
Updated Vagrant image with latest security patches.

### 2017-02-10

Updated Vagrant image with latest security patches.

### 2017-01-31

Updated Vagrant image to latest Bluemix build tool.
Updated Vagrant image with latest security patches.

### 2017-01-24

Updated Vagrant image to latest Bluemix build tool.
Updated Vagrant image with latest security patches.

### 2017-01-18

Updated VirtualBox requirement to 5.1.14.

## Pre-requisites

1.  Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
    Ensure you have at least version 5.1.16, or more recent.

2.  Download and install [Vagrant](https://www.vagrantup.com/downloads.html).
    Ensure you have at least version 1.8.5, or more recent.

    >   **Note**: On the Mac, Vagrant version 1.8.7 has a known issue. Check that you are running a more recent version of Vagrant on the Mac.

## Obtaining the tool

The main component is the Vagrant image 'docs2017builder'.

1.  Open the IBM Box folder:
    [https://ibm.ent.box.com/folder/15060512246](https://ibm.ent.box.com/folder/15060512246)
    ... in a browser.

2.  Download the newest `docs2017builder-YYYYMMDD.box` file.

3.  Open a terminal, and browse to the location where you downloaded the `docs2017builder-YYYYMMDD.box` file.

4.  Run the following command:

    ```
    vagrant box add --name mybuilder --force docs2017builder-YYYYMMDD.box
    ```
    
    (The `--force` option makes it easier to update the Vagrant image at a later date.)

5.  <div id="newday"></div>Change to the directory with the documentation source.
    It should have a `Vagrantfile` present.

6.  Check that the `Vagrantfile` has the following text at line 15:

    ```
    config.vm.box = "mybuilder"
    ```

    >   **Note**: The check is purely to make sure that we are in the correct folder.

7.  Run the following command:

    ```
    vagrant up --provider=virtualbox
    ```

    After a short delay, the prompt returns in the terminal window.

8.  Connect to the build system, by running the following command:

    ```
    vagrant ssh
    ```

    You are now connected to the Vagrant system.

9.  Change to the `/vagrant` folder in the build system, by running the following command:

    ```
    cd /vagrant
    ```

    If you do an `ls` at this point, you'll see the normal files and folders
    present in your build directory.

10. For the Cloudant docs,
    a simple build script is present in the `scripts` folder,
    so change to it:

    ```
    cd /vagrant/scripts
    ```

    You can now run the two main build tasks whenever you want, _within_ the build system:

    -   `make clean` - to remove the `/vagrant/build` folder.
    -   `make html` - to build the HTML files from the Bluemix markdown source,
        and store the results in the`/vagrant/build` folder.

11. When you have finished for the day, simply exit from the Vagrant build system:

    ```
    exit
    ```

    You are now back at the normal operating system prompt within the terminal window.

12. To 'switch off' the Vagrant machine, run the following command:

    ```
    vagrant halt
    ```

    When you want to start working again,
    simply bring up the Vagrant machine again ([step 5](#newday)).

## Updating the Vagrant image

From time-to-time,
a fresh image is made available.
This could be because the build tooling has been updated,
or components updated within the Vagrant image itself.

When a new image is available,
update your build environment by doing the following steps:

1.  'Switch off' any running Vagrant machine, by running the following command:

    ```
    vagrant halt
    ```
2.  Remove the old Vagrant machine, by running the following command:
    
    ```
    vagrant destroy
    ```
    
    This does _not_ damage your source files in any way.
    It simply removes the old Vagrant machine from your system.

3.  Proceed with [downloading and installing the new image](#obtaining-the-tool),
    as if this is a fresh installation.