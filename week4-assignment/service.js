this.prevTemp = undefined;
this.deviceType = undefined;
this.deviceId = undefined;

function Service(appClient) {
  this.appClient = appClient;
}

Service.prototype.connect = function() {
  // connect to iotf here with this.appClient
  this.appClient.connect();

  this.appClient.on('connect', function() {
    // hook up device events here with this.appClient
    this.appClient.subscribeToDeviceEvents();
  }.bind(this));

  this.appClient.on('deviceEvent', function (deviceType, deviceId, eventType, format, payload) {
    // act on device events and call handleTempEvent when the right type of event arrives
    var payload = JSON.parse(payload);
    if (payload.d.temperature) {
      // we received a temperature event
      if (!this.deviceType || !this.deciveId) {
        // Initialise deviceType and deviceId if needed
        this.deviceType = deviceType;
        this.deviceId = deviceId;
      }
      this.handleTempEvent(payload.d.temperature);
    }
  }.bind(this));
};

Service.prototype.handleTempEvent = function(temp) {
  // handle temperature changes here and call this.warningOn/this.warningOff accordingly.
  var threshold = 29;
  if (!this.prevTemp || (this.prevTemp < threshold && temp >= threshold) || (this.prevTemp >= threshold && temp < threshold)) {
    // Need to change the screen because it has not yet been set or we've just
    //   crossed the threshold
    if (temp < threshold) {
      this.warningOff();
    } else {
      this.warningOn();
    }
    this.prevTemp = temp;
  }
};

Service.prototype.warningOn = function() {
  // send a device commmand here
  // warningOn should only be called when the warning isn't already on
  var data = {'screen' : 'on'};
  data = JSON.stringify(data);
  this.appClient.publishDeviceCommand(this.deviceType, this.deviceId, "display", "json", data);
};

Service.prototype.warningOff = function() {
  // send a device commmand here
  // warningOff should only be called when the warning isn't already off
  var data = {'screen' : 'off'};
  data = JSON.stringify(data);
  this.appClient.publishDeviceCommand(this.deviceType, this.deviceId, "display", "json", data);
};

module.exports = Service;
