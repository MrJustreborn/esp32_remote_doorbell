#include <ArduinoWebsockets.h>
#include <WiFi.h>

#define PIN_LED    2
#define PIN_BUTTON 13

const char* ssid = "RTL Network";
const char* password = "<SNIP>";
const char* websockets_server = "ws://192.168.178.60:8765/key_esp";

//button bounce
bool bounce = false;

using namespace websockets;

void onMessageCallback(WebsocketsMessage message) {
    Serial.print("Got Message: ");
    Serial.println(message.data());
}

void onEventsCallback(WebsocketsEvent event, String data) {
    if(event == WebsocketsEvent::ConnectionOpened) {
        Serial.println("Connnection Opened");
    } else if(event == WebsocketsEvent::ConnectionClosed) {
        Serial.println("Connnection Closed");
    } else if(event == WebsocketsEvent::GotPing) {
        Serial.println("Got a Ping!");
    } else if(event == WebsocketsEvent::GotPong) {
        Serial.println("Got a Pong!");
    }
}

WebsocketsClient client;
void setup() {
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_BUTTON, INPUT);
  Serial.begin(115200);
  Serial.println("Init");

  // Connect to wifi
  WiFi.begin(ssid, password);
  
  // Wait some time to connect to wifi
  for(int i = 0; i < 10 && WiFi.status() != WL_CONNECTED; i++) {
      Serial.print(".");
      delay(1000);
  }
  
  // Setup Callbacks
  client.onMessage(onMessageCallback);
  client.onEvent(onEventsCallback);
  
  // Connect to server
  client.connect(websockets_server);
  
  // Send a message
  client.send("Hi Server!");
  // Send a ping
  client.ping();
}

void loop() {
  client.poll();
  if (digitalRead(PIN_BUTTON) == LOW) {
    digitalWrite(PIN_LED,HIGH);
    if (bounce) {
      Serial.println("Send ring");
      client.send("ring");
      bounce = false;
    }
  } else {
    digitalWrite(PIN_LED,LOW);
    bounce = true;
  }
}
