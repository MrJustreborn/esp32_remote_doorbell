import { Component, OnInit } from "@angular/core";
import { firebase } from "@nativescript/firebase";

@Component({
    selector: "ns-app",
    templateUrl: "./app.component.html"
})
export class AppComponent implements OnInit {
    ngOnInit(): void {
        firebase.init({
            showNotificationsWhenInForeground: true,
            persist: false,
            onMessageReceivedCallback: (message: any) => {
                console.log(`Title: ${message.title}`);
                console.log(`Body: ${message.body}`);
            },
            onPushTokenReceivedCallback: function(token) {
                console.log("Firebase push token: " + token);
            }
          }).then(
            () => {
              console.log("firebase.init done");
            },
            error => {
              console.log(`firebase.init error: ${error}`);
            }
          );
    }

}
