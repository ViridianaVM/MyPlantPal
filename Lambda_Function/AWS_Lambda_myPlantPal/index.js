exports.handler = function (request, context) {
  if (request.directive.header.namespace === 'Alexa.Discovery' && request.directive.header.name === 'Discover') {
      log("DEBUG:", "Discover request",  JSON.stringify(request));
      handleDiscovery(request, context, "");
  }
  else if (request.directive.header.namespace === 'Alexa.PowerController') {
      if (request.directive.header.name === 'TurnOn' || request.directive.header.name === 'TurnOff') {
          log("DEBUG:", "TurnOn or TurnOff Request", JSON.stringify(request));
          handlePowerControl(request, context);
      }
  }

  function handleDiscovery(request, context) {
      // var myToken = request.directive.payload.scope.token;
      // console.log("Aqui esta mi token: ",myToken);
      //MAndar a llamar mi web service para obtener mi lista de dispositivos
      //Con la lista de dispositivos crear mis endpoints y Alexa sepa cuantos dispositivos tiene ese usuario
      var payload = {
          "endpoints":
          [
              {
                  "endpointId": "my-plant-pal-001",
                  "manufacturerName": "Viri Smart Device Company",
                  "friendlyName": "Bedroom Plant",
                  "description": "Plant in bedroom",
                  "displayCategories": ["FAN"],
                  "additionalAttributes":  {
                    "manufacturer" : "Smart Device Company",
                    "model" : "Sample Model",
                    "serialNumber": "U11112233456",
                    "firmwareVersion" : "1.24.2546",
                    "softwareVersion": "1.036",
                    "customIdentifier": "Sample custom ID"
                  },
                  "cookie": {
                      "key1": "arbitrary key/value pairs for skill to reference this endpoint.",
                      "key2": "There can be multiple entries",
                      "key3": "but they should only be used for reference purposes.",
                      "key4": "This is not a suitable place to maintain current endpoint state."
                  },
                  "capabilities":
                  [
                      {
                        "type": "AlexaInterface",
                        "interface": "Alexa",
                        "version": "3"
                      },
                      {
                          "interface": "Alexa.PowerController",
                          "version": "3",
                          "type": "AlexaInterface",
                          "properties": {
                              "supported": [{
                                  "name": "powerState"
                              }],
                               "retrievable": true
                          }
                      },
                      {
                        "type": "AlexaInterface",
                        "interface": "Alexa.InventoryLevelSensor",
                        "instance": "PlantSensor.Moisture",
                        "version": "3",
                        "properties": {
                          "supported": [
                            {
                              "name": "level"
                            }
                          ],
                          "retrievable": true,
                          "proactivelyReported": true
                        },
                        "configuration": {
                          "measurement": {
                            "@type": "Percentage"
                          }
                        },
                        "capabilityResources": {
                          "friendlyNames": [
                            {
                              "@type": "text",
                              "value": {
                                "text": "Moisture sensor",
                                "locale": "en-US"
                              }
                            }
                          ]
                        }
                      }
                  ]
              }
          ]
      };
      var header = request.directive.header;
      header.name = "Discover.Response";
      log("DEBUG", "Discovery Response: ", JSON.stringify({ header: header, payload: payload }));
      context.succeed({ event: { header: header, payload: payload } });
  }

  function log(message, message1, message2) {
      console.log(message + message1 + message2);
  }

  function handlePowerControl(request, context) {
      // get device ID passed in during discovery
      var requestMethod = request.directive.header.name;
      var responseHeader = request.directive.header;
      responseHeader.namespace = "Alexa";
      responseHeader.name = "Response";
      responseHeader.messageId = responseHeader.messageId + "-R";
      // get user token pass in request
      var requestToken = request.directive.endpoint.scope.token;
      var powerResult;

      if (requestMethod === "TurnOn") {

          // Make the call to your device cloud for control
          // powerResult = stubControlFunctionToYourCloud(endpointId, token, request);
          powerResult = "ON";
      }
     else if (requestMethod === "TurnOff") {
          // Make the call to your device cloud for control and check for success
          // powerResult = stubControlFunctionToYourCloud(endpointId, token, request);
          powerResult = "OFF";
      }
      var contextResult = {
          "properties": [{
              "namespace": "Alexa.PowerController",
              "name": "powerState",
              "value": powerResult,
              "timeOfSample": "2017-09-03T16:20:50.52Z", //retrieve from result.
              "uncertaintyInMilliseconds": 50
              },
              {
              "namespace": "Alexa.InventoryLevelSensor",
              "instance": "InkSensor.Cyan",
              "name": "level",
              "value": {
                  "@type": "Percentage",
                  "value": 100
              }
              }
          ]
      };
      var response = {
          context: contextResult,
          event: {
              header: responseHeader,
              endpoint: {
                  scope: {
                      type: "BearerToken",
                      token: requestToken
                  },
                  endpointId: "my-plant-pal-001"
              },
              payload: {}
          }
      };
      log("DEBUG", "Alexa.PowerController ", JSON.stringify(response));
      context.succeed(response);
  }
};