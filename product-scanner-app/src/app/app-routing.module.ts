import { NgModule } from "@angular/core";
import { PreloadAllModules, RouterModule, Routes } from "@angular/router";

const routes: Routes = [
  {
    path: "",
    redirectTo: "scanner",
    pathMatch: "full",
  },
  {
    path: "scanner",
    loadChildren: () =>
      import("./pages/scanner/scanner.module").then((m) => m.ScannerPageModule),
  },
  {
    path: "search",
    loadChildren: () =>
      import("./pages/search/search.module").then((m) => m.SearchPageModule),
  },
  {
    path: "history",
    loadChildren: () =>
      import("./pages/history/history.module").then((m) => m.HistoryPageModule),
  },
  {
    path: "product-detail/:id",
    loadChildren: () =>
      import("./pages/product-detail/product-detail.module").then(
        (m) => m.ProductDetailPageModule
      ),
  },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
