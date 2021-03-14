import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { Button, EventData, Slider, Switch } from "@nativescript/core";
import { firebase } from "@nativescript/firebase";

import { SecureStorage } from "@nativescript/secure-storage";


@Component({
    selector: "ns-items",
    templateUrl: "./door_ctrl.component.html"
})
export class DoorCtrlComponent implements OnInit {

    private secure = new SecureStorage();

    columns;
    visitorModeActive = false;

    visitorModeTimme = 10;

    constructor(
        private router: Router
    ) { }

    ngOnInit(): void {
        this.setProgressbarWidth(100);
        const foo = this.secure.getSync({
            key: "apiKey"
        });

        console.log("init: ", foo)
    }

    setProgressbarWidth(percent) {
        this.columns = percent + "*," + (100 - percent) + "*";
    }


    onSliderValueChange(args: EventData) {
        let slider = args.object as Slider;
        console.log("onSliderValueChange", slider.value)
        this.visitorModeTimme = slider.value;
    }

    activateVisitorsMode(args: EventData) {
        let button = args.object as Button;
        console.log("activateVisitorsMode")
        this.visitorModeActive = true;
    }

    deactivateVisitorsMode(args: EventData) {
        let button = args.object as Button;
        console.log("deactivateVisitorsMode")
        this.visitorModeActive = false;
        this.visitorModeTimme = 10;
    }

    onProgressLoaded() {
        this.visitorModeActive = false;
    }

    onOpenDoor(args: EventData) {
        let button = args.object as Button;
        console.log("Open door!")
    }

    gotToSettings() {
        console.log("GotToSettings")
        this.router.navigate(['/settings'])
    }
}
