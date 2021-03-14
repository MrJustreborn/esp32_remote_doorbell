import { ChangeDetectorRef, Component, OnDestroy, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { Button, EventData, Slider, Switch } from "@nativescript/core";
import { firebase } from "@nativescript/firebase";

import { SecureStorage } from "@nativescript/secure-storage";
import { Subscription } from "rxjs";

import { environment, KEYS } from "../environment";
import { DoorbellService, User } from "../services/doorbell.service";


@Component({
    selector: "ns-items",
    templateUrl: "./door_ctrl.component.html"
})
export class DoorCtrlComponent implements OnInit, OnDestroy {

    private subs: Array<Subscription> = [];

    private secure = new SecureStorage();

    columns;
    visitorModeActive = false;

    visitorModeTimme = 10;

    user: User = null;

    constructor(
        private router: Router,
        private doorbellService: DoorbellService,
        private change: ChangeDetectorRef
    ) { }

    ngOnInit(): void {
        this.setProgressbarWidth(100);
        this.subs.push(this.doorbellService.user$.subscribe((u) => {
            this.user = u
            this.change.detectChanges()
        }))
        this.doorbellService.getUser();
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
        this.doorbellService.onOpenDoor();
    }

    gotToSettings() {
        console.log("GotToSettings")
        this.router.navigate(['/settings'])
    }

    ngOnDestroy() {
        this.subs.forEach((sub) => {
            sub.unsubscribe();
        });
        this.subs = [];
    }
}
