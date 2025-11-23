# Product Scanner - Simple Version

Aplicación web simple para escanear y buscar productos sin necesidad de instalar Ionic.

## ✨ Características

- 📷 **Escaneo de códigos de barras** con la cámara
- 🔍 **Búsqueda de productos** por nombre, marca o SKU
- 📊 **Estadísticas** de la base de datos
- 💾 **Funciona sin internet** (una vez cargados los datos)
- 📱 **Responsive** - Funciona en móvil y escritorio

## 🚀 Cómo Usar

### Opción 1: Servidor Local Simple

```powershell
cd simple-scanner-app
python -m http.server 8000
```

Abre: `http://localhost:8000`

### Opción 2: Live Server (VS Code)

1. Instala la extensión "Live Server" en VS Code
2. Click derecho en `index.html`
3. Selecciona "Open with Live Server"

### Opción 3: Node.js

```powershell
npx http-server simple-scanner-app -p 8000
```

## 📱 Uso en Móvil

1. En tu red local, abre: `http://[TU-IP]:8000`
2. Permite el acceso a la cámara
3. Apunta a un código de barras

## 🌐 Navegadores Compatibles

- ✅ **Chrome/Edge** (Android/Desktop) - Soporte completo
- ✅ **Safari** (iOS) - Soporte completo
- ⚠️ **Firefox** - Búsqueda manual (sin detección automática)

## 🗄️ Integración con API

La app se conecta automáticamente al Product API para cargar todos los productos:

- **Endpoint**: `http://localhost:3000/api/products/all`
- **Total productos**: 13,653 productos
- **Tiendas**: 4 tiendas mexicanas
  - 🛒 Chedraui (2,548 productos)
  - 🍬 Dulces Balu (3,283 productos)
  - 🏪 La Comer (6,549 productos)
  - 📝 Papelerias Tony (792 productos)
- **Fallback**: Si la API no está disponible, usa archivos JSON locales

### Configuración API

En `app.js`:

```javascript
const API_BASE_URL = "http://localhost:3000/api";
const USE_API = true; // Cambiar a false para usar archivos locales
```

## 📦 Base de Datos

La app carga automáticamente:

- `mexico_grocery_sample_20251118_162048.json` (2,000 productos de abarrotes)
- `stationery_products_20251118_162642.json` (2,000 productos de papelería)

**Total: 4,000+ productos**

## 🔧 Troubleshooting

### La cámara no funciona

- Verifica permisos del navegador
- Usa HTTPS o localhost
- Prueba en Chrome/Safari

### Productos no cargan

- Verifica que los archivos JSON estén en la carpeta padre (`../`)
- Revisa la consola del navegador (F12)
- Actualiza las rutas en `app.js` si es necesario

### BarcodeDetector no disponible

- Usa Chrome 83+ o Edge 83+
- En iOS, usa Safari 14+
- Como alternativa, busca manualmente por el código

## 💡 Ventajas vs Ionic

- ✅ **No requiere instalación** de CLI
- ✅ **No requiere build** ni compilación
- ✅ **Más ligero** y rápido
- ✅ **Fácil de modificar** - solo HTML/CSS/JS
- ✅ **Funciona inmediatamente** en cualquier servidor web

## 📝 Personalización

### Cambiar colores

Edita las variables en `index.html`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Agregar más productos

Actualiza las rutas en `app.js`:

```javascript
const response = await fetch("../tu-archivo.json");
```

## 🌟 Características Futuras

- [ ] PWA instalable
- [ ] Generar códigos QR
- [ ] Compartir productos
- [ ] Guardar favoritos
- [ ] Modo oscuro
- [ ] Múltiples idiomas

## 📱 Convertir a APK/IPA

Si quieres una app nativa:

1. Usa [PWA Builder](https://www.pwabuilder.com/)
2. Ingresa la URL de tu app
3. Descarga el paquete para Android/iOS

## 🎯 Testing

1. **Búsqueda Manual**: Funciona en todos los navegadores
2. **Escaneo con Cámara**: Requiere Chrome/Safari moderno
3. **Responsive**: Prueba en diferentes tamaños de pantalla

---

**¡Listo para usar! Solo abre el archivo en un servidor web** 🚀
