## Third-party client libraries

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the 'Third-party client libraries' topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/libraries/thirdparty.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

<aside class="warning" role="complementary" aria-label="notmaintained2">Third-party client libraries are not maintained or supported by Cloudant.</aside>

### Third-party Mobile libraries

Working with a Cloudant database: <a href="http://www.tricedesigns.com/2014/11/17/ibm-worklight-powered-native-objective-c-ios-apps/">IBM Worklight Powered Native Objective-C iOS Apps</a> with a Cloudant Adapter.

### C# / .NET

<a href="https://github.com/danielwertheim/mycouch">MyCouch</a> is an asynchronous CouchDB and Cloudant client for .Net.

To install the library, open up the Package manager console, and invoke:

`install-package mycouch.cloudant`

<table>
<tr>
<th>Libraries and Frameworks</th>
<th>Examples and Tutorials</th>
</tr>
<tr>
<td><ul>
<li><a href="https://github.com/danielwertheim/mycouch">MyCouch</a></li>
<li><a href="https://github.com/soitgoes/LoveSeat">LoveSeat</a></li>
<li><a href="https://github.com/foretagsplatsen/Divan">Divan</a></li>
<li><a href="https://github.com/arobson/Relax">Relax</a></li>
<li><a href="http://code.google.com/p/relax-net/">Hammock</a></li>
<li><a href="https://github.com/hhariri/EasyCouchDB">EasyCouchDB</a></li>
<li><a href="http://code.google.com/p/skitsanoswdk/source/browse/#svn%2Ftrunk%2FWDK10%2FWDK.API.CouchDb">WDK.API.CouchDB</a> from <a href="http://kanapeside.com/">Kanapes IDE</a>.</li>
</td>
<td>
<ul><li><a href="https://github.com/cloudant/haengematte/tree/master/c%23">CRUD</a></li></ul>
</td>
</tr>
</table>

### PHP

[Sag](http://www.saggingcouch.com/) is PHP's CouchDB and Cloudant client. [Sag.js](https://github.com/sbisbee/sag-js) is Sag's JavaScript counterpart.

To install, download sag from [http://www.saggingcouch.com/download.php](http://www.saggingcouch.com/download.php) then include the library in your application:

`require_once('./src/Sag.php');`

<table>
<tr>
<th>Libraries and Frameworks</th>
<th>Examples and Tutorials</th>
</tr>
<tr>
<td>
<ul>
<li><a href="http://www.saggingcouch.com/">sag</a></li>
<li><a href="https://github.com/doctrine/couchdb-client">Doctrine CouchDB Client</a></li>
<li><a href="https://github.com/dready92/PHP-on-Couch">PHP-on-Couch</a></li>
</ul>
</td>
<td>
<ul>
<li><a href="https://github.com/cloudant/haengematte/tree/master/php">CRUD</a></li>
</ul>
</td>
</tr>
</table>

### JavaScript

<a href="http://pouchdb.com/">PouchDB</a> is a JavaScript database that can sync with Cloudant, meaning you can make your apps offline-ready just by using PouchDB. For more info, see [our blog post](https://cloudant.com/blog/pouchdb) on PouchDB.

To obtain PouchDB, and for setup details, refer to <a href="http://pouchdb.com/">PouchDB</a>.

<aside class="notice" role="complementary" aria-label="nodejs">PouchDB is also available for Node.js: `npm install pouchdb`</aside>

<aside class="notice" role="complementary" aria-label="bower">PouchDB can also be installed with Bower: `bower install pouchdb`</aside>

<table>
<tr>
<th>Libraries and Frameworks</th>
<th>Examples and Tutorials</th>
</tr>
<tr>
<td><ul>
<li><a href="https://github.com/cloudant-labs/backbone.cloudant">Backbone.cloudant</a> See the <a href="https://cloudant.com/blog/backbone-and-cloudant/">blog post</a> for more information.</li>
<li><a href="http://www.saggingcouch.com/jsdocs.php">sag.js</a></li>
<li><a href="http://pouchdb.com/">PouchDB</a> - JavaScript database for browser, with offline synchronization.</li>
</ul>
</td>
<td>
<ul>
<li><a href="https://github.com/cloudant/haengematte/tree/master/javascript-jquery">CRUD</a> using jQuery.</li>
<li><a href="https://github.com/michellephung/CSVtoCloudant">CSVtoCloudant</a> - UI for importing .csv files into Cloudant. The app can also be accessed <a href="https://michellephung.github.io/CSVtoCloudant/">here</a>.</li>
<li><a href="https://github.com/Mango-information-systems/csv2couchdb">csv2couchdb</a> - UI from Mango Systems to import .csv files to CouchDB/Cloudant.</li>
<li><a href="https://github.com/millayr/songblog">songblog</a> - example app using JQuery.</li>
<li><a href="http://pouchdb.com/getting-started.html">PouchDB Getting Started Guide</a> - example Todo application that syncs from browser to Cloudant or CouchDB.</li>
<li><a href="https://github.com/rajrsingh/locationtracker">locationtracker</a> - example app to record and map location using PouchDB, CouchApp, and Cloudant.</li>
</ul>
</td>
</tr>
</table>

### Ruby

[CouchRest](https://github.com/couchrest/couchrest) is a CouchDB and Cloudant client with extensions for working with Rails using [CouchRest Model](https://github.com/couchrest/couchrest_model).

To install CouchRest, run the command:

`gem install couchrest`

<table>
<tr>
<th>Libraries and Frameworks</th>
<th>Examples and Tutorials</th>
</tr>
<tr>
<td>
<ul>
<li>There are many CouchDB clients listed on <a href="https://www.ruby-toolbox.com/categories/couchdb_clients">Ruby Toolbox</a>.</li>
</ul>
</td>
<td>
<ul>
<li><a href="https://github.com/cloudant/haengematte/tree/master/ruby">CRUD</a></li>
</ul>
</td>
</tr>
</table>


<div id="couchdb"></div>

### Meteor

<a href="https://atmospherejs.com/cloudant/couchdb">cloudant:couchdb</a> is the Cloudant library for the couchdb-meteor package. Since Apache CouchDB does not ship with Meteor or the couchdb package, you must provide a URL for Meteor to connect to and a running CouchDB or Cloudant server instance before you install Meteor. Add this package to your Meteor application:

`meteor add cloudant:couchdb`

The couchdb-meteor package provides:

+ Livequery implementation and real-time updates from the database by consuming the CouchDB `_changes` feed
+ Distributed Data Protocol (DDP) RPC endpoints that update data from clients connected locally
+ Serialization and deserialization of updates to the DDP format

**Note**: The JSON query syntax used by Cloudant Query, and initially developed by Cloudant, was contributed back to Apache CouchDB for version 2.0. Pre-built binaries for Apache CouchDB version 2.0 are not yet available. You can use this module with Cloudant DBaaS or Cloudant Local until the pre-built binaries are available.

To configure the Apache CouchDB or Cloudant server connection information, pass its URL as the COUCHDB_URL environment variable to the Meteor server process.

`$export COUCHDB_URL=https://<account>.cloudant.com`

See [API Reference](api.html) for more information about meteor-couchdb APIs. 

### Apache Spark

[spark-cloudant](https://github.com/cloudant-labs/spark-cloudant) is the official Cloudant library for Apache Spark.

The spark-cloudant library is already loaded into the [IBM Bluemix Apache Spark-as-a-Service](https://console.ng.bluemix.net/catalog/services/apache-spark/) offering.
It can be used with any stand-alone Spark cluster.

See the [project information](https://github.com/cloudant-labs/spark-cloudant)
and [Spark Packages](https://spark-packages.org/package/cloudant-labs/spark-cloudant) for more details.


