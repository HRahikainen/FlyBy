import { Injectable } from '@angular/core';
import { Firebase } from '@ionic-native/firebase/ngx';
import { Platform } from '@ionic/angular';
import { AngularFirestore } from 'angularfire2/firestore';
import { HomePage } from '../../src/app/home/home.page';

@Injectable()
export class FcmService {

  constructor(private firebase: Firebase,
              private afs: AngularFirestore,
              private platform: Platform,
              public hmp:HomePage) {}

  async getToken() {
    let token;

    if (this.platform.is('android')) {
      token = await this.firebase.getToken();
    }

    if (this.platform.is('ios')) {
      token = await this.firebase.getToken();
      await this.firebase.grantPermission();
    }

    this.saveToken(token);
  }

  private saveToken(token) {
    if (!token) return;

    const devicesRef = this.afs.collection(token);

    const data = {
      token,
      userId: 'testUserId'
    };

    //return devicesRef.doc(token).set(data);
  }

  onNotifications() {

    var elm : Element  = {
      name : "Junction Hack",
      cost : 2.49,
      pic :'../../assets/img/food2.png'
    }

    this.hmp.balance = this.hmp.balance - elm.cost;
    this.hmp.elements.push(elm);
    return this.firebase.onNotificationOpen();
  }
}


export  class  Element {

  cost: number;
  name: string;
  pic:string;
  constructor(values: Object = {}) {

  Object.assign(this, values);
  }  
}
