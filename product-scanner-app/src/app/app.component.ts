import { Component } from "@angular/core";

@Component({
  selector: "app-root",
  templateUrl: "app.component.html",
  styleUrls: ["app.component.scss"],
})
export class AppComponent {
  public appPages = [
    { title: "Scanner", url: "/scanner", icon: "scan" },
    { title: "Search", url: "/search", icon: "search" },
    { title: "History", url: "/history", icon: "time" },
  ];

  constructor() {}
}
