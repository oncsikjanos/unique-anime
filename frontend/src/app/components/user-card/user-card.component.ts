import {Component, Input, SimpleChanges} from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-user-card',
    imports: [
      MatCardModule,
      MatIconModule,
      CommonModule
    ],
    templateUrl: './user-card.component.html',
    styleUrls: ['./user-card.component.scss']
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
