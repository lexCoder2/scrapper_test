# 📱 Product Scanner Mobile App

## ✅ Hybrid Mobile App Created!

A complete Ionic/Capacitor mobile app for scanning and identifying products using barcodes.

### 🎯 Features

- 📷 **Barcode Scanner** - Scan UPC/EAN codes with camera
- 🔍 **Product Search** - Search by name, brand, SKU
- 📊 **4,000+ Products** - Grocery & stationery database
- 💾 **Offline Mode** - Works without internet
- 💰 **Price Comparison** - Compare across stores
- ⭐ **Product Details** - Complete info with ratings
- 📝 **Scan History** - Track scanned items

### 📱 Platform Support

- ✅ **Android** - Build APK for Android devices
- ✅ **iOS** - Build IPA for iPhone/iPad
- ✅ **Web** - Test in browser during development

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```powershell
cd product-scanner-app
.\setup.ps1
```

This will:

- Install all dependencies
- Copy product data automatically
- Build the app
- Ready to test!

### Option 2: Manual Setup

```powershell
cd product-scanner-app

# Install dependencies
npm install

# Copy product data
New-Item -Path "src/assets/data" -ItemType Directory -Force
Copy-Item "../mexico_grocery_sample_20251118_162048.json" -Destination "src/assets/data/grocery-products.json"
Copy-Item "../stationery_products_20251118_162642.json" -Destination "src/assets/data/stationery-products.json"

# Build
ionic build
```

---

## 🖥️ Test in Browser

```powershell
cd product-scanner-app
ionic serve
```

Opens at `http://localhost:8100`

**Note:** Barcode scanner only works on real devices, not in browser.

---

## 📱 Build for Mobile

### Android

```powershell
# First time
ionic capacitor add android

# Build & sync
ionic build
ionic capacitor sync android

# Open in Android Studio
ionic capacitor open android
```

Then click "Run" in Android Studio to install on device/emulator.

### iOS (macOS only)

```powershell
# First time
ionic capacitor add ios

# Build & sync
ionic build
ionic capacitor sync ios

# Open in Xcode
ionic capacitor open ios
```

Then click "Run" in Xcode to install on device/simulator.

---

## 📂 Project Structure

```
product-scanner-app/
├── src/
│   ├── app/
│   │   ├── pages/
│   │   │   ├── scanner/        # Barcode scanning
│   │   │   ├── search/         # Product search
│   │   │   ├── history/        # Scan history
│   │   │   └── product-detail/ # Product info
│   │   └── services/
│   │       ├── barcode-scanner.service.ts
│   │       └── product.service.ts
│   └── assets/
│       └── data/
│           ├── grocery-products.json
│           └── stationery-products.json
├── android/              # Android project
├── ios/                 # iOS project
├── capacitor.config.ts  # Capacitor config
├── README.md           # Full documentation
├── BUILD.md            # Build instructions
└── setup.ps1           # Setup script
```

---

## 🔧 Prerequisites

Before building:

1. **Node.js 18+** - [Download](https://nodejs.org/)
2. **Ionic CLI** - `npm install -g @ionic/cli`
3. **Android Studio** - For Android builds
4. **Xcode** - For iOS builds (macOS only)

---

## 💡 How It Works

1. **Scan Barcode** - Camera scans UPC/EAN code
2. **Search Database** - Looks up product in local JSON
3. **Display Results** - Shows product details, price, store
4. **Save History** - Keeps track of scanned items

### Data Flow

```
Phone Camera → Barcode Scanner → Product Service → JSON Database → UI
```

---

## 🎨 Customization

### Add More Products

Edit JSON files in `src/assets/data/`:

```json
{
  "sku": "ST5000001",
  "upc": "750123456789",
  "name": "Product Name",
  "brand": "Brand",
  "price": 99.99,
  "store": "Store"
}
```

### Change Theme

Edit `src/theme/variables.scss`:

```scss
:root {
  --ion-color-primary: #3880ff;
}
```

---

## 📊 Product Database

The app includes:

- **2,131 Grocery Products**

  - Bebidas, Lácteos, Despensa, Carnes, etc.
  - Stores: Soriana, Walmart, Chedraui, HEB

- **2,000 Stationery Products**
  - Escritura, Cuadernos, Arte, Tecnología
  - Stores: Office Depot, OfficeMax, Lumen

**Total: 4,131 products ready to scan!**

---

## 🔍 Testing Without Device

While in browser (`ionic serve`):

1. Use the **Search** tab to test product lookup
2. Type product names to see results
3. Click products to view details
4. Scanner only works on real devices

---

## 📱 Permissions Required

### Android

- **Camera** - For barcode scanning
- Auto-configured in the app

### iOS

- **Camera** - For barcode scanning
- User will be prompted on first scan

---

## 🐛 Troubleshooting

### "ionic: command not found"

```powershell
npm install -g @ionic/cli
```

### Camera not working

1. Check device permissions
2. Rebuild: `ionic capacitor sync --force`
3. Clear app cache

### Products not loading

1. Verify JSON files in `src/assets/data/`
2. Check file names match service
3. Rebuild: `ionic build && ionic capacitor sync`

### Build errors

```powershell
# Clean install
Remove-Item -Recurse -Force node_modules, www
npm install
ionic build
```

---

## 📚 Documentation

- **README.md** - Complete app documentation
- **BUILD.md** - Detailed build instructions
- **setup.ps1** - Automated setup script

---

## 🎯 Next Steps

1. ✅ Run `.\setup.ps1` to install everything
2. ✅ Test in browser with `ionic serve`
3. ✅ Add Android/iOS platform
4. ✅ Build and install on device
5. ✅ Start scanning products!

---

## 🔗 Resources

- [Ionic Framework](https://ionicframework.com/)
- [Capacitor](https://capacitorjs.com/)
- [Barcode Scanner Plugin](https://github.com/capacitor-community/barcode-scanner)

---

## 📦 What's Included

- ✅ Complete Ionic/Angular app
- ✅ Barcode scanner integration
- ✅ Product search & lookup
- ✅ Offline database (4,000+ products)
- ✅ UI pages (Scanner, Search, History, Details)
- ✅ Services (Scanner, Products)
- ✅ Build configurations (Android/iOS)
- ✅ Setup scripts & documentation

---

**Ready to scan! 📱📷🛒**

Run `cd product-scanner-app` and `.\setup.ps1` to get started!
