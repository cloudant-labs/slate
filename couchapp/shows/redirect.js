function(doc, req) {
    return { code : 301, headers: { "Location": 'https://console.bluemix.net/docs/services/Cloudant/' + req.query.target } };
}
