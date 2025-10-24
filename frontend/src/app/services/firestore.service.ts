import { Injectable, inject } from '@angular/core';
import { collection, collectionData, Firestore } from '@angular/fire/firestore';
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class FirestoreService {
  firestore: Firestore = inject(Firestore);

  constructor() { }

  getUserList(){
    const userCollection = collection(this.firestore, 'User')
    return collectionData(userCollection);
  }

  getAnimeList(user: string): Observable<any[]> {
    const animeCollection = collection(this.firestore, "Anime/"+user+"/Uniques")
    return collectionData(animeCollection)
  }
}
