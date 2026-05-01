import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { map, Observable, of, switchMap } from 'rxjs';
import { AsyncPipe, CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIcon } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule } from '@angular/forms';
import { Anime } from '../../models/Anime';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-anime-list',
  imports: [
    AsyncPipe,
    CommonModule,
    RouterLink,
    MatButtonModule,
    MatIcon,
    MatFormFieldModule,
    MatSelectModule,
    FormsModule
  ],
  templateUrl: './anime-list.component.html',
  styleUrls: ['./anime-list.component.scss']
})
export class AnimeListComponent implements OnInit {
  private dataService = inject(DataService);
  private route = inject(ActivatedRoute);

  user = '';
  animes$: Observable<Anime[]> = of([]);
  orders = [
    { value: 'name', viewValue: 'Name' },
    { value: 'point', viewValue: 'Rating' },
  ];
  selectedOrder = 'point';
  increase = true;
  searchTerm = '';

  ngOnInit(): void {
    this.animes$ = this.route.paramMap.pipe(
      switchMap(params => {
        this.user = params.get('name') ?? '';
        return this.dataService.getAnimeData(this.user);
      }),
      map(animes => this.filterAndSortAnimes(animes))
    );
  }

  private filterAndSortAnimes(animes: Anime[]): Anime[] {
    let filtered = animes;
    if (this.searchTerm.trim()) {
      const q = this.searchTerm.toLowerCase();
      filtered = animes.filter(a => a.title?.toLowerCase().includes(q));
    }
    return this.sortAnimes(filtered);
  }

  private sortAnimes(animes: Anime[]): Anime[] {
    return [...animes].sort((a, b) => {
      const useName = this.selectedOrder === 'name';
      const cmpA = useName ? (a.title?.toLowerCase() ?? '') : (a.rating ?? 0);
      const cmpB = useName ? (b.title?.toLowerCase() ?? '') : (b.rating ?? 0);
      if (cmpA < cmpB) return this.increase ? 1 : -1;
      if (cmpA > cmpB) return this.increase ? -1 : 1;
      return 0;
    });
  }

  private refresh(): void {
    this.animes$ = this.dataService.getAnimeData(this.user).pipe(
      map(animes => this.filterAndSortAnimes(animes))
    );
  }

  onSelectionChange(): void { this.refresh(); }
  onOrderingClick(): void { this.increase = !this.increase; this.refresh(); }
  onSearchChange(): void { this.refresh(); }
}
