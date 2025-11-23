import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { AlertController, LoadingController } from "@ionic/angular";
import { BarcodeScannerService } from "../../services/barcode-scanner.service";
import { ProductService, Product } from "../../services/product.service";

@Component({
  selector: "app-scanner",
  templateUrl: "./scanner.page.html",
  styleUrls: ["./scanner.page.scss"],
})
export class ScannerPage implements OnInit {
  isScanning = false;
  lastScannedCode: string = "";
  scannedProduct: Product | null = null;

  constructor(
    private barcodeScanner: BarcodeScannerService,
    private productService: ProductService,
    private router: Router,
    private alertController: AlertController,
    private loadingController: LoadingController
  ) {}

  ngOnInit() {}

  async startScan() {
    this.isScanning = true;

    const barcode = await this.barcodeScanner.startScan();

    this.isScanning = false;

    if (barcode) {
      this.lastScannedCode = barcode;
      await this.searchProduct(barcode);
    }
  }

  async searchProduct(barcode: string) {
    const loading = await this.loadingController.create({
      message: "Searching product...",
      duration: 5000,
    });
    await loading.present();

    this.productService.searchByBarcode(barcode).subscribe(
      async (product) => {
        await loading.dismiss();

        if (product) {
          this.scannedProduct = product;
          // Navigate to product detail
          this.router.navigate(["/product-detail", product.sku]);
        } else {
          await this.showProductNotFound(barcode);
        }
      },
      async (error) => {
        await loading.dismiss();
        console.error("Search error:", error);
        await this.showError();
      }
    );
  }

  async showProductNotFound(barcode: string) {
    const alert = await this.alertController.create({
      header: "Product Not Found",
      message: `No product found with barcode: ${barcode}. The product might not be in our database yet.`,
      buttons: ["OK"],
    });
    await alert.present();
  }

  async showError() {
    const alert = await this.alertController.create({
      header: "Error",
      message:
        "An error occurred while searching for the product. Please try again.",
      buttons: ["OK"],
    });
    await alert.present();
  }

  goToSearch() {
    this.router.navigate(["/search"]);
  }
}
