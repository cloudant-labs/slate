Welcome
=======

This is a repository containing Cloudant documentation content,
to be published on IBM Bluemix.

Issues and PRs welcome.

Bluemix markdown
----------------

The Bluemix markdown content is built using the `marked-it*` toolkits for Node.js.

Specifically,
the repositories required are:
-   `git@github.ibm.com:Grant-Gayed/marked-it.git`
-   `git@github.ibm.com:Grant-Gayed/marked-it-cli.git`

>   **Note**: The `marked-it*` modules are only available internally within IBM.
    However,
    they are basically markdown build scripts with some additional capabilities
    for Bluemix-specific 'extras'.
    It is not essential to have these tools;
    they are only used for building a local preview of content.
    It is still perfectly possible to do a 'pure' markdown-only build of the content
    for local preview purposes.

When you have obtained copies of these two repositories,
you must tell Node about them.

Do this by running the following two commands **from your Home folder**:
1.  `npm install <marked-it-install-folder>/marked-it`
2.  `npm install <marked-it-cli-install-folder>/marked-it-cli`

... where `<marked-it-install-folder>` and `<marked-it-cli-install-folder>`
correspond to the installation folders for the two repositories.

Finally,
modify the `docs2017/scripts/Makefile` variables:
-   `TOOLDIR` (on line 8)
-   `BUILDTOOLDIR` (on line 9)

... so that the build system can locate the `marked-it-cli` component.

Style
-----

Sample code illustrating how to invoke a capability should be provided in the
following order:

_Example of using an HTTP request to &lt;activity&gt;:_

_Example of using the command line to &lt;activity&gt;:_

_Example of using JavaScript to &lt;activity&gt;:_

_Example of using Python to &lt;activity&gt;:_

```
Sample code line 1
Sample code line 2
```
{:screen}

_Example response:_
 
```
Sample response line 1
Sample response line 2
```
{:screen}

Basically,
HTTP first,
then the command line,
then each language in simple alphabetic order,
and finally a sample response from running the code.