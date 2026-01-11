import { Injectable, inject } from '@angular/core';
import { collection, collectionData, Firestore } from '@angular/fire/firestore';
import {Observable} from "rxjs";

interface User {
  name: string;
  pfp: string;
  completed: number;
  unique: number;
}

@Injectable({
  providedIn: 'root'
})
export class FirestoreService {
  firestore: Firestore = inject(Firestore);

  constructor() { }

  getUserList(): Observable<User[]> {
    const userCollection = collection(this.firestore, 'User')
    return collectionData(userCollection) as Observable<User[]>;
  }

  getAnimeList(user: string): Observable<any[]> {
    const animeCollection = collection(this.firestore, "Anime/"+user+"/Uniques")
    return collectionData(animeCollection)
  }
}
