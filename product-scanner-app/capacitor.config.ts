import { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "com.productscanner.app",
  appName: "Product Scanner",
  webDir: "www",
  server: {
    androidScheme: "https",
  },
  plugins: {
    BarcodeScanner: {
      scanInstructions: "Scan a barcode or QR code",
      scanningText: "Scanning...",
    },
  },
};

export default config;
