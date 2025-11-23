import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { ProductService, Product } from "../../services/product.service";

@Component({
  selector: "app-search",
  templateUrl: "./search.page.html",
  styleUrls: ["./search.page.scss"],
})
export class SearchPage implements OnInit {
  searchQuery: string = "";
  searchResults: Product[] = [];
  isSearching: boolean = false;

  constructor(private productService: ProductService, private router: Router) {}

  ngOnInit() {}

  onSearchChange(event: any) {
    const query = event.detail.value;
    this.searchQuery = query;

    if (query && query.length >= 2) {
      this.isSearching = true;
      this.productService.searchByText(query).subscribe(
        (results) => {
          this.searchResults = results;
          this.isSearching = false;
        },
        (error) => {
          console.error("Search error:", error);
          this.isSearching = false;
        }
      );
    } else {
      this.searchResults = [];
    }
  }

  viewProduct(product: Product) {
    this.router.navigate(["/product-detail", product.sku]);
  }

  clearSearch() {
    this.searchQuery = "";
    this.searchResults = [];
  }
}
