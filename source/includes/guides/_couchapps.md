## CouchApps

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the CouchApps topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/guides/couchapps.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

Because Cloudant can host raw file data, like images, and serve them
over HTTP, then theoretically it can host all the static files necessary
to run a website, and host them just like a web server. Because these
files would be hosted on Cloudant, the client-side JavaScript could
access Cloudant databases. An application built this way is said to have
a two-tier architecture, consisting of the client -- typically a browser
-- and the database. In the CouchDB community, this is called a
CouchApp.

Most web apps have three tiers: the client, the server, and the
database. Placing the server inbetween the client and the database can
help with authentication, authorization, asset management, leveraging
third-party web APIs, providing particularly sophisticated endpoints,
etc. This separation allows for added complexity without conflating
concerns, so your client can worry first and last about data
presentation, while your database can focus on storing and serving data.

CouchApps shine in their simplicity, but frequently a web app will need
the power of a 3-tier architecture. When is each appropriate?

### A CouchApp is appropriate if...

-   Your server would have only provided an API to Cloudant anyway.
-   You're OK using Cloudant's [cookie-based
    authentication](http://docs.cloudant.com/api/authn.html).
-   You're OK using Cloudant's [\_users and
    \_security](https://cloudant.com/for-developers/faq/auth/) databases
    to manage users and permissions.
-   You don't need to schedule cronjobs or other regular tasks.

To get started with CouchApps, read [Managing applications on
Cloudant](https://cloudant.com/blog/app-management/).

### A 3-tier application is appropriate if...

-   You need finer-grained permissions than the `_security` database
    allows.
-   You need an authentication method other than Basic auth or cookie
    authentication, such as Oauth or a 3rd-party login system.
-   You need to schedule tasks outside the client to run regularly.

You can write your server layer using whatever technologies work best
for you. We keep a list of libraries for working with Cloudant here:
[Developing on
Cloudant](https://cloudant.com/for-developers/faq/development/).
