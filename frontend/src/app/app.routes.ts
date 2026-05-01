import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { AnimeListComponent } from './components/anime-list/anime-list.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'user/:name', component: AnimeListComponent },
  { path: '**', redirectTo: '' },
];
