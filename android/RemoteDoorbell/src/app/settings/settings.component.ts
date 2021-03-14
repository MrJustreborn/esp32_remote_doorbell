import { ChangeDetectorRef, Component, OnDestroy, OnInit } from "@angular/core";
import { RouterExtensions } from "@nativescript/angular";
import { Button, EventData, Slider, Switch, TextField } from "@nativescript/core";
import { firebase } from "@nativescript/firebase";

import { SecureStorage } from "@nativescript/secure-storage";
import { Subscription } from "rxjs";

import { environment, KEYS } from "../environment";
import { DoorbellService, User } from "../services/doorbell.service";


@Component({
    selector: "ns-settings",
    templateUrl: "./settings.component.html"
})
export class SettingsComponent implements OnInit, OnDestroy {

    private subs: Array<Subscription> = [];

    private secure = new SecureStorage();

    user: User = null;

    apiKey = "";
    serverUrl = environment.serverUrl;
    constructor(
        private routerExtensions: RouterExtensions,
        private doorbellService: DoorbellService,
        private change: ChangeDetectorRef
        ) { }
    ngOnInit(): void {
        this.apiKey = this.secure.getSync({
            key: KEYS.apiKey
        })
        this.serverUrl = this.secure.getSync({
            key: KEYS.serverUrl
        })

        this.subs.push(this.doorbellService.user$.subscribe((u) => {
            this.user = u
            this.change.detectChanges()
        }))
        this.doorbellService.getUser();
    }

    goBack() {
        this.routerExtensions.backToPreviousPage();
    }

    onReturnPress(args: EventData) {
        this.routerExtensions.backToPreviousPage();
    }

    saveData(apiKey: TextField, serverUrl: TextField) {
        console.log(apiKey.text, serverUrl.text)
        this.apiKey = apiKey.text;
        this.serverUrl = serverUrl.text;

        this.secure.setSync({
            key: KEYS.apiKey,
            value: apiKey.text
        })
        this.secure.setSync({
            key: KEYS.serverUrl,
            value: serverUrl.text
        })

        this.doorbellService.getUser();
    }

    ngOnDestroy() {
        this.subs.forEach((sub) => {
            sub.unsubscribe();
        });
        this.subs = [];
    }
}
