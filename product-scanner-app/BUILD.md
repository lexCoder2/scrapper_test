# Product Scanner App - Build & Deploy Guide

## Quick Start

```powershell
# Run setup script
.\setup.ps1

# Start development server
ionic serve
```

## Manual Setup

### 1. Install Dependencies

```powershell
npm install
```

### 2. Copy Product Data

```powershell
# Create directories
New-Item -Path "src/assets/data" -ItemType Directory -Force

# Copy files (use your actual file names)
Copy-Item "../mexico_grocery_sample_20251118_162048.json" -Destination "src/assets/data/grocery-products.json"
Copy-Item "../stationery_products_20251118_162642.json" -Destination "src/assets/data/stationery-products.json"
```

### 3. Test in Browser

```powershell
ionic serve
```

## Build for Android

```powershell
# First time setup
ionic capacitor add android

# Build and sync
ionic build
ionic capacitor sync android

# Open in Android Studio
ionic capacitor open android

# Or run directly
ionic capacitor run android
```

## Build for iOS (macOS only)

```powershell
# First time setup
ionic capacitor add ios

# Build and sync
ionic build
ionic capacitor sync ios

# Open in Xcode
ionic capacitor open ios

# Or run directly
ionic capacitor run ios
```

## Android Permissions

Add to `android/app/src/main/AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-feature android:name="android.hardware.camera" />
```

## iOS Permissions

Add to `ios/App/App/Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>We need camera access to scan product barcodes</string>
```

## Troubleshooting

### "ionic: command not found"

```powershell
npm install -g @ionic/cli
```

### Camera not working on device

1. Check permissions in device settings
2. Rebuild: `ionic capacitor sync android --force`
3. Clear app data and reinstall

### Products not loading

1. Verify JSON files exist in `src/assets/data/`
2. Check browser console for errors
3. Rebuild: `ionic build && ionic capacitor sync`

## Production Build

```powershell
# Build optimized version
ionic build --prod

# Sync to native projects
ionic capacitor sync

# Generate signed APK in Android Studio
# Or signed IPA in Xcode
```

## App Icons & Splash Screen

1. Place your icon at `resources/icon.png` (1024x1024)
2. Place your splash at `resources/splash.png` (2732x2732)
3. Run: `ionic capacitor resources`

## Testing

```powershell
# Unit tests
npm test

# E2E tests
npm run e2e

# Lint
npm run lint
```
