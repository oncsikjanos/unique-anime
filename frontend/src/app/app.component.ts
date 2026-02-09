import {Component, inject} from '@angular/core';
import { UserCardComponent } from "./components/user-card/user-card.component";
import {map, Observable} from 'rxjs';
import { CommonModule } from '@angular/common';
import {AnimeListComponent} from "./components/anime-list/anime-list.component";
import {User} from "./models/User";
import {DataService} from "./services/data.service";


@Component({
    selector: 'app-root',
    imports: [UserCardComponent, CommonModule, AnimeListComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss'
})
export class AppComponent {
    dataService: DataService = inject(DataService);

    users$: Observable<User[]>;
    selectedUser: User | null = null;

  constructor(){
    this.users$ = this.dataService.getUserData();
  }

  onUserCardClick(user: User): void {
    this.selectedUser = user;
  }

  isSelected(user: User): boolean {
    return this.selectedUser === user;
  }

}
