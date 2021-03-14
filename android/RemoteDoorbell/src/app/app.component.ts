import { Component, OnInit } from "@angular/core";
import { firebase } from "@nativescript/firebase";
import { DoorbellService } from "./services/doorbell.service";

@Component({
    selector: "ns-app",
    templateUrl: "./app.component.html"
})
export class AppComponent implements OnInit {

    constructor(
        private doorbellService: DoorbellService
    ) {}
    ngOnInit(): void {
        firebase.init({
            onMessageReceivedCallback: (message: any) => {
                console.log(`Title: ${message.title}`);
                console.log(`Body: ${message.body}`);
            },
            onPushTokenReceivedCallback: (token) => {
                console.log("Firebase push token: " + token);
                this.doorbellService.setMessageToken(token);
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
