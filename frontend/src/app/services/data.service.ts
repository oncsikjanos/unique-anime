import {inject, Injectable} from '@angular/core';
import {FirestoreService} from "./firestore.service";
import {map, tap, of, Observable} from "rxjs";
import {User} from "../models/User";
import {Anime} from "../models/Anime";

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private firestoreService: FirestoreService = inject(FirestoreService);

  getUserData(): Observable<User[]> {
    //TODO: Handle cache delete if there is newer data in firestore
    return this.getDataFromCache('userDataList', () => this.initUsersListCache());
  }

  getAnimeData(userName: string): Observable<Anime[]> {
    //TODO: Handle cache delete if there is newer data in firestore
    return this.getDataFromCache(userName + '_animeDataList', () => this.initAnimeListCache(userName));
  }

  private getDataFromCache<T>(cacheKey: string, initCacheMethod: () => Observable<T>): Observable<T> {
    const cachedData = localStorage.getItem(cacheKey);

    if (cachedData) {
      return of(JSON.parse(cachedData));
    }

    return initCacheMethod();
  }

  private initUsersListCache(): Observable<User[]> {
    return this.firestoreService.getUserList().pipe(
        map(users => [...users].sort((a, b) => b.unique - a.unique)),
        tap(users => localStorage.setItem('userDataList', JSON.stringify(users)))
    );
  }

  private initAnimeListCache(userName: string): Observable<Anime[]> {
    return this.firestoreService.getAnimeList(userName).pipe(
        map(animes => [...animes].sort((a, b) => b.rating - a.rating)),
        tap(animes => localStorage.setItem(userName + '_animeDataList', JSON.stringify(animes)))
    );
  }
}
