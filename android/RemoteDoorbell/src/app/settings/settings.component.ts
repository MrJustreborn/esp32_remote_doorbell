import { Component, OnInit } from "@angular/core";
import { RouterExtensions } from "@nativescript/angular";
import { Button, EventData, Slider, Switch, TextField } from "@nativescript/core";
import { firebase } from "@nativescript/firebase";

import { SecureStorage } from "@nativescript/secure-storage";


@Component({
    selector: "ns-settings",
    templateUrl: "./settings.component.html"
})
export class SettingsComponent implements OnInit {

    private secure = new SecureStorage();

    apiKey = "";
    constructor(private routerExtensions: RouterExtensions) { }
    ngOnInit(): void {
        this.apiKey = this.secure.getSync({
            key: "apiKey"
        })
    }

    goBack() {
        this.routerExtensions.backToPreviousPage();
    }

    onReturnPress(args: EventData) {
        this.routerExtensions.backToPreviousPage();
    }

    saveData(foo: TextField) {
        console.log(foo.text)
        this.apiKey = foo.text;
        this.secure.setSync({
            key: "apiKey",
            value: foo.text
        })
    }
}
