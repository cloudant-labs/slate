## Javascript

### nodejs-cloudant

[nodejs-cloudant](https://github.com/cloudant/nodejs-cloudant) is the officially supported Cloudant library for Node.js. You can install it with `npm`:

The best way to use the Cloudant client is to begin with your own Node.js project, and define it as a dependency in your `package.json`. The `npm` tool can do this for you, from the command line:

```shell
npm install --save cloudant
```

Notice that your package.json will now reflect this package. Everything is working if you can run this code without errors:

<pre class="thebe">
require("cloudant");
console.log("Cloudant works");
</pre>

As you can see, you can run and edit these code snippets right on this website.

#### Getting Started

Now it's time to begin doing real work with Cloudant and Node.js.

Initialize your Cloudant connection by supplying your *account* and *password*, and supplying a callback function to run when everything is ready.

<pre class="thebe">
// Load the Cloudant library.
var Cloudant = require('cloudant');

var username = 'docs-playground'; // Set this to your own account
var password = 'docs-playground'; // Set this to your own password

// Initialize the library with the account.
var cloudant = Cloudant({account:username, password:password});

// Get all databases
cloudant.db.list(function(err, allDbs) {
  if (err) {
    console.log(err);
  } else {
    console.log('All databases: %s', allDbs.join(', '));
  }
});
</pre>

Possible output (depending on your databases, of course):

     All my databases: example_db, jasons_stuff, scores

Upper-case `Cloudant` is the package you load using `require()`, while lower-case `cloudant` represents an authenticated, confirmed connection to your Cloudant service.

If you omit the "password" field, you will get an "anonymous" connection: a client that sends no authentication information (no passwords, no cookies, etc.)

Here is simple but complete example of working with data:

<pre class="thebe" id="nodejs-example-alice">
// Load the Cloudant library.
var Cloudant = require('cloudant');

// Initialize Cloudant with your credentials
var username = 'your username';
var password = 'your password';
var dbname = 'alice'; //change this if you already have a database called alice
var cloudant = Cloudant({account:username, password:password});

// Remove any existing database with that name.
cloudant.db.destroy(dbname, function(err) {

  // Create a new database.
  cloudant.db.create(dbname, function() {

    // Specify the database we are going to use (e.g. alice)...
    var alice = cloudant.db.use(dbname)

    // ...and insert a document in it.
    alice.insert({ crazy: true }, 'rabbit', function(err, body, header) {
      if (err) {
        return console.log('[alice.insert] ', err.message);
      }
      console.log('You have inserted the rabbit.');
      console.log(body);
    });
  });
});
</pre>

If you run this example, you will see:

```
You have inserted the rabbit.
{ ok: true,
  id: 'rabbit',
  rev: '1-6e4cb465d49c0368ac3946506d26335d' }
```

You can find a further CRUD example in the [example](https://github.com/cloudant/nodejs-cloudant/tree/master/example) directory of this project.

#### Initialization

To use Cloudant, `require('cloudant')` in your code. That will return the initialization function. Run that function, passing your account name and password, and an optional callback. (And see the [security note](#security-note) about placing your password into your source code.

In general, the common style is that `Cloudant` (upper-case) is the **package** you load; wheareas `cloudant` (lower-case) is your connection to your database--the result of calling `Cloudant()`:

```javascript
var Cloudant = require('cloudant');
var cloudant = Cloudant({account:me, password:password});
```

If you would prefer, you can also initialize Cloudant with a URL:

```javascript
var Cloudant = require('cloudant');
var cloudant = Cloudant("https://MYUSERNAME:MYPASSWORD@MYACCOUNT.cloudant.com");
```

You can optionally provide a callback to the Cloudant initialization function. This will make the library automatically "ping" Cloudant to confirm the connection and that your credentials work.

Here is a simple example of initializing asychronously, using its optional callback parameter:

<pre class="thebe">
var Cloudant = require('cloudant');
var username = 'nodejs'; // Replace with your account.
var password = ''; // Put your password here
var dbname = 'alice';

Cloudant({account:username, password:password}, function(err, cloudant) {
  if (err) {
    return console.log('Failed to initialize Cloudant: ' + err.message);
  }

  var db = cloudant.db.use(dbname);
  db.get("alice", function(err, data) {
    // The rest of your code goes here. For example:
    if (err) {
      console.log(err);
    } else {
      console.log("Found Alice:", data);
    }
  });
});
</pre>

#### Callback Signature

After initialization, in general, callback functions receive three arguments:

* `err` - the error, if any
* `body` - the http _response body_ from Cloudant, if no error.
* `header` - the http _response header_ from Cloudant, if no error

The `ping()` function is the only exception to this rule. It does not return headers since a "ping" is made from multiple requests to gather various bits of information.

#### Password Authentication

By default, when you connect to your cloudant account (i.e. "account.cloudant.com"), you authenticate as the account owner (i.e. "account"). However, you can use Cloudant with any username and password. Just provide an additional "username" option when you initialize Cloudant. This will connect to your account, but using the username as the authenticated user. (And of course, use the appropriate password.)

<pre class="thebe">
var Cloudant = require('cloudant');
var account = "nodejs";         // Substitute with your Cloudant user account.
var otherUsername = "jhs"; // Substitute with some other Cloudant user account.
var otherPassword = process.env.other_cloudant_password;

Cloudant({account:account, username:otherUsername, password:otherPassword}, function(er, cloudant, reply) {
  if (er) {
    throw er;
  }

  console.log('Connected with username: %s', reply.userCtx.name);
});
</pre>

### PouchDB

<a href="http://pouchdb.com/">PouchDB</a> is a JavaScript database that runs in the browser and in Node.js and can sync with Cloudant, meaning you can make your apps offline-ready just by using PouchDB. For more info, see [our blog post](https://cloudant.com/blog/pouchdb) on PouchDB. Cloudant does not provide support for PouchDB.

To obtain PouchDB, and for setup details, refer to <a href="http://pouchdb.com/">PouchDB</a>.

<aside class="notice">PouchDB is also available for Node.js: `npm install pouchdb`</aside>

<aside class="notice">PouchDB can also be installed with Bower: `bower install pouchdb`</aside>

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

#### Related links

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
<a href="http://cloudhead.io/cradle">cradle</a> is a high-level client is also available if you absolutely need ease of use at the cost of lower performance.</li>
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
<li><a href="http://www.ibm.com/developerworks/library/ba-remoteservpi-app/index.html">Do it yourself: Build a remote surveillance app using Bluemix, Cloudant, and Raspberry Pi.</a></li>
</ul>
</td>
</tr>
</table>
