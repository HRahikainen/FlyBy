import { Component } from '@angular/core';
import { Events } from '@ionic/angular';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss']
})
export class HomePage {



  constructor(public events: Events){
    this.elements = this.getElements();
    this.balance = 126.79;
    
  }

  
  public elements : Element[] = [];
  public balance : number;



  getElements(){

    this.elements = [
      {
        name : "X-burger",
        cost : 11.49,
        pic:'../../assets/img/food.png'
      },
      {
        name : "School cafe",
        cost : 6.49,
        pic:'../../assets/img/food2.png'
      },
      {
        name : "Fast buffet",
        cost : 8.19,
        pic:'../../assets/img/food.png'
      },
      {
        name : "School buffet",
        cost : 5.29,
        pic:'../../assets/img/food2.png'
      }
    ]

    return this.elements;
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

