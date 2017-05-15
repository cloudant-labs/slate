---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-10"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Setting up remote access for the rebalancer

The rebalancer runs on the load balancer. It needs SSH access to
the database nodes to run the operations that are required to
move shards between database nodes. The Cloudant&reg; Local installer
creates a `cloudantrebal` user account on every database node in
your cluster for the rebalancer. During installation, this
account is configured with the permissions and path that are
required to do the operations that the rebalancer requires with
SSH. The `cloudantrebal` account eliminates some of the work an
operator must do to set up a cluster rebalance.
{:shortdesc}



<ol>
<li>On the load balancer, as a root user, generate a pair of
    public and private keys for SSH access to the rebalancer.
<p>`>  cd ~/.ssh`<br>
`>  ssh-keygen -t rsa`</p>
<ol type=a>
<li>Enter a name for the key file, or leave it as the default.</li>
<li>Record the passphrase that you enter for the key creation. 
<p>The result is to produce two key files in the `~/.ssh` folder.</p>
<ul><li>A private key file with the default name `id_rsa`.</li>
<li>A public key file with the default name `id_rsa.pub`.</li></ul>
</li>
</ol>
</li>
<li>Add the public and private keys to every database node in your cluster.
<p>**Note:** The controlling node is defined as the node where you run `rebal` (in this case your load balancer). The new node is the database node that you just added to the cluster.</p>
</li>
<li>Set up the public and private keys.
<p>**Note:** The `rebal` uses SSH to communicate between the controlling node and the database nodes (existing and new). It also communicates between nodes when `rsync` shards from existing database nodes to the new node.</p>
<ol type=a>
<li>Create an `authorized_keys` file in `/opt/cloudantrebal/.ssh`.</li>
<li>Add the public key to the `/opt/cloudantrebal/.ssh/authorized_keys` file on all the database nodes, including the one you are adding.</li>
<li>Copy the public and private keys to `/opt/cloudantrebal/.ssh`.</li>
<li>Ensure that the `owner:group` is `cloudantrebal:Cloudant`.
<p>The private key has permission, `0600`, and the public key has permission, `0644`. See the following example.</p>
<p>`cloudantrebal@db1:~/.ssh$ ls -la`<br>
        `total 20`<br>
        `drwxr-xr-x 2 cloudantrebal cloudant 4096 Mar 27 23:57 .`<br>
        `drwxr-xr-x 3 cloudantrebal cloudant 4096 Mar 27 23:57 ..`<br>
        `-rw-r--r-- 1 cloudantrebal cloudant  395 Mar 27 23:57 authorized_keys`<br>
        `-rw------- 1 cloudantrebal cloudant 1675 Mar 27 23:57 id_rsa`<br>
        `-rw-r--r-- 1 cloudantrebal cloudant  395 Mar 27 23:57 id_rsa.pub`</p></li>
<li>Test that you can SSH from your existing database nodes to the new node by using the following command.
<p>`cloudantrebal@db1:~/.ssh$ ssh new-db-node.example.com`</p></li>
</ol>
</li>
<li>On the load balancer, create the following entry in the
    `~/.ssh/config` file for the account that you are using to run
    the rebalancer.
<p>`Host *.yourcluster.yourdomain.com`<br>
    `User cloudantrebal`</p></li>
<li>If you use `ssh-agent` to manage the SSH credentials for the
    rebalancer, ensure that you specify the private key by
    providing the file name to `ssh-add`.
<p>`>  eval $(ssh-agent)`<br>
    `>  ssh-add ~/.ssh/id_rsa`</p></li>
<li>Enter the passphrase of the key when prompted.
<p>**Note:** When you enter the passphrase for the key, the passphrase is saved for the current `ssh` session. You run the commands again if you open a new `ssh` session on the load balancer, for example, when you run the rebalance shards scripts in subsequent steps.</p>
</li>
<li>Confirm that the database nodes are accessible with SSH from the load balancer, such as by configuring `ssh-agent`.</li>
<li>Verify the access by trying to SSH into all database nodes
    from the load balancer.</li>
</ol>


1.  On the load balancer, as a root user, generate a pair of
    public and private keys for SSH access to the rebalancer.

    ``` sh
    >  cd ~/.ssh
    >  ssh-keygen -t rsa
    ```
    {:codeblock}

    a.  Enter a name for the key file, or leave it as the default.

    b.  Record the passphrase that you enter for the key creation. 
    The result is to produce two key files in the `~/.ssh` folder.

    *   A private key file with the default name `id_rsa`.
    *   A public key file with the default name `id_rsa.pub`.

2.  Add the public and private keys to every database node in your cluster.

    >   **Note:** The controlling node is defined as the node where you run `rebal` (in this case your load balancer). The new node is the database node that you just added to the cluster.

3.  Set up the public and private keys.

    >   **Note:** The `rebal` uses SSH to communicate between the controlling node and the database nodes (existing and new). It also communicates between nodes when `rsync` shards from existing database nodes to the new node.

    a.  Create an `authorized_keys` file in `/opt/cloudantrebal/.ssh`.

    b.  Add the public key to the `/opt/cloudantrebal/.ssh/authorized_keys` file on all the database nodes, including the one you are adding.

    c.  Copy the public and private keys to `/opt/cloudantrebal/.ssh`.

    d.  Ensure that the `owner:group` is `cloudantrebal:Cloudant`.
    The private key has permission, `0600`, and the public key has permission, `0644`. See the following example.

        ``` sh
        cloudantrebal@db1:~/.ssh$ ls -la
        total 20
        drwxr-xr-x 2 cloudantrebal cloudant 4096 Mar 27 23:57 .
        drwxr-xr-x 3 cloudantrebal cloudant 4096 Mar 27 23:57 ..
        -rw-r--r-- 1 cloudantrebal cloudant  395 Mar 27 23:57 authorized_keys
        -rw------- 1 cloudantrebal cloudant 1675 Mar 27 23:57 id_rsa
        -rw-r--r-- 1 cloudantrebal cloudant  395 Mar 27 23:57 id_rsa.pub
        ```
        {:codeblock}

    e.  Test that you can SSH from your existing database nodes to the new node by using the following command.

        ``` sh
        cloudantrebal@db1:~/.ssh$ ssh new-db-node.example.com
        ```
        {:codeblock}

4.  On the load balancer, create the following entry in the
    `~/.ssh/config` file for the account that you are using to run
    the rebalancer.

    ``` sh
    Host *.yourcluster.yourdomain.com
    User cloudantrebal
    ```
    {:codeblock}

5.  If you use `ssh-agent` to manage the SSH credentials for the
    rebalancer, ensure that you specify the private key by
    providing the file name to `ssh-add`.

    ``` sh
    >  eval $(ssh-agent)
    >  ssh-add ~/.ssh/id_rsa
    ```
    {:codeblock}

6.  Enter the passphrase of the key when prompted.

>   **Note:** When you enter the passphrase for the key, the passphrase is saved for the current `ssh` session. You run the commands again if you open a new `ssh` session on the load balancer, for example, when you run the rebalance shards scripts in subsequent steps.

7.  Confirm that the database nodes are accessible with SSH from the load balancer, such as by configuring `ssh-agent`.

8.  Verify the access by trying to SSH into all database nodes
    from the load balancer.
