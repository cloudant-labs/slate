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

# Troubleshooting a remote logging configuration

If the source is configured to send log messages to a remote
logging server, but the messages are not seen in the logs, run
the following checks.
{:shortdesc}

<ol><li>Ensure that the `syslog` facility property is configured on the source by checking the source log configuration file.

<ol type="a"><li>Check the configuration on the remote logging server by inspecting the `/etc/rsyslog.conf` or `/etc/rsyslog.d/*.conf` files to see where facility writes the log.</li>
<li>Ensure that the facility values are not in conflict with the different types of logs.
    
<p>You can use different facility values from `local2` through
        to `local7` inclusive. For more information about facility
        values, see <a href="http://tools.ietf.org/html/rfc3164#section-4.1.1" target="_blank">RFC 3164 <img src="images/launch-glyph.svg" alt="External link icon"></a>.
        The following table lists the values that are used by Cloudant&reg; Local.</p>

 <p>       
        <table>
        <thead>
        <tr>
        <th>Facility</th>
        <th>Purpose</th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <td>`local2`</td>
        <td>Cloudant database logs</td>
        </tr>
        <tr>
        <td>`local3`</td>
        <td>Metrics logs</td>
        </tr>
        <tr>
        <td>`local4`</td>
        <td>HAProxy logs</td>
        </tr>
        <tr>
        <td>`local5`</td>
        <td>Clouseau logs</td>
        </tr>
        </tbody>
        </table>
        </p>
</li></ol></li>
<li>Change the logging level, on the source nodes, to `info` temporarily to generate more logging activity.</li> 
<li>After you complete your verification checks, remember to change the logging level back to the default or your preferred level.</li>
<li>Confirm that the UDP port (default port = 514) that is used for remote logging is open on the remote syslog server.

<ol type="a"><li>Modify the port by changing the value of the `UDPServerRun` entry in the `/etc/rsyslog.conf` file.</li>
<li>Confirm that the port value is the same port that the source nodes use to send log messages.</li>
</li></ol></li>
<li>Verify that log messages are sent by the source node, and received by the log server, through the configured port.
<ol type="a"><li>Use a network monitoring tool such as `tcpdump` to check.</li>
<li>Use the tool on the source and log servers, and monitor or sniff the logging port.

    <p>If you use `tcpdump` to monitor outgoing traffic on the default log port, 514, you can expect to see results similar to the following example.
    
        ```
        [root@db2 tmp]# sudo tcpdump -n -s 1500 -X port 514
    
        14:33:01.995812 IP 104.131.89.154.58467 > 104.131.35.26.syslog: SYSLOG local2.notice, length: 221
        0x0000:  4500 00f9 0000 4000 4011 ec39 6883 599a  E.....@.@..9h.Y.
        0x0010:  6883 231a e463 0202 00e5 4eb1 3c31 3439  h.#..c....N.&lt;149
        .....
        0x0090:  5d20 636c 6f75 6461 6e74 4064 6232 2e61  ].cloudant@db2.a
        0x00a0:  6e75 6a2e 6365 6e74 6f73 2e63 6c6f 7564  nuj.centos.cloud
        0x00b0:  616e 742d 6c6f 6361 6c2e 636f 6d20 3c30  ant-local.com.&lt;0
        0x00d0:  6120 3130 342e 3133 312e 3335 2e32 3620  a.104.131.35.26.
        0x00e0:  756e 6465 6669 6e65 6420 4745 5420 2f20  undefined.GET./.
        0x00f0:  3230 3020 6f6b 2033 0a                   200.ok.3.
        ```
  </p>      
<p>In this example, the database node logs are being monitored, by watching for traffic that is associated with the facility `local2`.</p>

<p>If you are monitoring the incoming traffic on the log server at the same time, you can expect to see results similar to the following example.

        ```sh
        [root@lb1 tmp]# sudo tcpdump -n -s 1500 -X port 514
        tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
        listening on eth0, link-type EN10MB (Ethernet), capture size 1500 bytes
        14:33:02.193469 IP 104.131.89.154.58467 > 104.131.35.26.syslog: SYSLOG local2.notice, length: 221
        0x0000:  4500 00f9 0000 4000 3f11 ed39 6883 599a  E.....@.?..9h.Y.
        0x0010:  6883 231a e463 0202 00e5 777d 3c31 3439  h.#..c....w}&lt;149
        ......
        0x0070:  2032 3031 342d 3130 2d30 3320 3134 3a33  .2014-10-03.14:3
        0x0090:  5d20 636c 6f75 6461 6e74 4064 6232 2e61  ].cloudant@db2.a
        0x00a0:  6e75 6a2e 6365 6e74 6f73 2e63 6c6f 7564  nuj.centos.cloud
        0x00b0:  616e 742d 6c6f 6361 6c2e 636f 6d20 3c30  ant-local.com.&lt;0
        0x00e0:  756e 6465 6669 6e65 6420 4745 5420 2f20  undefined.GET./.
        0x00f0:  3230 3020 6f6b 2033 0a                   200.ok.3.
        ```
</p>
<p><b>Note:**</b> Other enterprise services might be sending messages to the log server through the same port. When you verify incoming traffic on the logging server, check which node or server the message came from.</p>
</li></ol></li>
<li>Edit `/etc/rsyslog.conf` and disable any other default rules that can cause log duplication. Log duplication occurs when log messages are written to multiple files.</li>
<li>If it is not configured, enable automatic log rotation by using `logrotate`.

<p>More information about `logrotate` is available at
    <a href="http://linux.die.net/man/8/logrotate" target="_blank">http://linux.die.net/man/8/logrotate <img src="images/launch-glyph.svg" alt="External link icon"></a>. Use output channel
    scripts instead of `logrotate`, see more information here,
    <a href="http://www.rsyslog.com/doc/log_rotation_fix_size.html" target="_blank">http://www.rsyslog.com/doc/log_rotation_fix_size.html <img src="images/launch-glyph.svg" alt="External link icon"></a>.</p>
    </li></ol>


