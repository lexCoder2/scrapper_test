# Product Scanner App - Quick Setup Script

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  PRODUCT SCANNER APP - SETUP" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

$appPath = "C:\Users\IRWIN\OneDrive\Documentos\n8n\product-scanner-app"

# Check if we're in the right directory
if (-not (Test-Path $appPath)) {
    Write-Host "Error: App directory not found!" -ForegroundColor Red
    exit 1
}

Set-Location $appPath

Write-Host "Step 1: Installing dependencies..." -ForegroundColor Green
npm install

Write-Host "`nStep 2: Creating assets directory..." -ForegroundColor Green
New-Item -Path "src/assets/data" -ItemType Directory -Force | Out-Null
New-Item -Path "src/assets/img" -ItemType Directory -Force | Out-Null

Write-Host "`nStep 3: Copying product data..." -ForegroundColor Green

# Find the most recent product files
$groceryFile = Get-ChildItem -Path ".." -Filter "mexico_grocery_sample_*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$stationeryFile = Get-ChildItem -Path ".." -Filter "stationery_products_*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($groceryFile) {
    Copy-Item $groceryFile.FullName -Destination "src/assets/data/grocery-products.json"
    Write-Host "  ✓ Copied grocery products" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Grocery products file not found" -ForegroundColor Yellow
}

if ($stationeryFile) {
    Copy-Item $stationeryFile.FullName -Destination "src/assets/data/stationery-products.json"
    Write-Host "  ✓ Copied stationery products" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Stationery products file not found" -ForegroundColor Yellow
}

Write-Host "`nStep 4: Building the app..." -ForegroundColor Green
ionic build

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test in browser: ionic serve" -ForegroundColor White
Write-Host "  2. Add Android: ionic capacitor add android" -ForegroundColor White
Write-Host "  3. Add iOS: ionic capacitor add ios" -ForegroundColor White
Write-Host "  4. Build & sync: ionic build && ionic capacitor sync`n" -ForegroundColor White

Write-Host "To run the app now:" -ForegroundColor Yellow
Write-Host "  ionic serve`n" -ForegroundColor Cyan
