import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { UserCardComponent } from "./components/main/user-card/user-card.component";
import {map, Observable} from 'rxjs';
import { FirestoreService } from './services/firestore.service';
import { CommonModule } from '@angular/common';
import {AnimeListComponent} from "./components/main/anime-list/anime-list.component";

interface User {
  name: string;
  pfp: string;
  completed: number;
  unique: number;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, UserCardComponent, CommonModule, AnimeListComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'unique-anime';
  users$: Observable<User[]>;
  animes$: Observable<any[]>;
  count = 1;
  selectedUser: any = "";

  constructor(private fsService: FirestoreService){
    this.users$ = this.fsService.getUserList().pipe(
      map((users: User[]) => users.sort((a: User, b: User) => b.unique - a.unique))
    );
    this.animes$ = this.fsService.getAnimeList("");
    this.selectedUser = ""
  }

  onUserCardClick(user: User): void {
    this.selectedUser = user;
  }

  isSelected(user: User): boolean {
    return this.selectedUser === user;
  }

}
