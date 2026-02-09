import { Component } from '@angular/core';
import { UserCardComponent } from "./components/main/user-card/user-card.component";
import {map, Observable} from 'rxjs';
import { FirestoreService } from './services/firestore.service';
import { CommonModule } from '@angular/common';
import {AnimeListComponent} from "./components/main/anime-list/anime-list.component";
import {Anime} from "./models/Anime";
import {User} from "./models/User";


@Component({
    selector: 'app-root',
    imports: [UserCardComponent, CommonModule, AnimeListComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'unique-anime';
  users$: Observable<User[]>;
  animes$: Observable<Anime[]> | null = null;
  count = 1;
  selectedUser: User | null = null;

  constructor(private fsService: FirestoreService){
    this.users$ = this.fsService.getUserList().pipe(
      map((users: User[]) => users.sort((a: User, b: User) => b.unique - a.unique))
    );
    //console.log(this.users$);
    //this.animes$ = this.fsService.getAnimeList("");
    //this.selectedUser = ""
  }

  onUserCardClick(user: User): void {
    this.selectedUser = user;
  }

  isSelected(user: User): boolean {
    return this.selectedUser === user;
  }

}
