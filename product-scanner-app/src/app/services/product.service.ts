import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable, of } from "rxjs";
import { map, catchError } from "rxjs/operators";

export interface Product {
  sku: string;

  // Core barcode fields (all stores)
  ean13?: string;
  upc?: string;

  // Chedraui-specific barcodes
  ean?: string;
  multi_ean?: string;
  reference?: string;
  product_id?: string;

  // La Comer-specific barcodes
  art_ean?: string;
  art_cod?: string;

  // Papelerias Tony-specific barcodes
  item_ean?: string;
  product_reference?: string;
  product_reference_code?: string;

  // Product details
  name: string;
  brand: string;
  category: string;
  subcategory?: string;
  size?: string;
  price: number;
  list_price?: number;
  discount_percentage?: number;
  currency: string;
  available: boolean;
  stock?: number;
  stock_quantity?: number;
  image_url?: string;
  local_image?: string;
  product_url?: string;
  store: string;
  description?: string;
  rating?: number;
  reviews_count?: number;
  unit_multiplier?: number;
  measurement_unit?: string;
  scraped_at?: string;
}

@Injectable({
  providedIn: "root",
})
export class ProductService {
  private products: Product[] = [];
  private searchHistory: {
    barcode: string;
    product: Product | null;
    timestamp: Date;
  }[] = [];

  constructor(private http: HttpClient) {
    this.loadProducts();
  }

  private async loadProducts() {
    try {
      // Load grocery products
      this.http
        .get<Product[]>("assets/data/grocery-products.json")
        .pipe(catchError(() => of([])))
        .subscribe((data) => {
          this.products.push(...data);
        });

      // Load stationery products
      this.http
        .get<Product[]>("assets/data/stationery-products.json")
        .pipe(catchError(() => of([])))
        .subscribe((data) => {
          this.products.push(...data);
        });
    } catch (error) {
      console.error("Error loading products:", error);
    }
  }

  searchByBarcode(barcode: string): Observable<Product | null> {
    return of(this.products).pipe(
      map((products) => {
        const cleanBarcode = barcode.trim();

        // Search across all barcode fields
        let product = products.find(
          (p) =>
            p.sku === cleanBarcode ||
            p.ean13 === cleanBarcode ||
            p.upc === cleanBarcode ||
            p.ean === cleanBarcode ||
            p.multi_ean === cleanBarcode ||
            p.art_ean === cleanBarcode ||
            p.art_cod === cleanBarcode ||
            p.item_ean === cleanBarcode ||
            p.product_reference === cleanBarcode ||
            p.product_reference_code === cleanBarcode ||
            p.reference === cleanBarcode ||
            p.product_id === cleanBarcode
        );

        // If not found, try partial matches (for truncated barcodes)
        if (!product && cleanBarcode.length >= 8) {
          product = products.find(
            (p) =>
              p.ean13?.includes(cleanBarcode) ||
              p.upc?.includes(cleanBarcode) ||
              p.ean?.includes(cleanBarcode) ||
              p.multi_ean?.includes(cleanBarcode) ||
              p.art_ean?.includes(cleanBarcode) ||
              p.item_ean?.includes(cleanBarcode) ||
              p.sku?.includes(cleanBarcode)
          );
        }

        // Add to history
        this.addToHistory(cleanBarcode, product || null);

        return product || null;
      })
    );
  }

  searchByText(query: string): Observable<Product[]> {
    const searchTerm = query.toLowerCase().trim();

    if (!searchTerm) {
      return of([]);
    }

    return of(this.products).pipe(
      map((products) => {
        return products
          .filter(
            (p) =>
              p.name.toLowerCase().includes(searchTerm) ||
              p.brand.toLowerCase().includes(searchTerm) ||
              p.category.toLowerCase().includes(searchTerm) ||
              p.sku.toLowerCase().includes(searchTerm)
          )
          .slice(0, 50); // Limit to 50 results
      })
    );
  }

  getProductBySku(sku: string): Observable<Product | null> {
    return of(this.products).pipe(
      map((products) => products.find((p) => p.sku === sku) || null)
    );
  }

  getAllProducts(): Observable<Product[]> {
    return of(this.products);
  }

  getProductsByCategory(category: string): Observable<Product[]> {
    return of(this.products).pipe(
      map((products) => products.filter((p) => p.category === category))
    );
  }

  getProductsByStore(store: string): Observable<Product[]> {
    return of(this.products).pipe(
      map((products) => products.filter((p) => p.store === store))
    );
  }

  private addToHistory(barcode: string, product: Product | null) {
    this.searchHistory.unshift({
      barcode,
      product,
      timestamp: new Date(),
    });

    // Keep only last 50 searches
    if (this.searchHistory.length > 50) {
      this.searchHistory = this.searchHistory.slice(0, 50);
    }

    // Save to localStorage
    try {
      localStorage.setItem("searchHistory", JSON.stringify(this.searchHistory));
    } catch (error) {
      console.error("Error saving history:", error);
    }
  }

  getHistory(): any[] {
    try {
      const saved = localStorage.getItem("searchHistory");
      if (saved) {
        this.searchHistory = JSON.parse(saved);
      }
    } catch (error) {
      console.error("Error loading history:", error);
    }
    return this.searchHistory;
  }

  clearHistory(): void {
    this.searchHistory = [];
    localStorage.removeItem("searchHistory");
  }
}
