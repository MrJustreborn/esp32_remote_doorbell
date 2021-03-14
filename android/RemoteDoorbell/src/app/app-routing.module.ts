import { NgModule } from "@angular/core";
import { Routes } from "@angular/router";
import { NativeScriptRouterModule } from "@nativescript/angular";

import { DoorCtrlComponent } from "./door_ctrl/door_ctrl.component";
import { SettingsComponent } from "./settings/settings.component";

const routes: Routes = [
    { path: "", component: DoorCtrlComponent },
    { path: "settings", component: SettingsComponent }
];

@NgModule({
    imports: [NativeScriptRouterModule.forRoot(routes)],
    exports: [NativeScriptRouterModule]
})
export class AppRoutingModule { }
