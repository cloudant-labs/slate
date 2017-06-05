##CAP Theorem

<div id="cap_theorem"></div>
<div id="consistency"></div>

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the 'CAP Theorem' topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/guides/cap_theorem.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

Cloudant uses an '[Eventually Consistent](http://en.wikipedia.org/wiki/Eventual_consistency)' model. To understand how this works, and why it is an essential part of using Cloudant, we must first consider what is meant by Consistency.

Consistency is one of the three attributes in the CAP (**C**onsistency, **A**vailability, and **P**artition tolerance) theorem, which states that it is not possible for a distributed computer system - such as Cloudant - to simultaneously guarantee three attributes:

- Consistency, where all nodes see the same data at the same time.
- Availability, which guarantees that every request receives a response about whether it succeeded or failed.
- Partition tolerance, where the system continues to operate even if any one part of the system is lost or fails.

The impossibility of guaranteeing all three attributes means that Cloudant does not guarantee the Consistency attribute. In an eventually consistent model, like Cloudant, an update made to one part of the system is *eventually* seen by other parts of the system. As the update propagates, the system is said to 'converge' on complete consistency.

Eventual consistency is good for performance. With a strong consistency model, a system would have to wait for any updates to propagate completely and successfully before a write or update request could be completed. With an eventually consistent model, the write or update request can return almost immediately, while the propagation across the system continues 'behind the scenes'.

A database can only exhibit two of these three for both theoretical and practical reasons. A database prioritizing consistency and availability is simple: a single node storing a single copy of your data. But this is difficult to scale as you must upgrade the node to get more performance, rather than leverage additional nodes. And, even a minor system failure can shut down a single-node system, while any message loss will mean significant data loss. To endure, the system must become more sophisticated.

### Tradeoffs in Partition Tolerance

A database which prioritizes consistency and partition tolerance will commonly employ a [master-slave](http://en.wikipedia.org/wiki/Master/slave_(technology)) setup, where some node of the many in the system is elected leader. Only the leader can approve data writes, while all secondary nodes replicate data from the leader in order to handle reads. If the leader loses connection to the network, or can't communicate with a majority of the system's nodes, the majority elects a new leader. This election process will differ between systems, and can be a source of [significant problems](http://aphyr.com/posts/284-call-me-maybe-mongodb).

Cloudant prioritizes availability and partition tolerance by employing a master-master setup, such that every node can accept both writes and reads to its portion of your data. Multiple nodes contain copies of each portion of your data, with each copying data between them, so that if a node becomes inaccessible, others can serve in its place while the network heals. This way, the system will return your data in a timely manner despite arbitrary node failure, while maintaining [eventual consistency](http://en.wikipedia.org/wiki/Eventual_consistency). The tradeoff in deprioritizing absolute consistency is that it will take a moment for all nodes to see the same data, such that responses may contain old data while the new data propagates through the system.

### Changing our thinking

Maintaining one consistent view of our data is logical and easy to understand because a relational database does this work for you. We expect Web services interacting with database systems to behave this way, but that doesn't mean they should. Consistency isn't a given, and it takes a little work to change our approach.

In fact, consistency isn't necessarily essential for many enterprise cloud services. Large, heavily used systems bring with them a high probability that a portion of the system may fail. A database engineered around this assumption that prioritizes availability and eventual consistency is better suited to keeping your application online. The consistency of application data can be addressed after the fact. As Seth Gilbert and Nancy Lynch of MIT conclude, "most real-world systems today are forced to settle with returning 'most of the data, most of the time.'"

### Application availability vs. consistency in the enterprise

A look at popular Web services shows that people already expect high availability, and happily trade this for eventually consistent data, often without realizing they are doing so.

Applications have been lying to users for years for the sake of availability. Consider ATMs: inconsistent banking data is why it's still possible to overdraft money without realizing it. It is unrealistic to present a consistent view of your account balance throughout the entire banking system if every node in the network needs to halt and record this figure before continuing operations. It's better to make the system highly available.

The banking industry figured it out back in the 1980s, but many IT organizations are still worried about sacrificing consistency for the sake of availability. Think about the number of support calls placed when your sales team can't access their CRM app. Now consider if they would even notice when it takes a few seconds for a database update to propagate throughout the application.

Availability trumps consistency more than you might expect. Online shopping cart systems, HTTP caches, and DNS are a few more examples. Organizations must consider the cost of downtime: user frustration, productivity loss, missed opportunities, etc.

### From theory to implementation

Addressing high availability is vital for cloud applications. Otherwise, global database consistency will always be a major bottleneck as you scale. Highly available applications need to maintain constant contact with their data, even if that data isn't the most up-to-date. That's the concept of eventual consistency, and it's nothing to be scared of. At large scale, sometimes it's better to serve answers that are not perfectly correct than to not serve them at all.

Database systems hide the complexities of availability vs. consistency in different ways, but they are always there. The view that we take with Cloudant's database-as-a-service, along with CouchDB and other NoSQL databases, is that it's better to expose developers to these complexities early in the design process. By doing the hard work up front, there are no surprises because applications are ready to scale from day one.

