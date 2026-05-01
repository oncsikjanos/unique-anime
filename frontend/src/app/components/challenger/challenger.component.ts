import { Component, Input} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';
import { User } from '../../models/User';
import { UserCardComponent } from '../user-card/user-card.component';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-challenger',
  imports: [CommonModule, UserCardComponent, RouterLink],
  templateUrl: './challenger.component.html',
  styleUrl: './challenger.component.scss'
})
export class ChallengerComponent {
    @Input() users$: Observable<User[]> = new Observable<User[]>();
}
