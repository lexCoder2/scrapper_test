import { Injectable } from "@angular/core";
import { BarcodeScanner } from "@capacitor-community/barcode-scanner";

@Injectable({
  providedIn: "root",
})
export class BarcodeScannerService {
  constructor() {}

  async checkPermission(): Promise<boolean> {
    try {
      const status = await BarcodeScanner.checkPermission({ force: true });

      if (status.granted) {
        return true;
      }

      if (status.denied) {
        alert(
          "Camera permission is required to scan barcodes. Please enable it in settings."
        );
        return false;
      }

      return false;
    } catch (error) {
      console.error("Permission check error:", error);
      return false;
    }
  }

  async startScan(): Promise<string | null> {
    try {
      const permission = await this.checkPermission();

      if (!permission) {
        return null;
      }

      // Make background of WebView transparent
      await BarcodeScanner.hideBackground();

      // Start scanning
      const result = await BarcodeScanner.startScan();

      // Make background visible again
      await BarcodeScanner.showBackground();

      if (result.hasContent) {
        return result.content;
      }

      return null;
    } catch (error) {
      console.error("Scan error:", error);
      await BarcodeScanner.showBackground();
      return null;
    }
  }

  async stopScan(): Promise<void> {
    try {
      await BarcodeScanner.stopScan();
      await BarcodeScanner.showBackground();
    } catch (error) {
      console.error("Stop scan error:", error);
    }
  }
}
