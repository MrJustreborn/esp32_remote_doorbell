import { Component, OnInit } from "@angular/core";
import { Button, EventData, Switch } from "@nativescript/core";
import { firebase } from "@nativescript/firebase";


@Component({
    selector: "ns-items",
    templateUrl: "./door_ctrl.component.html"
})
export class DoorCtrlComponent implements OnInit {

    constructor() { }

    ngOnInit(): void {
    }

    onOpenDoor(args: EventData) {
        let button = args.object as Button;
        console.log("Open door!")
        firebase.getCurrentPushToken().then((token: string) => {
            // may be null if not known yet
            console.log(`Current push token: ${token}`);
          });
    }
}
