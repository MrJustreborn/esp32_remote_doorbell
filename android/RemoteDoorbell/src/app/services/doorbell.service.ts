import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Injectable({
    providedIn: 'root'
})
export class DoorbellService {
    public constructor(
        private http: HttpClient
    ) {}

    public setMessageToken(token) {
        console.info("DoorbellService::setMessageToken()", token);
        this.http.put('http://192.168.178.60:5000/setToken/key/' + token, {}, {
            responseType: "text"
        }).toPromise()
        .then((res) => {
            console.log("OK", res);
        })
        .catch((res) => {
            console.log("NOT OK", res);
        });
    }

}
