import {inject, Injectable} from '@angular/core';
import {FirestoreService} from "./firestore.service";
import {catchError, map, Observable, of, shareReplay, switchMap, tap} from "rxjs";
import {User} from "../models/User";
import {Anime} from "../models/Anime";
import {LastUpdated} from '../models/LastUpdated';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private firestoreService: FirestoreService = inject(FirestoreService);
  private lastUpdated$?: Observable<LastUpdated[]>;

  getUserData(): Observable<User[]> {
    return this.cachedOrFresh(
      'userDataList',
      () => this.firestoreService.getUserList().pipe(
        map(users => [...users].sort((a, b) => b.unique - a.unique))
      )
    );
  }

  getAnimeData(userName: string): Observable<Anime[]> {
    return this.cachedOrFresh(
      userName + '_animeDataList',
      () => this.firestoreService.getAnimeList(userName).pipe(
        map(animes => [...animes].sort((a, b) => b.rating - a.rating))
      )
    );
  }

  getLastUpdated(): Observable<LastUpdated[]> {
    if (!this.lastUpdated$) {
      this.lastUpdated$ = this.firestoreService.getLastUpdated().pipe(
        shareReplay({ bufferSize: 1, refCount: false })
      );
    }
    return this.lastUpdated$;
  }

  private cachedOrFresh<T>(key: string, fetcher: () => Observable<T>): Observable<T> {
    return this.getLastUpdated().pipe(
      switchMap(items => {
        const serverStamp = this.toStamp(items);
        const cached = localStorage.getItem(key);
        const cachedStamp = localStorage.getItem(key + '_lastUpdated');

        if (cached && cachedStamp === serverStamp) {
          return of(JSON.parse(cached) as T);
        }

        return fetcher().pipe(
          tap(data => {
            localStorage.setItem(key, JSON.stringify(data));
            localStorage.setItem(key + '_lastUpdated', serverStamp);
          })
        );
      }),
      catchError(() => {
        const cached = localStorage.getItem(key);
        return cached ? of(JSON.parse(cached) as T) : fetcher();
      })

    );
  }

  private toStamp(items: LastUpdated[]): string {
    if (!items?.length) return '';
    const ts: any = items[0].timestamp;
    if (ts && typeof ts.seconds === 'number') return String(ts.seconds);
    if (ts instanceof Date) return String(ts.getTime());
    if (typeof ts === 'string') return ts;
    return String(ts);
  }
}
