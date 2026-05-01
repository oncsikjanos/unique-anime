import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs/internal/Observable';
import { User } from '../../models/User';
import { PodiumElementComponent } from './podium-element/podium-element.component';

@Component({
    selector: 'app-podium',
    imports: [CommonModule, PodiumElementComponent],
    templateUrl: './podium.component.html',
    styleUrl: './podium.component.scss'
})
export class PodiumComponent {
    @Input() podium$!: Observable<User[]>;

}
