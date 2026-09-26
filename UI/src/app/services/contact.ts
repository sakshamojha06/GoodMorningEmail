import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

import { Contact } from "../models/contact";

@Injectable({
    providedIn: 'root'
})
export class ContactService {
    private apiUrl = 'http://127.0.0.1:5000/contacts';

    constructor(private http: HttpClient) {}

    getContacts(): Observable<Contact[]> {
        return this.http.get<Contact[]>(this.apiUrl);
    }

    addContact(contact: Omit<Contact, 'id'>): Observable<any> {
        return this.http.post(this.apiUrl, contact);
    }

    updateContact(id: number, contact: Omit<Contact, 'id'>): Observable<any> {
        return this.http.put(`${this.apiUrl}/${id}`, contact);
    }

    deleteContact(id: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}/${id}`);
    }
}