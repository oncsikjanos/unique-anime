import { Injectable, inject } from '@angular/core';
import { collection, collectionData, Firestore } from '@angular/fire/firestore';
import {Observable} from "rxjs";
import {User} from "../models/User";
import {Anime} from "../models/Anime";

@Injectable({
  providedIn: 'root'
})
export class FirestoreService {
  private firestore: Firestore = inject(Firestore);

  getUserList(): Observable<User[]> {
    return this.getDataFromFirestore<User>('User');
  }

  getAnimeList(user: string): Observable<Anime[]> {
    return this.getDataFromFirestore<Anime>("Anime/"+user+"/Uniques");
  }

  private getDataFromFirestore<T>(collectionPath: string): Observable<T[]> {
    const collectionRef = collection(this.firestore, collectionPath);
    return collectionData(collectionRef) as Observable<T[]>;
  }

}
