import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Contact } from './models/contact';
import { ContactService } from './services/contact';
import { Topic } from './models/topic';
import { TopicService } from './services/topic';

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit{
    contacts = signal<Contact[]>([]);
    topics: Topic[] = [];

    form = {
      name: '',
      email: '',
      startDate: '',
      isActive: true,
      topicId: 0
    };

    editingId: number | null = null;

    constructor(private contactService: ContactService, private topicService: TopicService) {}

    ngOnInit(): void {
      this.loadContacts();
      this.loadTopics();
    }

    loadContacts(): void {
      this.contactService.getContacts().subscribe({
        next: data => this.contacts.set(data),
        error: err => console.error('Failed to load contacts', err)
      });
    }

    loadTopics(): void {
      this.topicService.getTopics().subscribe({
        next: (data) => {
          this.topics = data;

          if (this.topics.length > 0 && this.form.topicId === 0) {
            this.form.topicId = this.topics[0].id;
          }
        },
        error: (error) => {
          console.error('Failed to load topics', error);
        }
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
        isActive: contact.isActive,
        topicId: contact.topicId
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

    getTopicName(topicId: number): string {
      const topic = this.topics.find(t => t.id === topicId);

      return topic ? topic.name : 'Unknown';
    }

    resetForm(): void {
      this.editingId = null;

      this.form = {
        name: '',
        email: '',
        startDate: '',
        isActive: true,
        topicId: this.topics.length > 0 ? this.topics[0].id : 0
      };
    }
}
