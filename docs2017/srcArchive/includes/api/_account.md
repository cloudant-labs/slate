## Account

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the Account topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/account.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

Your account is your entry point for Cloudant's API.
You access your account using the address prefix `https://$USERNAME.cloudant.com`.
Your Cloudant dashboard is always `https://$USERNAME.cloudant.com/dashboard.html`.

If you don't yet have an account, [sign up](https://cloudant.com/sign-up/).

### Ping

> Example of connecting to your Cloudant account:

```http
GET / HTTP/1.1
HOST: $USERNAME.cloudant.com
```

```shell
curl -u $USERNAME https://$USERNAME.cloudant.com
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
var account = nano("https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com");

account.request(function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

To see if your Cloudant account is accessible, make a `GET` against `https://$USERNAME.cloudant.com`. If you misspelled your account name, you might get a [503 'service unavailable' error](#503).
