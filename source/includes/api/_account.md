## Account

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/getting-started.html">here</a>,
and the Account topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/account.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

Your account is your entry point for Cloudant's API.
You access your account using the address prefix `https://<account>.cloudant.com`.
Your Cloudant dashboard is always `https://<account>.cloudant.com/dashboard.html`.

If you don't yet have an account, [sign up](https://cloudant.com/sign-up/).

### Ping

> Example of connecting to your Cloudant account:

```http
GET / HTTP/1.1
HOST: <account>.cloudant.com
```

```shell
curl $ACCOUNT https://$ACCOUNT.cloudant.com
```

```python
import cloudant

account = cloudant.Account(USERNAME)
ping = account.get()
print ping.status_code
# 200
```

```javascript
var nano = require('nano');
var account = nano("https://$ACCOUNT.cloudant.com");

account.request(function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

To see if your Cloudant account is accessible, make a `GET` against `https://<account>.cloudant.com`. If you misspelled your account name, you might get a [503 'service unavailable' error](#503).
