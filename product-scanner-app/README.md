# Product Scanner App

A hybrid mobile application built with Ionic/Capacitor for scanning and identifying products using barcodes. Works offline with a local product database.

## Features

- 📱 **Hybrid App** - Works on iOS and Android
- 📷 **Barcode Scanning** - Scan UPC/EAN codes with your camera
- 🔍 **Product Search** - Search by name, brand, SKU, or category
- 📊 **Product Database** - 4,000+ Mexican products (grocery & stationery)
- 💾 **Offline Mode** - Works without internet connection
- 💰 **Price Comparison** - Compare prices across stores
- ⭐ **Product Details** - Complete product information with ratings
- 📝 **Scan History** - Keep track of scanned products

## Tech Stack

- **Ionic Framework 7** - Hybrid app framework
- **Angular 17** - Frontend framework
- **Capacitor 5** - Native bridge
- **Barcode Scanner** - Camera-based scanning
- **TypeScript** - Type-safe development

## Prerequisites

Before you begin, ensure you have:

- Node.js 18+ installed
- npm or yarn package manager
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)
- Ionic CLI: `npm install -g @ionic/cli`

## Installation

### 1. Install Dependencies

```powershell
cd product-scanner-app
npm install
```

### 2. Add Product Data

Copy your product JSON files to the assets folder:

```powershell
# Create assets directory
New-Item -Path "src/assets/data" -ItemType Directory -Force

# Copy product data
Copy-Item "../mexico_grocery_sample_*.json" -Destination "src/assets/data/grocery-products.json"
Copy-Item "../stationery_products_*.json" -Destination "src/assets/data/stationery-products.json"
```

### 3. Run in Browser (Development)

```powershell
ionic serve
```

Or:

```powershell
npm start
```

The app will open at `http://localhost:8100`

## Build for Mobile

### Android

1. **Add Android Platform:**

   ```powershell
   ionic capacitor add android
   ```

2. **Build the App:**

   ```powershell
   ionic build
   ionic capacitor sync android
   ```

3. **Open in Android Studio:**

   ```powershell
   ionic capacitor open android
   ```

4. **Run on Device/Emulator:**
   - Click "Run" in Android Studio
   - Or use: `ionic capacitor run android`

### iOS (macOS only)

1. **Add iOS Platform:**

   ```powershell
   ionic capacitor add ios
   ```

2. **Build the App:**

   ```powershell
   ionic build
   ionic capacitor sync ios
   ```

3. **Open in Xcode:**

   ```powershell
   ionic capacitor open ios
   ```

4. **Run on Device/Simulator:**
   - Click "Run" in Xcode
   - Or use: `ionic capacitor run ios`

## Project Structure

```
product-scanner-app/
├── src/
│   ├── app/
│   │   ├── pages/
│   │   │   ├── scanner/          # Barcode scanner page
│   │   │   ├── search/           # Product search page
│   │   │   ├── history/          # Scan history page
│   │   │   └── product-detail/   # Product details page
│   │   ├── services/
│   │   │   ├── barcode-scanner.service.ts  # Scanner logic
│   │   │   └── product.service.ts          # Product data management
│   │   ├── app.component.ts      # Root component
│   │   ├── app.module.ts         # App module
│   │   └── app-routing.module.ts # Routing
│   ├── assets/
│   │   └── data/
│   │       ├── grocery-products.json      # Grocery products data
│   │       └── stationery-products.json   # Stationery products data
│   ├── theme/
│   │   └── variables.scss        # Theme variables
│   ├── global.scss               # Global styles
│   └── index.html                # Main HTML
├── android/                      # Android native project
├── ios/                         # iOS native project
├── capacitor.config.ts          # Capacitor configuration
├── angular.json                 # Angular configuration
├── package.json                 # Dependencies
└── tsconfig.json               # TypeScript config
```

## How to Use

### 1. Scan a Product

1. Open the app
2. Tap "Start Scanning"
3. Point your camera at a barcode
4. Product details will appear

### 2. Search for Products

1. Go to "Search" tab
2. Type product name, brand, or SKU
3. Tap on a product to view details

### 3. View History

1. Go to "History" tab
2. See all previously scanned products
3. Tap to view details again

## Permissions

The app requires:

- **Camera** - For barcode scanning
- **Storage** - For offline product database

## Customization

### Add More Products

Edit the JSON files in `src/assets/data/`:

```json
{
  "sku": "ST5000001",
  "upc": "750123456789",
  "name": "Product Name",
  "brand": "Brand",
  "category": "Category",
  "price": 99.99,
  "available": true,
  "store": "Store Name"
}
```

### Change Theme Colors

Edit `src/theme/variables.scss`:

```scss
:root {
  --ion-color-primary: #3880ff;
  --ion-color-secondary: #3dc2ff;
  // ... more colors
}
```

### Modify Camera Settings

Edit `capacitor.config.ts`:

```typescript
plugins: {
  BarcodeScanner: {
    scanInstructions: 'Your custom message',
    scanningText: 'Scanning...'
  }
}
```

## Troubleshooting

### Camera Not Working

- Check camera permissions in device settings
- Rebuild the app: `ionic capacitor sync`
- Clear cache: `ionic capacitor sync --force`

### Products Not Loading

- Verify JSON files are in `src/assets/data/`
- Check file names match in `product.service.ts`
- Rebuild: `ionic build && ionic capacitor sync`

### Build Errors

```powershell
# Clean and reinstall
Remove-Item -Recurse -Force node_modules, www
npm install
ionic build
```

## Development Commands

```powershell
# Serve in browser
ionic serve

# Build for production
ionic build --prod

# Sync with native projects
ionic capacitor sync

# Run on Android
ionic capacitor run android

# Run on iOS
ionic capacitor run ios

# Generate new page
ionic generate page pages/my-page

# Generate new service
ionic generate service services/my-service
```

## Performance Tips

1. **Optimize Images** - Use compressed images
2. **Lazy Loading** - Pages are lazy-loaded by default
3. **Product Data** - Keep JSON files under 5MB each
4. **Index Products** - For faster searching (implement in service)

## Security

- Product data is stored locally (no server required)
- No user data is collected
- Camera access only when scanning
- Offline-first approach

## Future Enhancements

- [ ] Add product favorites
- [ ] Export scan history to CSV
- [ ] Compare prices across stores
- [ ] Add barcode generation
- [ ] Implement product recommendations
- [ ] Add shopping list feature
- [ ] Cloud sync for history
- [ ] Multi-language support

## Resources

- [Ionic Documentation](https://ionicframework.com/docs)
- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Angular Documentation](https://angular.io/docs)
- [Barcode Scanner Plugin](https://github.com/capacitor-community/barcode-scanner)

## License

MIT

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review Ionic/Capacitor documentation
3. Check device permissions and settings

---

**Built with ❤️ using Ionic Framework**
