---
title: IBM Cloudant NoSQL DB

language_tabs:
#  - http
#  - shell: curl
#  - javascript: node.js
#  - python

---
# Getting started with Cloudant NoSQL DB

Cloudant NoSQL DB is a NoSQL database as a service (DBaaS). It's built from the ground
up to scale globally, run non-stop, and handle a wide variety of data
types like JSON, full-text, and geospatial. Cloudant NoSQL DB is
an operational data store optimized to handle concurrent reads and
writes, and provide high availability and data durability.

Learn about Cloudant NoSQL DB with live demos and code examples in the <tm tmtype="tm" trademark="Cloudant">Cloudant</tm> [For Developers
section](https://cloudant.com/for-developers/), or get into the details with the [API Documentation](https://docs.cloudant.com/api/index.html). If you're
using Cloudant NoSQL DB for a mobile app, check out [Data for iOS8](../data/index.html#data).

*	[The Web Console](index.html#The Web Console)
*	[Bluemix applications](index.html#Bluemix applications)
*	[Applications outside of Bluemix](index.html#Applications outside of Bluemix)



##The Web Console

You can launch the Cloudant NoSQL DB console from the service launch page on the Bluemix dashboard.


##Bluemix applications

You can use the `VCAP_SERVICES` environment variable to connect
to the Cloudant NoSQL database. You can use the Bluemix user
interface to create applications and services, or you can do the same
from the command line interface by using the CloudFoundry cf tool.

Before we get started you need to install the CloudFoundry cf tool
on your desktop. Instructions on how to do that can be found in the Bluemix Quick
Start guide.

####1	Managing Cloudant NoSQL DB instance with CLI
First, create a new service instance with the `cf create-service` command. Type the following command at the terminal:

	```$ cf create-service```


The `cf` command prompts you to choose one of the available service offerings, and
then asks you for a unique instance name and the plan for the service.
It will present you with a random name but you can change it if you
want.

After creating a new service, you can use the `cf services`
command to list all available service instances that you have created.

	```$ cf services```

Before using a service in an application, you must bind the service to your
application. Use the following command:

	```$ cf bind-service```

You need to select one of the applications and one of the services from
the list. Once the binding action succeeds, `cf` will return a message
to you.

####2	Connecting to the service in your application

After binding a service instance to the application,
code similar to the following example is added to your `VCAP_SERVICES` environment
variable.

	```{
	  "cloudantNoSQLDB": {
	    "name": "Cloudant-3s",
	    "label": "cloudantNoSQLDB",
	    "plan": "shared",
	    "credentials": {
	      "username": "someusername",
	      "password": "secret",
	      "host": "myhost-bluemix.cloudant.com",
	      "port": 443,<account>@myhost-bluemix.cloudant.com"
	    }
	  }
	}```

As you can see, the `VCAP_SERVICE` environment variable includes the following items:


**key** - The name of the service (`cloudantNoSQLDB`)

**name** - The user provided name of the service instance

**host** - The host name of Cloudant NoSQL DB server

**port** - The port number of the Cloudant NoSQL DB server

**username** - The user name for authentication

**password** - The password for authentication

**url** - The url of the Cloudant NoSQL DB instance

Now you can use this Cloudant NoSQL DB instance from a variety of Bluemix run-times like java, was-liberty, node.js application and ruby applications.

####3	Interacting with Cloudant NoSQL DB instance to insert and query data

*	[Cloudant Developer homepage](https://cloudant.com/for-developers/)
*	[Using Cloudant from Python](https://github.com/cloudant-labs/cloudant-python)
*	[Using Cloudant from Java](https://github.com/cloudant/couchjava)
*	[Using Cloudant from Ruby](https://www.ruby-toolbox.com/categories/couchdb_clients)
*	[Cloudant Sync for Android](https://github.com/cloudant/sync-android)
*	[Cloudant Sync for iOS](https://github.com/cloudant/CDTDatastore)

####4	Pushing your application to Bluemix

After you finish the coding, you can deploy your application to a Bluemix environment
for verification. To deploy an application, you need to enter into
the root directory of the Java application and use the following command:

	```$ cf push```

####5	Unbinding or deleting a service instance

To unbind a service instance from an application, use the following command:

	```cf unbind-service```

To delete a service instance, use the following command:

	```cf delete-service```


##Applications outside of Bluemix

The connection and credential information for the service
instance is available in the Bluemix `VCAP_SERVICES` environment variable. It provides the following information to connect to the Cloudant NoSQL database:

*	Host name
*	Port number
*	Username and password
*	URL

##Cloudant Node.js Client

[Cloudant Node.js Client](https://github.com/cloudant/nodejs-cloudant) is the official Cloudant NoSQL DB library for Node.js, based on the nano library.

The Cloudant Node.js client requires user name, password, and account values from the Bluemix `VCAP_SERVICES` environment variable. These fields map onto the user name, password, and user name fields in `VCAP_SERVICES`. See the Cloudant Node.js fields mapped to `VCAP_SERVICES` table.

| Cloudant Node.js | VCAP_SERVICES |
| -----------------|---------------|
| username   | username |
| password   | password |
| account    | username |


##Binding a Cloudant NoSQL DB to Liberty applications

If you push an application or a packaged Liberty server and bind to a NoSQL database, the Liberty buildpack automatically generates or updates CouchDB-related server.xml entries.

When you push an application, the Liberty buildpack generates a `server.xml` file. If you bind your application to a NoSQL database, the Liberty buildpack generates the associated `server.xml` stanzas that are required to access the database. Additionally, the Liberty buildpack provides the required JAR files of the client driver. In summary, the Liberty buildpack:

*	Generates a `couchdb>` stanza.
*	Generates a `<library>` stanza with an embedded `<fileset>` stanza.
*	Adds the couchdb-1.0 feature to the `<featureManager>` stanza.
*	Adds the classloader for the CouchDB ektorp libraries to the `<application>` stanza.

The Liberty buildpack must generate a jndiName in the `<couchdb>` stanza. Because the Liberty buildpack does not have access to the JNDI name that is used by the application, it generates a JNDI name with the convention `couchdb/<service_name>` where the `<service_name>` is the name of the bound service.

For example, if you bind a Cloudant NoSQL DB that is named `mycloudant` to the application, the Liberty buildpack generates a JNDI name of `couchdb/mycloudant`. When you develop the application and create the Cloudant NoSQL DB, you must ensure that the JNDI name that is used by the application matches the JNDI name that is generated by the Liberty buildpack.

The following example shows the generated configuration when an application is pushed and bound to a Cloudant NoSQL DB named `mycloudant`.

	```<featureManager>
		<feature>webProfile-6.0&lt;/feature>
		<feature>jaxrs-1.1&lt;/feature>
		<feature>couchdb-1.0&lt;/feature>
	</featureManager>

	<application context-root='/' location='../../../../../' name='<cmdname props="keyref(app_name)">myapp</cmdname>.war' type='war'>
		<classloader commonLibraryRef='cloudantNoSQLDB-library'>
	</application>

	<couchdb id='cloudantNoSQLDB-mycloudant' jndiName='couchdb/mycloudant' libraryRef='cloudantNoSQLDB-	library' password='${cloud.services.mycloudant.connection.password}' url='${cloud.services.mycloudant.connection.url}' username='${cloud.services.mycloudant.connection.username}'/>
	<library id='cloudantNoSQLDB-library'>
		<fileset dir='${server.config.dir}/lib'
			id='cloudantNoSQLDB-fileset'
			includes='commons-codec-1.6.jar
			commons-io-2.0.1.jar
			commons-logging-1.1.1.jar
			httpclient-4.2.5.jar
			httpclient-cache-4.2.5.jar
			httpcore-4.2.5.jar
			jackson-annotations-2.2.2.jar
			jackson-core-2.2.2.jar
			jackson-databind-2.2.2.jar
			jcl-over-slf4j-1.6.6.jar
			org.ektorp-1.4.1.jar
			slf4j-api-1.6.6.jar
			slf4j-jdk14-1.6.6.jar'/>
	</library>```

###Pushing a Packaged Server

When you push a packaged server, the Liberty buildpack detects and uses the `server.xml` file in the compressed file that is pushed. When you bind the packaged server to a NoSQL database, the Liberty buildpack checks the `server.xml` file for `<couchdb>` entries that correspond to the bound database.

If the Liberty buildpack does not find the `<couchdb>` stanza, it is created and added to the `server.xml` file.

If you provide configuration in your `server.xml` file, the configuration must be coherent. The `<couchdb>`, `<library>`, and `<fileset>` stanzas must be configured properly. The `<featureManager>` must contain the couchdb-1.0 feature, and the `<application>` or `<webApplication>` stanza must contain the classloader that includes the library. Additionally, your configuration stanzas must contain configuration ids as described in the next section.

The Liberty buildpack searches for existing configuration by using the configuration IDs in the stanzas. The following algorithms are used to generate the configuration IDs that are used in the search:

*	The `<couchdb>` search uses a configuration ID of `<service_type>`-`<service_name>`.
*	The `<library>` search uses a configuration ID of `<service_type>`-library.
*	The `<fileset>` search uses a configuration ID of `<service_type>`-fileset.

The `<service_type>` is a lowercase string constant. For Cloudant NoSQL DB, the `service_type` is cloudantNoSQLDB. The `<service_type>` is the name of the service. For example, if you create a Cloudant NoSQL DB with the name `mycloudant`, `mycloudant` is the `service_name` and the cloudant stanza ID is  `cloudantNoSQLDB-mycloudant`. If you provide configuration stanzas, your configuration IDs must be created with the necessary algorithms. Failure to comply with these conventions results in errors.

If the Liberty buildpack finds existing configuration, it checks and updates that configuration if necessary. For example, the buildpack might update the following stanzas and attributes: The user, password and url attributes in the `<couchdb>` stanza or the `dir` and `includes` attributes in the `<fileset>` stanza.


**Note**: In this case, the Liberty buildpack does not update the `jndiName` attribute.

You can provide your own client driver JAR files. The client driver JAR files must be placed in the `usr/servers/<servername>/lib` directory. If you do not provide client driver JAR files, the Liberty buildpack provides the files. Any client JAR files that you provide must use the standard names that are established by the providing vendor. You cannot rename client JAR files.

**Note**: To avoid classloading conflicts, you should not provide the client driver JAR files in the `WEB-INF/lib` directory of your application.

The following code is a sample of Cloudant NoSQL DB configuration that might be provided in the local `server.xml` file. This sample assumes that when the packaged server is pushed to the cloud, it is bound to a Cloudant NoSLQ DB named `mycloudant`. In this case, the `jndiName` attribute can be whatever value you prefer. The value of the `jndiName` attribute is independent of the service name.

	```<couchdb id="cloudantNoSQLDB-mycloudant" jndiName='couchdb/mycloudant' libraryRef='cloudantNoSQLDB-library' password='somepass' url='https://<account>.cloudant.com'/>
	<library id="cloudantNoSQLDB-library">
		<fileset id='cloudantNoSQLDB-fileset'
			dir='c:/cloudantlibs'		
			includes='commons-codec-1.6.jar
			commons-io-2.0.1.jar
			commons-logging-1.1.1.jar
			httpclient-4.2.5.jar
			httpclient-cache-4.2.5.jar
			httpcore-4.2.5.jar
			jackson-annotations-2.2.2.jar
			jackson-core-2.2.2.jar
			jackson-databind-2.2.2.jar
			jcl-over-slf4j-1.6.6.jar
			org.ektorp-1.4.1.jar
			slf4j-api-1.6.6.jar
			slf4j-jdk14-1.6.6.jar'/>
	</library>```

When the `server.xml` file is pushed to the cloud, the Liberty buildpack updates the CouchDB configuration stanzas as follows:

	```<couchdb id='cloudantNoSQLDB-mycloudant' jndiName='couchdb/mycloudant' libraryRef='cloudantNoSQLDB-library' password='${cloud.services.mycloudant.connection.password}' url='${cloud.services.mycloudant.connection.url}' username='${cloud.services.mycloudant.connection.username}'/>
	<library id='cloudantNoSQLDB-library'>
			<fileset dir='${server.config.dir}/lib'
				id='cloudantNoSQLDB-fileset'
				includes='commons-codec-1.6.jar
				commons-io-2.0.1.jar
				commons-logging-1.1.1.jar
				httpclient-4.2.5.jar
				httpclient-cache-4.2.5.jar
				httpcore-4.2.5.jar
				jackson-annotations-2.2.2.jar
				jackson-core-2.2.2.jar
				jackson-databind-2.2.2.jar
				jcl-over-slf4j-1.6.6.jar
				org.ektorp-1.4.1.jar
				slf4j-api-1.6.6.jar
				slf4j-jdk14-1.6.6.jar'/>
		</library>```

##Sample for <tm tmtype="tm" trademark="Cloudant">Cloudant</tm> on Liberty

The following <tm tmtype="reg" trademark="developerWorks">developerWorks</tm> article
contains a sample that shows how this auto-configuration works:

[Java and Cloudant NoSQL DB on Bluemix](https://developer.ibm.com/bluemix/2014/07/08/cloudant_on_bluemix/)
