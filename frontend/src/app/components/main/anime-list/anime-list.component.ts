import {Component, Input, SimpleChanges} from '@angular/core';
import {FirestoreService} from "../../../services/firestore.service";
import {Observable} from "rxjs";
import {AsyncPipe, CommonModule} from "@angular/common";
import {MatCard} from "@angular/material/card";
import {MatButtonModule} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatSelectModule} from "@angular/material/select";

@Component({
    selector: 'app-anime-list',
    imports: [
        AsyncPipe,
        CommonModule,
        MatCard,
        MatButtonModule,
        MatIcon,
        MatFormFieldModule,
        MatSelectModule
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
  increase = false

  @Input({'required': true}) user = "szbalcsi"

  constructor(private fsService: FirestoreService) {
    this.animes$ = fsService.getAnimeList(this.user);

  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['user']) {
      this.animes$ = this.fsService.getAnimeList(this.user);
    }

  }

  onSelectionChange(){
    console.log("selected: "+this.selectedOrder);
  }

  onOrderingClick(){
    this.increase = !this.increase;
  }

}
