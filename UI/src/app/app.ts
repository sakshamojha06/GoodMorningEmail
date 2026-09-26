import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Contact } from './models/contact';
import { ContactService } from './services/contact';

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit{
    contacts = signal<Contact[]>([]);

    form = {
      name: '',
      email: '',
      startDate: '',
      isActive: true
    };

    editingId: number | null = null;

    constructor(private contactService: ContactService) {}

    ngOnInit(): void {
      this.loadContacts();
    }

    loadContacts(): void {
      this.contactService.getContacts().subscribe({
        next: data => this.contacts.set(data),
        error: err => console.error('Failed to load contacts', err)
      });
    }

    saveContacts(): void {
      if (this.editingId === null) {
        this.contactService.addContact(this.form).subscribe({
          next: () => {
            alert('Contact added successfully');
            this.resetForm();
            this.loadContacts();
          },
          error: (error) => {
            console.error(error);
            alert('Failed to add contact');
          }
        });
      }
      else {
        this.contactService.updateContact(this.editingId, this.form).subscribe({
          next: () => {
            alert('Contact updated successfully');
            this.resetForm();
            this.loadContacts();
          },
          error: (error) => {
            console.error(error);
            alert('Failed to update contact');
          }
        });
      }
    }

    editContact(contact: Contact): void {
      this.editingId = contact.id;

      this.form = {
        name: contact.name,
        email: contact.email,
        startDate: contact.startDate,
        isActive: contact.isActive
      };
    }

    deleteContact(id: number): void {
      if(!confirm('Are you sure you want to delete this contact? ')) {
        return;
      }

      this.contactService.deleteContact(id).subscribe({
        next: () => {
          alert('Contact deleted successfully');
          this.loadContacts();
        },
        error: (error) => {
          console.error(error);
          alert('Failed to delete contact');
        }
      });
    }

    resetForm(): void {
      this.editingId = null;

      this.form = {
        name: '',
        email: '',
        startDate: '',
        isActive: true
      };
    }
}
