import { NgModule, NO_ERRORS_SCHEMA } from "@angular/core";
import { NativeScriptModule } from "@nativescript/angular";
import { HttpClientModule } from "@angular/common/http";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { DoorCtrlComponent } from "./door_ctrl/door_ctrl.component";
import { SettingsComponent } from "./settings/settings.component";

import { DoorbellService } from "./services/doorbell.service";

@NgModule({
    bootstrap: [
        AppComponent
    ],
    imports: [
        NativeScriptModule,
        AppRoutingModule,
        HttpClientModule
    ],
    declarations: [
        AppComponent,
        DoorCtrlComponent,
        SettingsComponent
    ],
    providers: [DoorbellService],
    schemas: [
        NO_ERRORS_SCHEMA
    ]
})
export class AppModule { }
