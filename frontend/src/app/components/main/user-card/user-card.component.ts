import {Component, Input, SimpleChanges} from '@angular/core';
import {MatCard} from '@angular/material/card';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-user-card',
    imports: [
        MatCard,
        CommonModule
    ],
    templateUrl: './user-card.component.html',
    styleUrl: './user-card.component.scss'
})
export class UserCardComponent {
  defaultUser = {'pfp': 's', 'name': 's', 'completed': 1, 'unique': 1}
  @Input({required: true}) user = this.defaultUser;
  @Input({required: true}) placement = 0;
  color = "#FFFFFF";

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['placement']) {
      this.setColor(this.placement);
    }
  }

  setColor(placement: number): void {
    switch (placement) {
      case 1:
        this.color = "#FFD700";
        break;
      case 2:
        this.color = "#C0C0C0";
        break;
      case 3:
        this.color = "#CD7F32";
        break;
      default:
        this.color = "#FFE0E0";
        break;
    }
  }

}
