import { Injectable } from "@angular/core";
import { Topic } from "../models/topic";
import { Observable } from "rxjs";
import { HttpClient } from "@angular/common/http";

@Injectable({
    providedIn: 'root'
})
export class TopicService {
    private apiUrl = 'http://127.0.0.1:5000/topics';

    constructor(private http: HttpClient) {}

    getTopics(): Observable<Topic[]> {
        return this.http.get<Topic[]>(this.apiUrl);
    }
}