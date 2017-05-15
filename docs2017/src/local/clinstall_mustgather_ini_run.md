---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-13"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Running the MustGather tool

If you have an issue with Cloudant&reg; Local, run the MustGather
tool to collect your system data and send it to IBM&reg; Support.
{:shortdesc}

>   **Note:** You must have root privileges to run the MustGather tool.

<ol>
<li>Run the MustGather tool by using the following command.
<ol type=a>
<li>Add the root SSH private keys to all nodes, including
        database nodes and load-balancer nodes.</li>
<li>Copy the SSH public keys to the
        `/root/.ssh/authorized_keys` file.</li>
<li>Turn off `StrictHostChecking`.
<p>`mustgather --help`<br>
    `usage: mustgather [-h] [-n NODES] [-o OUTPUT_DIR]`<br>
                   <br>
    `mustgather - Gathers diagnostic data for a Cloudant cluster.`<br>
    `optional arguments:`<br>
    `-h, --help       Show this help message and exit.`<br>
    `-n  NODES        Comma-separated list of host names for the cluster nodes that you can configure as`<br>
                    `the list of nodes for MustGather to use.`<br>
    `-k KEY_FILE      The SSH private key file. If the SSH key is not in the` <br>
                    `default ~/.ssh directory, you can specify this option, for example,` <br>
                    `~/sample/id_rsa.`<br>
    `-o  OUTPUT_DIR   Directory where the output tar file is created.`</p></li></ol>
</li>
<li>Run the MustGather tool with option `-n` or option `-o`.

<ol type=a>
<li>Update the `mustgather.ini` file to specify the nodes with
        option `-n`. 
<ul><li>Specify the `-n` option the first time you run the
            MustGather tool.</li>
<li>Do not specify option `-n` for any subsequent runs
            unless the node information changes from the previous
            run.</li></ul>
</li>
<li>Update the `mustgather.ini` file to specify the nodes with
        option `-o`.
<ul><li>The `mustgather.tar` file is saved to the output
           directory when option `-o` is specified.</li>
<li>The `mustgather.tar` file is saved to the current
            directory when option `-o` is not specified.</li></ul></li></ol>
<li>After you run the tool, send the `tar` file to IBM support.</li>
</ol>

