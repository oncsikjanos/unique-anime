import {Component, EventEmitter, inject, Input, Output, SimpleChanges} from '@angular/core';
import {map, Observable} from "rxjs";
import { AsyncPipe, CommonModule } from "@angular/common";
import {MatCard} from "@angular/material/card";
import {MatButtonModule} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatSelectModule} from "@angular/material/select";
import {FormsModule} from "@angular/forms";
import {Anime} from "../../models/Anime";
import {DataService} from "../../services/data.service";

@Component({
    selector: 'app-anime-list',
    imports: [
        AsyncPipe,
        CommonModule,
        MatCard,
        MatButtonModule,
        MatIcon,
        MatFormFieldModule,
        MatSelectModule,
        FormsModule
    ],
    templateUrl: './anime-list.component.html',
    styleUrl: './anime-list.component.scss'
})
export class AnimeListComponent {
  @Input({'required': true}) user: string = "";
  @Output() listClosed = new EventEmitter<void>();

  private dataService: DataService = inject(DataService);

  animes$: Observable<Anime[]> = new Observable<Anime[]>();
  orders= [
    {value: 'name', viewValue: 'Name'},
    {value: 'point', viewValue: 'Point'},
  ];
  selectedOrder = "name";
  increase = false;
  searchTerm = "";

  ngAfterViewInit() {
    this.animes$ = this.dataService.getAnimeData(this.user);
  }

  constructor() {
    this.animes$ = this.dataService.getAnimeData(this.user);
  }

  private getOrderedAnimes(): Observable<any[]> {
    return this.dataService.getAnimeData(this.user).pipe(
      map(animes => this.filterAndSortAnimes(animes))
    );
  }

  private filterAndSortAnimes(animes: any[]): any[] {
    let filtered = animes;
    
    // Apply search filter
    if (this.searchTerm.trim()) {
      const searchLower = this.searchTerm.toLowerCase();
      filtered = animes.filter(anime => 
        anime.title?.toLowerCase().includes(searchLower)
      );
    }

    // Apply sorting
    return this.sortAnimes(filtered);
  }

  private sortAnimes(animes: Anime[]): Anime[] {
    return [...animes].sort((a: Anime, b: Anime) => {
      let compareA: string | number;
      let compareB: string | number;

      if (this.selectedOrder === 'name') {
        compareA = a.title?.toLowerCase() || '';
        compareB = b.title?.toLowerCase() || '';
      } else {
        compareA = a.rating || 0;
        compareB = b.rating || 0;
      }

      if (compareA < compareB) {
        return this.increase ? 1 : -1;
      } else if (compareA > compareB) {
        return this.increase ? -1 : 1;
      }
      return 0;
    });
  }

  onSelectionChange(){
    console.log("selected: "+this.selectedOrder);
    this.animes$ = this.getOrderedAnimes();
  }

  onOrderingClick(){
    this.increase = !this.increase;
    this.animes$ = this.getOrderedAnimes();
  }

  onSearchChange(){
    this.animes$ = this.getOrderedAnimes();
  }

}
