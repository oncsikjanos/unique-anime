import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
    selector: 'app-podium-element',
    imports: [CommonModule, RouterLink],
    templateUrl: './podium-element.component.html',
    styleUrl: './podium-element.component.scss'
})
export class PodiumElementComponent {
    @Input() pfp!: string;
    @Input() name!: string;
    @Input() uniqueAnimeCount!: number;
    @Input() completedAnimeCount!: number
    @Input() placement!: number;

    get ringClass() {
        return 'ring-' + this.placement;
    }

    get slotClass() {
        return 'slot-' + this.placement;
    }

    get pillarClass() {
        return 'pillar-' + this.placement;
    }

    get medalClass() {
        return 'medal-' + this.placement;
    }

    get bigForFirsPlacement() {
        return this.placement === 1 ? 'big' : '';
    }

}
