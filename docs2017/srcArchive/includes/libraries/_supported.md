## Supported client libraries

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the 'Supported client libraries' topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/libraries/supported.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

### Mobile

The Cloudant Sync library is used to store, index and query local JSON data on a mobile device.
It is also used to synchronise data between many devices.
Synchronisation is controlled by your application.
The library also provides helper methods for finding and resolving conflicts,
both in the local device and the remote database.

Two versions are available:

- <a href="https://github.com/cloudant/sync-android">Cloudant Sync - Android / JavaSE</a>
- <a href="https://github.com/cloudant/CDTDatastore">Cloudant Sync - iOS (CDTDatastore)</a>

An <a href="https://cloudant.com/product/cloudant-features/sync/">overview</a> of Cloudant Sync is available, as are details of <a href="https://cloudant.com/cloudant-sync-resources/">resources</a>.

### Java

[java-cloudant](https://github.com/cloudant/java-cloudant) is the official Cloudant library for Java.

Information about installing the library by adding it as a dependency to your maven or gradle builds is available
[here](https://github.com/cloudant/java-cloudant#installation-and-usage),
along with details and examples of how to use the library.

<table>
<tr>
<th>Libraries and Frameworks</th>
<th>Examples and Tutorials</th>
</tr>
<tr>
<td>Supported:<ul><li><a href="https://github.com/cloudant/java-cloudant">java-cloudant</a></li></ul>
Unsupported:<ul><li><a href="http://ektorp.org/">ektorp</a></li>
<li><a href="http://code.google.com/p/jcouchdb/">jcouchdb</a></li>
<li><a href="https://github.com/isterin/jrelax">jrelax</a></li>
<li><a href="http://www.lightcouch.org/">LightCouch</a></li>
<li><a href="https://ace.ng.bluemix.net/#/store/cloudOEPaneId=store&appTemplateGuid=CloudantJavaBPTemplate&fromCatalog=true">Java Cloudant Web Starter</a> boilerplate for Bluemix.</li></ul>
</td>
<td><ul><li><a href="https://github.com/cloudant/haengematte/tree/master/java">CRUD</a> with HTTP and JSON libraries.</li>
<li><a href="https://github.com/cloudant/haengematte/tree/master/java/CrudWithEktorp">CRUD</a> with ektorp library.</li>
<li><a href="https://cloudant.com/blog/building-apps-using-java-with-cloudant-on-ibm-bluemix/">Building apps using Java with Cloudant on IBM Bluemix</a></li>
<li><a href="http://www.ibm.com/developerworks/cloud/library/cl-multiservicegame-app/index.html?ca=drs-">Build a game app with Liberty, Cloudant, and Single Sign On</a> Bluemix example.</li>
<li><a href="https://developer.ibm.com/bluemix/2014/10/17/building-java-ee-app-ibm-bluemix-using-watson-cloudant/">Building a Java EE app on IBM Bluemix Using Watson and Cloudant</a> Bluemix example along with <a href="https://www.youtube.com/watch?feature=youtu.be&v=9AFMY6m0LIU&app=desktop">YouTube video</a>.</li></ul>
</td>
</tr>
</table>

### Node.js

<a href="https://github.com/cloudant/nodejs-cloudant">nodejs-cloudant</a> is the official Cloudant library for Node.js. You can install it with npm:

`npm install cloudant`

<table>
<tr>
<th>Libraries and Frameworks</th>
<th>Examples and Tutorials</th>
</tr>
<tr>
<td>
<ul>
<li>
<a href="https://github.com/cloudant/nodejs-cloudant">nodejs-cloudant</a> (<a href="https://www.npmjs.org/package/cloudant">npm</a>)</li>
<a href="https://github.com/sbisbee/sag-js">sag-js</a> which also works in the browser. See <a href="http://www.saggingcouch.com/">saggingcouch</a> for more detail.</li>
<li>
<a href="https://github.com/dscape/nano">nano</a> is a minimalist implementation.</li>
<li>
<a href="https://github.com/danwrong/restler">restler</a> delivers the best performance but is really barebones.</li>
<li>
<a href="http://cloudhead.io/cradle">cradle</a> is a high-level client is also available if you absolutely need ease of use at the cost of reduced performance.</li>
<li><a href="https://github.com/ddemichele/cane_passport">cane_passport</a> - Cloudant Angular Node Express with Bootstrap.</li>
<li><a href="https://github.com/cloudant-labs/express-cloudant">express-cloudant</a> - a template for Node.js Express framework also using PouchDB and Grunt.</li>
<li><a href="https://ace.ng.bluemix.net/#/store/cloudOEPaneId=store&appTemplateGuid=nodejscloudantbp&fromCatalog=true">Node.js Cloudant DB Web Starter</a> - boilerplate for Bluemix.</li>
<li><a href="https://ace.ng.bluemix.net/#/store/cloudOEPaneId=store&appTemplateGuid=mobileBackendStarter&fromCatalog=true">Mobile Cloud</a> - boiler plate for Bluemix (Node.js, Security, Push, and Mobile Data/Cloudant)</li>
</ul>
</td>
<td>
<ul>
<li><a href="https://github.com/cloudant/haengematte/tree/master/nodejs">CRUD</a></li>
<li><a href="https://github.com/garbados/Cloudant-Uploader">Cloudant-Uploader</a> - utility to upload .csv files to Cloudant.</li>
<li><a href="https://github.com/glynnbird/couchimport">couchimport</a> - utility to import csv or tsv files into CouchDB or Cloudant</li>
<li><a href="http://thoughtsoncloud.com/2014/07/getting-started-ibm-bluemix-node-js/">Getting started with IBM Bluemix and Node.js</a></li>
<li><a href="https://gigadom.wordpress.com/2014/08/15/a-cloud-medley-with-ibm-bluemix-cloudant-db-and-node-js/">A Cloud medley with IBM Bluemix, Cloudant DB and Node.js</a></li>
<li><a href="http://www.ibm.com/developerworks/cloud/library/cl-guesstheword-app/index.html?ca=drs-">Build a simple word game app using Cloudant on Bluemix</a> - uses Node.js</li>
<li><a href="https://www.twilio.com/blog/2012/09/building-a-real-time-sms-voting-app-part-1-node-js-couchdb.html">Building a Real-time SMS Voting App</a> - six-part series using Node.js, Twilio, and Cloudant.</li>
<li><a href="http://msopentech.com/blog/2013/12/19/tutorial-building-multi-tier-windows-azure-web-application-use-cloudants-couchdb-service-node-js-cors-grunt-2/">Building a Multi-Tier Windows Azure Web application</a> - uses Cloudant, Node.js, CORS, and Grunt.</li>
<li><a href="http://www.ibm.com/developerworks/library/ba-remoteservpi-app/index.html">Do it yourself: Build a remote surveillance application using Bluemix, Cloudant, and Raspberry Pi.</a></li>
</ul>
</td>
</tr>
</table>

### Python

A supported library for working with Cloudant using Python is available [here](https://github.com/cloudant/python-cloudant).

Download the current library release [here](https://pypi.python.org/pypi/cloudant/). Learn more information about the Python language at [python.org](https://www.python.org/about/). 

### Swift

A supported library is available for working with Cloudant. The library is called SwiftCloudant, and is installed using `cocoapods`.

The Podfile entry is:

`pod 'SwiftCloudant'`

More information about SwiftCloudant, including details of installation and how to use the library to store, index, and query remote JSON data on Cloudant, is available [here](https://github.com/cloudant/swift-cloudant).

The library is an early release version. As such, it does not currently have complete Cloudant API coverage. 

<aside class="warning" role="complementary" aria-label="betaonly0">SwiftCloudant is not supported on iOS, and you cannot call it from Objective-C.</aside>


