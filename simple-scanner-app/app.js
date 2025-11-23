// Product Scanner App - Simple Version
let products = [];
let currentStream = null;

// API Configuration - Accessible from LAN with HTTPS
// Automatically detects protocol and hostname
const getApiBaseUrl = () => {
  // If on localhost, use localhost URL with HTTPS
  if (
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
  ) {
    return "https://localhost:3443/api";
  }
  // For LAN access, use HTTPS on port 3443
  return `https://${window.location.hostname}:3443/api`;
};

const API_BASE_URL = getApiBaseUrl();
const USE_API = true;

console.log(`🔧 API Configuration: ${API_BASE_URL}`);

// Load product data from API only (no JSON fallback)
async function loadProducts() {
  try {
    console.log(`Loading products from API: ${API_BASE_URL}/products/all`);

    const response = await fetch(`${API_BASE_URL}/products/all`, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(
        `API returned status ${response.status}: ${response.statusText}`
      );
    }

    products = await response.json();
    console.log(`✅ Successfully loaded ${products.length} products from API`);
    console.log(
      `📊 Stores included: ${[...new Set(products.map((p) => p.store))].join(
        ", "
      )}`
    );

    updateStats();
    updateProductCount();
  } catch (error) {
    console.error("❌ Error loading products from API:", error);
    showPopup(
      "⚠️ Error de Conexión",
      `<p><strong>No se pudieron cargar los productos desde la API.</strong></p>
       <p style="margin-top: 12px; font-size: 13px; color: #666;"><strong>API URL:</strong><br/><code style="background: #f3f4f6; padding: 4px 8px; border-radius: 4px; display: block; margin-top: 4px; word-break: break-all;">${API_BASE_URL}/products/all</code></p>
       <p style="margin-top: 12px; font-size: 13px; color: #666;"><strong>Error:</strong> ${error.message}</p>
       <p style="margin-top: 16px; font-size: 14px;"><strong>Verifica que:</strong></p>
       <ul style="margin: 8px 0 0 20px; font-size: 13px; color: #666; line-height: 1.8;">
         <li>La API esté ejecutándose (puerto 3443)</li>
         <li>La URL sea accesible desde este dispositivo</li>
         <li>No haya problemas de CORS o firewall</li>
       </ul>`,
      "error"
    );
    throw error;
  }
}

// Show popup modal (replaces alert)
function showPopup(title, message, type = "info") {
  const modal = document.getElementById("popupModal");
  const header = document.getElementById("popupHeader");
  const titleEl = document.getElementById("popupTitle");
  const bodyEl = document.getElementById("popupBody");

  // Set icon based on type
  const icons = {
    error: '<i class="fas fa-exclamation-circle"></i>',
    warning: '<i class="fas fa-exclamation-triangle"></i>',
    success: '<i class="fas fa-check-circle"></i>',
    info: '<i class="fas fa-info-circle"></i>',
  };

  // Set colors based on type
  const colors = {
    error: "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
    warning: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
    success: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
    info: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
  };

  header.style.background = colors[type] || colors.info;
  titleEl.innerHTML = `${icons[type] || icons.info} ${title}`;
  bodyEl.innerHTML = `<div style="font-size: 14px; line-height: 1.6; color: #374151;">${message}</div>`;

  modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

// Close popup modal
function closePopup() {
  const modal = document.getElementById("popupModal");
  modal.classList.remove("active");
  document.body.style.overflow = "auto";
}

// Update statistics
function updateStats() {
  document.getElementById("totalProducts").textContent =
    products.length.toLocaleString();

  const stores = new Set(products.map((p) => p.store));
  document.getElementById("totalStores").textContent = stores.size;

  const brands = new Set(products.map((p) => p.brand));
  document.getElementById("totalBrands").textContent = brands.size;

  const categories = new Set(products.map((p) => p.category));
  document.getElementById("totalCategories").textContent = categories.size;
}

// Update product count in search
function updateProductCount() {
  const countEl = document.getElementById("productCount");
  const quickCountEl = document.getElementById("quickProductCount");

  if (countEl) {
    countEl.textContent = `${products.length.toLocaleString()} productos`;
  }
  if (quickCountEl) {
    quickCountEl.textContent = products.length.toLocaleString();
  }
}

// Normalize text: remove accents, punctuation, and extra spaces
function normalizeText(text) {
  if (!text) return "";
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // Remove accents
    .replace(/[^\w\s]/g, " ") // Replace punctuation with space
    .replace(/\s+/g, " ") // Collapse multiple spaces
    .trim();
}

// Calculate Levenshtein distance for fuzzy matching
function levenshteinDistance(str1, str2) {
  const len1 = str1.length;
  const len2 = str2.length;
  const matrix = Array(len2 + 1)
    .fill(null)
    .map(() => Array(len1 + 1).fill(0));

  for (let i = 0; i <= len1; i++) matrix[0][i] = i;
  for (let j = 0; j <= len2; j++) matrix[j][0] = j;

  for (let j = 1; j <= len2; j++) {
    for (let i = 1; i <= len1; i++) {
      const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
      matrix[j][i] = Math.min(
        matrix[j][i - 1] + 1, // deletion
        matrix[j - 1][i] + 1, // insertion
        matrix[j - 1][i - 1] + cost // substitution
      );
    }
  }

  return matrix[len2][len1];
}

// Check if query matches text with fuzzy logic
function fuzzyMatch(text, query) {
  const normalizedText = normalizeText(text);
  const normalizedQuery = normalizeText(query);

  // Exact match after normalization
  if (normalizedText.includes(normalizedQuery)) {
    return { match: true, score: 100 };
  }

  // Split into words for partial matching
  const textWords = normalizedText.split(" ");
  const queryWords = normalizedQuery.split(" ");

  // Check if all query words exist in text (allows reordering)
  const allWordsMatch = queryWords.every((qWord) =>
    textWords.some((tWord) => tWord.includes(qWord) || qWord.includes(tWord))
  );

  if (allWordsMatch) {
    return { match: true, score: 90 };
  }

  // Fuzzy matching for single word queries
  if (queryWords.length === 1 && normalizedQuery.length >= 3) {
    for (const word of textWords) {
      if (word.length < 3) continue;

      const distance = levenshteinDistance(word, normalizedQuery);
      const maxLen = Math.max(word.length, normalizedQuery.length);
      const similarity = ((maxLen - distance) / maxLen) * 100;

      // Allow up to 2 character differences for words >= 5 chars
      if (similarity >= 70 || (normalizedQuery.length >= 5 && distance <= 2)) {
        return { match: true, score: similarity };
      }
    }
  }

  // Multi-word fuzzy matching
  if (queryWords.length > 1) {
    let matchedWords = 0;
    let totalScore = 0;

    for (const qWord of queryWords) {
      if (qWord.length < 3) {
        matchedWords++;
        totalScore += 100;
        continue;
      }

      let bestScore = 0;
      for (const tWord of textWords) {
        if (tWord.length < 3) continue;

        const distance = levenshteinDistance(tWord, qWord);
        const maxLen = Math.max(tWord.length, qWord.length);
        const similarity = ((maxLen - distance) / maxLen) * 100;

        if (similarity > bestScore) {
          bestScore = similarity;
        }
      }

      if (bestScore >= 70) {
        matchedWords++;
        totalScore += bestScore;
      }
    }

    const matchRatio = matchedWords / queryWords.length;
    if (matchRatio >= 0.6) {
      // At least 60% of words match
      return {
        match: true,
        score: (totalScore / queryWords.length) * matchRatio,
      };
    }
  }

  return { match: false, score: 0 };
}

// Search products with robust fuzzy matching
function searchProducts(query) {
  const searchTerm = query.trim();

  if (!searchTerm || searchTerm.length < 2) {
    return [];
  }

  // For numeric searches (SKU, UPC, EAN, etc.), use exact matching across all barcode fields
  const isNumeric = /^\d+$/.test(searchTerm);
  if (isNumeric) {
    return products
      .filter(
        (p) =>
          p.sku.includes(searchTerm) ||
          (p.ean13 && p.ean13.includes(searchTerm)) ||
          (p.upc && p.upc.includes(searchTerm)) ||
          (p.ean && p.ean.includes(searchTerm)) ||
          (p.multi_ean && p.multi_ean.includes(searchTerm)) ||
          (p.art_ean && p.art_ean.includes(searchTerm)) ||
          (p.art_cod && p.art_cod.includes(searchTerm)) ||
          (p.item_ean && p.item_ean.includes(searchTerm)) ||
          (p.product_reference && p.product_reference.includes(searchTerm)) ||
          (p.product_reference_code &&
            p.product_reference_code.includes(searchTerm)) ||
          (p.reference && p.reference.includes(searchTerm)) ||
          (p.product_id && p.product_id.includes(searchTerm))
      )
      .slice(0, 50);
  }

  // Score each product and filter
  const scoredProducts = products
    .map((p) => {
      const nameMatch = fuzzyMatch(p.name, searchTerm);
      const brandMatch = fuzzyMatch(p.brand, searchTerm);
      const categoryMatch = fuzzyMatch(p.category, searchTerm);

      // Best score wins
      const bestScore = Math.max(
        nameMatch.score,
        brandMatch.score * 0.8, // Brand is slightly less important
        categoryMatch.score * 0.6 // Category is even less important
      );

      return {
        product: p,
        score: bestScore,
        match: nameMatch.match || brandMatch.match || categoryMatch.match,
      };
    })
    .filter((item) => item.match && item.score >= 60) // Minimum 60% similarity
    .sort((a, b) => b.score - a.score) // Sort by score descending
    .slice(0, 50)
    .map((item) => item.product);

  return scoredProducts;
}

// Search by barcode - Enhanced with all barcode fields
function searchByBarcode(barcode) {
  const cleanBarcode = barcode.trim();

  // Try exact match first across ALL barcode fields
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

  // Try partial match if no exact match found (for truncated barcodes)
  if (!product && cleanBarcode.length >= 6) {
    const barcodeUpper = cleanBarcode.toUpperCase();
    product = products.find(
      (p) =>
        (p.ean13 && p.ean13.includes(cleanBarcode)) ||
        (p.upc && p.upc.includes(cleanBarcode)) ||
        (p.ean && p.ean.includes(cleanBarcode)) ||
        (p.multi_ean && p.multi_ean.includes(cleanBarcode)) ||
        (p.art_ean && p.art_ean.includes(cleanBarcode)) ||
        (p.item_ean && p.item_ean.includes(cleanBarcode)) ||
        (p.sku && p.sku.toUpperCase().includes(barcodeUpper)) ||
        (p.product_reference &&
          p.product_reference.toUpperCase().includes(barcodeUpper)) ||
        (p.product_reference_code &&
          p.product_reference_code.toUpperCase().includes(barcodeUpper)) ||
        (p.reference && p.reference.toUpperCase().includes(barcodeUpper)) ||
        (p.product_id && p.product_id.includes(cleanBarcode))
    );
  }

  return product;
}

// Display search results
function displaySearchResults(results) {
  const container = document.getElementById("searchResults");

  if (results.length === 0) {
    container.innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                </svg>
                <h3>No se encontraron productos</h3>
                <p>Intenta con otro término de búsqueda</p>
            </div>
        `;
    return;
  }

  const html = results
    .map((product) => {
      const imageSrc = product.local_image
        ? `../${product.local_image}`
        : product.image_url ||
          'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="%23ccc" stroke-width="2"%3E%3Crect x="3" y="3" width="18" height="18" rx="2"/%3E%3Ccircle cx="8.5" cy="8.5" r="1.5"/%3E%3Cpath d="M21 15l-5-5L5 21"/%3E%3C/svg%3E';

      const discountBadge =
        product.discount_percentage > 0
          ? `<span class="badge badge-discount">-${product.discount_percentage}%</span>`
          : "";

      // Display barcode info
      const barcodeInfo = product.ean13
        ? `<div style="font-size: 11px; color: #9ca3af; font-family: monospace; margin-top: 2px;">
             <i class="fas fa-barcode" style="font-size: 10px;"></i> ${product.ean13}
           </div>`
        : product.upc
        ? `<div style="font-size: 11px; color: #9ca3af; font-family: monospace; margin-top: 2px;">
             <i class="fas fa-barcode" style="font-size: 10px;"></i> ${product.upc}
           </div>`
        : "";

      return `
        <div class="product-card" onclick='showProductDetail(${JSON.stringify(
          product
        ).replace(/'/g, "&apos;")})'>
            <img src="${imageSrc}" alt="${
        product.name
      }" class="product-image" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\"http://www.w3.org/2000/svg\\" width=\\"60\\" height=\\"60\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"%23ccc\\" stroke-width=\\"2\\"%3E%3Crect x=\\"3\\" y=\\"3\\" width=\\"18\\" height=\\"18\\" rx=\\"2\\"/%3E%3Ccircle cx=\\"8.5\\" cy=\\"8.5\\" r=\\"1.5\\"/%3E%3Cpath d=\\"M21 15l-5-5L5 21\\"/%3E%3C/svg%3E'">
            <div class="product-details">
                <div class="product-header">
                    <div class="product-name">${product.name}</div>
                </div>
                ${barcodeInfo}
                <div class="product-info">
                    <span>${product.brand}</span>
                    <span>•</span>
                    <span>${product.store}</span>
                    ${discountBadge}
                </div>
            </div>
            <div style="display: flex; flex-direction: column; align-items: flex-end; justify-content: center; gap: 8px;">
                <div class="product-price">$${product.price.toFixed(2)}</div>
                <div class="product-chevron">›</div>
            </div>
        </div>
    `;
    })
    .join("");

  container.innerHTML = `
        <div style="margin-bottom: 15px; color: #666; font-size: 14px;">
            Se encontraron ${results.length} producto(s)
        </div>
        <div class="product-list">${html}</div>
    `;
}

// Show product detail in modal
function showProductDetail(product) {
  const modal = document.getElementById("productModal");
  const modalBody = document.getElementById("modalBody");

  const imageSrc = product.local_image
    ? `../${product.local_image}`
    : product.image_url ||
      'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 24 24" fill="none" stroke="%23ccc" stroke-width="2"%3E%3Crect x="3" y="3" width="18" height="18" rx="2"/%3E%3Ccircle cx="8.5" cy="8.5" r="1.5"/%3E%3Cpath d="M21 15l-5-5L5 21"/%3E%3C/svg%3E';

  const discountBadge =
    product.discount_percentage > 0
      ? `<span class="modal-badge badge-discount"><i class="fas fa-tag"></i> -${product.discount_percentage}% OFF</span>`
      : "";

  const availableBadge = product.available
    ? '<span class="modal-badge badge-success"><i class="fas fa-check-circle"></i> Disponible</span>'
    : '<span class="modal-badge badge-danger"><i class="fas fa-times-circle"></i> Agotado</span>';

  const listPriceHTML =
    product.list_price > product.price
      ? `<div class="modal-list-price">Antes: $${product.list_price.toFixed(
          2
        )} ${product.currency}</div>`
      : "";

  const ratingHTML = product.rating
    ? `
    <div class="detail-row">
      <div class="detail-label">⭐ Rating</div>
      <div class="detail-value">${product.rating}/5.0 (${
        product.reviews_count || 0
      } opiniones)</div>
    </div>
  `
    : "";

  const sizeHTML = product.size
    ? `
    <div class="detail-row">
      <div class="detail-label">📏 Tamaño</div>
      <div class="detail-value">${product.size}</div>
    </div>
  `
    : "";

  const descriptionHTML = product.description
    ? `
    <div class="detail-section">
      <h3 style="margin-bottom: 10px; font-size: 16px;">📝 Descripción</h3>
      <p style="color: #666; line-height: 1.6; font-size: 14px;">${product.description}</p>
    </div>
  `
    : "";

  modalBody.innerHTML = `
    <img src="${imageSrc}" alt="${product.name}" class="modal-product-image" 
         onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\"http://www.w3.org/2000/svg\\" width=\\"250\\" height=\\"250\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"%23ccc\\" stroke-width=\\"2\\"%3E%3Crect x=\\"3\\" y=\\"3\\" width=\\"18\\" height=\\"18\\" rx=\\"2\\"/%3E%3Ccircle cx=\\"8.5\\" cy=\\"8.5\\" r=\\"1.5\\"/%3E%3Cpath d=\\"M21 15l-5-5L5 21\\"/%3E%3C/svg%3E'">
    
    <h2 class="modal-product-name">${product.name}</h2>
    
    <div class="modal-price-section">
      <div class="modal-price">$${product.price.toFixed(2)} ${
    product.currency
  }</div>
      ${listPriceHTML}
      <div class="modal-badges">
        ${availableBadge}
        ${discountBadge}
      </div>
    </div>

    <div class="detail-section">
      <div class="detail-row">
        <div class="detail-label"><i class="fas fa-tag"></i> Marca</div>
        <div class="detail-value">${product.brand}</div>
      </div>
      <div class="detail-row">
        <div class="detail-label"><i class="fas fa-store"></i> Tienda</div>
        <div class="detail-value">${product.store}</div>
      </div>
      <div class="detail-row">
        <div class="detail-label"><i class="fas fa-box"></i> Categoría</div>
        <div class="detail-value">${product.category}</div>
      </div>
      ${sizeHTML}
      <div class="detail-row">
        <div class="detail-label"><i class="fas fa-cubes"></i> Stock</div>
        <div class="detail-value">${product.stock} unidades</div>
      </div>
      ${ratingHTML}
    </div>

    <div class="detail-section">
      <h3 style="margin-bottom: 10px; font-size: 16px; display: flex; align-items: center; gap: 8px;"><i class="fas fa-barcode"></i> Códigos de Barras</h3>
      <div class="detail-row">
        <div class="detail-label"><i class="fas fa-hashtag"></i> SKU</div>
        <div class="detail-value" style="font-family: monospace;">${
          product.sku
        }</div>
      </div>
      ${
        product.ean13
          ? `<div class="detail-row"><div class="detail-label"><i class="fas fa-barcode"></i> EAN-13</div><div class="detail-value" style="font-family: monospace;">${product.ean13}</div></div>`
          : ""
      }
      ${
        product.upc
          ? `<div class="detail-row"><div class="detail-label"><i class="fas fa-qrcode"></i> UPC</div><div class="detail-value" style="font-family: monospace;">${product.upc}</div></div>`
          : ""
      }
      ${
        product.ean
          ? `<div class="detail-row"><div class="detail-label"><i class="fas fa-barcode"></i> EAN (Item)</div><div class="detail-value" style="font-family: monospace;">${product.ean}</div></div>`
          : ""
      }
      ${
        product.multi_ean
          ? `<div class="detail-row"><div class="detail-label"><i class="fas fa-barcode"></i> Multi EAN</div><div class="detail-value" style="font-family: monospace;">${product.multi_ean}</div></div>`
          : ""
      }
      ${
        product.art_ean
          ? `<div class="detail-row"><div class="detail-label"><i class="fas fa-barcode"></i> Article EAN</div><div class="detail-value" style="font-family: monospace;">${product.art_ean}</div></div>`
          : ""
      }
      ${
        product.art_cod
          ? `<div class="detail-row"><div class="detail-label"><i class="fas fa-hashtag"></i> Article Code</div><div class="detail-value" style="font-family: monospace;">${product.art_cod}</div></div>`
          : ""
      }
      ${
        product.item_ean
          ? `<div class="detail-row"><div class="detail-label"><i class="fas fa-barcode"></i> Item EAN</div><div class="detail-value" style="font-family: monospace;">${product.item_ean}</div></div>`
          : ""
      }
      ${
        product.product_reference
          ? `<div class="detail-row"><div class="detail-label"><i class="fas fa-tag"></i> Product Ref</div><div class="detail-value" style="font-family: monospace;">${product.product_reference}</div></div>`
          : ""
      }
      ${
        product.product_reference_code
          ? `<div class="detail-row"><div class="detail-label"><i class="fas fa-tag"></i> Ref Code</div><div class="detail-value" style="font-family: monospace;">${product.product_reference_code}</div></div>`
          : ""
      }
      ${
        product.reference
          ? `<div class="detail-row"><div class="detail-label"><i class="fas fa-tag"></i> Reference</div><div class="detail-value" style="font-family: monospace;">${product.reference}</div></div>`
          : ""
      }
      ${
        product.product_id
          ? `<div class="detail-row"><div class="detail-label"><i class="fas fa-fingerprint"></i> Product ID</div><div class="detail-value" style="font-family: monospace;">${product.product_id}</div></div>`
          : ""
      }
    </div>

    ${descriptionHTML}
  `;

  modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

// Close product modal
function closeProductModal() {
  const modal = document.getElementById("productModal");
  modal.classList.remove("active");
  document.body.style.overflow = "auto";
}

// Close modal when clicking outside
document.addEventListener("click", (e) => {
  const modal = document.getElementById("productModal");
  if (e.target === modal) {
    closeProductModal();
  }
});

// Camera functions
async function startCamera() {
  try {
    const constraints = {
      video: {
        facingMode: "environment",
        width: { ideal: 1280 },
        height: { ideal: 720 },
      },
    };

    currentStream = await navigator.mediaDevices.getUserMedia(constraints);
    const video = document.getElementById("video");
    video.srcObject = currentStream;

    document.getElementById("cameraContainer").classList.add("active");
    document.getElementById("startScanBtn").style.display = "none";
    document.getElementById("stopScanBtn").style.display = "flex";

    // Start barcode detection (if available)
    if ("BarcodeDetector" in window) {
      startBarcodeDetection(video);
    } else {
      console.log("BarcodeDetector no disponible en este navegador");
      showPopup(
        "⚠️ Funcionalidad No Disponible",
        '<p>Tu navegador no soporta detección automática de códigos de barras.</p><p style="margin-top: 12px;">Por favor usa el <strong>Buscador Manual</strong> en la pestaña de búsqueda.</p>',
        "warning"
      );
    }
  } catch (error) {
    console.error("Error accessing camera:", error);
    showPopup(
      "❌ Error de Cámara",
      '<p>No se pudo acceder a la cámara.</p><p style="margin-top: 12px;">Por favor verifica los permisos de cámara en tu navegador.</p>',
      "error"
    );
  }
}

async function startBarcodeDetection(video) {
  const barcodeDetector = new BarcodeDetector({
    formats: ["ean_13", "ean_8", "upc_a", "upc_e", "code_128"],
  });

  const detectBarcodes = async () => {
    if (!currentStream) return;

    try {
      const barcodes = await barcodeDetector.detect(video);

      if (barcodes.length > 0) {
        const barcode = barcodes[0].rawValue;
        console.log("Barcode detected:", barcode);

        const product = searchByBarcode(barcode);

        if (product) {
          stopCamera();
          showProductDetail(product);
        } else {
          stopCamera();
          showPopup(
            "🔍 Producto No Encontrado",
            `<p><strong>Código escaneado:</strong></p><p style="font-family: monospace; background: #f3f4f6; padding: 8px 12px; border-radius: 6px; margin-top: 8px; font-size: 16px; text-align: center;">${barcode}</p><p style="margin-top: 16px;">Este producto no se encuentra en la base de datos.</p><p style="margin-top: 8px; font-size: 13px; color: #666;">Intenta buscarlo manualmente o verifica que el código sea correcto.</p>`,
            "warning"
          );
        }
      }
    } catch (error) {
      console.error("Error detecting barcode:", error);
    }

    if (currentStream) {
      requestAnimationFrame(detectBarcodes);
    }
  };

  detectBarcodes();
}

function stopCamera() {
  if (currentStream) {
    currentStream.getTracks().forEach((track) => track.stop());
    currentStream = null;
  }

  document.getElementById("cameraContainer").classList.remove("active");
  document.getElementById("startScanBtn").style.display = "flex";
  document.getElementById("stopScanBtn").style.display = "none";
}

// Tab switching
document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", function () {
    // Remove active class from all tabs
    document
      .querySelectorAll(".tab")
      .forEach((t) => t.classList.remove("active"));
    document
      .querySelectorAll(".tab-content")
      .forEach((c) => c.classList.remove("active"));

    // Add active class to clicked tab
    this.classList.add("active");
    const tabId = this.getAttribute("data-tab");
    document.getElementById(tabId).classList.add("active");

    // Stop camera when switching tabs
    if (tabId !== "scanner") {
      stopCamera();
    }
  });
});

// Search input
let searchTimeout;
document.getElementById("searchInput").addEventListener("input", function (e) {
  clearTimeout(searchTimeout);

  const query = e.target.value;

  if (!query || query.length < 2) {
    document.getElementById("searchResults").innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                </svg>
                <h3>Buscar Productos</h3>
                <p>Escribe el nombre, marca o SKU del producto</p>
            </div>
        `;
    return;
  }

  document.getElementById("searchResults").innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Buscando...</p>
        </div>
    `;

  searchTimeout = setTimeout(() => {
    const results = searchProducts(query);
    displaySearchResults(results);
  }, 300);
});

// Switch tab function
function switchTab(tabName) {
  // Update tab buttons
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.remove("active");
    if (tab.dataset.tab === tabName) {
      tab.classList.add("active");
    }
  });

  // Update tab content
  document.querySelectorAll(".tab-content").forEach((content) => {
    content.classList.remove("active");
  });
  document.getElementById(tabName).classList.add("active");
}

// Camera buttons
document.getElementById("startScanBtn").addEventListener("click", startCamera);
document.getElementById("stopScanBtn").addEventListener("click", stopCamera);

// Initialize
loadProducts();

// Show initial empty state
document.getElementById("searchResults").innerHTML = `
    <div class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
        </svg>
        <h3>Buscar Productos</h3>
        <p>Escribe el nombre, marca o SKU del producto</p>
    </div>
`;
