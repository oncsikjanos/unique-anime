import {Component, Input, SimpleChanges} from '@angular/core';
import {FirestoreService} from "../../../services/firestore.service";
import {map, Observable} from "rxjs";
import { AsyncPipe, CommonModule } from "@angular/common";
import {MatCard} from "@angular/material/card";
import {MatButtonModule} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatSelectModule} from "@angular/material/select";
import {FormsModule} from "@angular/forms";

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
  animes$: Observable<any[]>;
  orders= [
    {value: 'name', viewValue: 'Name'},
    {value: 'point', viewValue: 'Point'},
  ];
  selectedOrder = "name";
  increase = false;
  searchTerm = "";

  @Input({'required': true}) user: string = "";

  constructor(private fsService: FirestoreService) {
    this.animes$ = this.getOrderedAnimes();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['user']) {
      this.animes$ = this.getOrderedAnimes();
    }
  }

  private getOrderedAnimes(): Observable<any[]> {
    return this.fsService.getAnimeList(this.user).pipe(
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

  private sortAnimes(animes: any[]): any[] {
    const sorted = [...animes].sort((a: any, b: any) => {
      let compareA: any;
      let compareB: any;

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

    return sorted;
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
