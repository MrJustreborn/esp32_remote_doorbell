import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";

import { SecureStorage } from "@nativescript/secure-storage";

import { environment, KEYS } from "../environment";
import { BehaviorSubject } from "rxjs";

export interface User {
    id: number;
    name: string;
}

@Injectable({
    providedIn: 'root'
})
export class DoorbellService {

    user$: BehaviorSubject<User> = new BehaviorSubject(null);

    private secure = new SecureStorage();
    public constructor(
        private http: HttpClient
    ) {}

    public setMessageToken(token) {
        console.info("DoorbellService::setMessageToken()", token);

        try {
            const apiKey = this.getApiKey();
            const serverUrl = this.getServerUrl();
            this.http.put(serverUrl + 'setToken/' +apiKey+ '/' + token, {}, {
                responseType: "text"
            }).toPromise()
            .then((res) => {
                console.log("OK", res);
            })
            .catch((res) => {
                console.log("NOT OK", res);
            });
        } catch (error) {
            console.error("Cannot setToken: ", error)
            return null;
        }
    }

    public onOpenDoor() {
        try {
            const apiKey = this.getApiKey();
            const serverUrl = this.getServerUrl();
            this.http.post(serverUrl + 'open/' +apiKey, {}, {
                responseType: "text"
            }).toPromise()
            .then((res) => {
                console.log("OK", res);
            })
            .catch((res) => {
                console.log("NOT OK", res);
            });
        } catch (error) {
            console.error("Cannot open: ", error)
            return null;
        }
    }

    public async getUser(): Promise<User> {
        try {
            const apiKey = this.getApiKey();
            const serverUrl = this.getServerUrl();
            const user = await this.http.get<User>(serverUrl + 'getUser/' +apiKey).toPromise();
            console.log("Got User: ", user)
            this.user$.next(user);
            return user;
        } catch (error) {
            console.error("Cannot getUser: ", error)
            this.user$.next(null);
            return null;
        }
    }

    private getApiKey() {
        const apiKey = this.secure.getSync({key: KEYS.apiKey});
        if (!apiKey) {
            console.error("NO KEY DEFINED");
            throw new Error("No Key Defined");
        }
        return apiKey;
    }
    private getServerUrl() {
        const apiKey = this.secure.getSync({key: KEYS.serverUrl});
        if (!apiKey) {
            console.error("NO SERVER URL DEFINED");
            return environment.serverUrl;
        }
        return apiKey;
    }
}
