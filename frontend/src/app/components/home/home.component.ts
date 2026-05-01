import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { map, Observable } from 'rxjs';
import { User } from '../../models/User';
import { DataService } from '../../services/data.service';
import { PodiumComponent } from '../podium/podium.component';
import { ChallengerComponent } from '../challenger/challenger.component';

@Component({
  selector: 'app-home',
  imports: [CommonModule, PodiumComponent, ChallengerComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  private dataService = inject(DataService);

  users$: Observable<User[]> = this.dataService.getUserData();
  podium$: Observable<User[]> = this.users$.pipe(map(u => u.slice(0, 3)));
  rest$: Observable<User[]> = this.users$.pipe(map(u => u.slice(3)));
}
