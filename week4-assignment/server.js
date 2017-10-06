var iotf = require('ibmiotf');
var service;

// TODO create your iotf application client here
var appClientConfig // = ... ;
if (process.env.VCAP_SERVICES) {
	var env = JSON.parse(process.env.VCAP_SERVICES);
	appClientConfig = {
		'org' : env["iotf-service"][0].credentials.org,
		'id' : 'cbc-a4',
		'auth-key' : env["iotf-service"][0].credentials.apiKey,
		'auth-token' : env["iotf-service"][0].credentials.apiToken
	}
} else {
	appClientConfig = require('./application.json');
}
var appClient = new iotf.IotfApplication(appClientConfig);

var Service = require('./service');

// Binding to a port ensures that the service is kept alive.
// We use express for that and implement a /status endpoint.
var express = require('express');
var cfenv = require('cfenv');
var cfappEnv = cfenv.getAppEnv();
var app = express();

app.get('/status', function(req, res) {
  res.status(200).json({ message: 'iot service running' });
});

app.get('/', function(req, res) {
  var response = "Server running on " + cfappEnv.url + "<br/>";
  if (service) {
    if (service.deviceType || service.deviceId) {
      response += "Events being transmit and received from device " + service.deviceId + " of type " + service.deviceType + "<br/>";
    } else {
      response += "No device events received yet<br/>";
    }
    if (service.prevTemp) {
      response += "Last temperature received was " + service.prevTemp;
    } else {
      response += "No previous temperature received";
    }
  }
  res.send(response);
});

module.exports = app.listen(cfappEnv.port, function() {
  console.log('server started on ' + cfappEnv.url);
  service = new Service(appClient);
  // use service to connect here
  service.connect();
});
