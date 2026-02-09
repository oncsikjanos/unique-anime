import { Component } from '@angular/core';
import {User} from "../../../models/User";
import {Input} from "@angular/core";
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-search',
  imports: [
    FormsModule
  ],
  styleUrl: './search.component.scss',
  template:
      `<div class="search-box">
        <input
            type="text"
            [(ngModel)]="search"
            placeholder="Search anime..."
            class="search-input"/>
      </div>`,
})
export class SearchComponent {
  @Input() userList: User[] = [];

  search: string = "";
}
