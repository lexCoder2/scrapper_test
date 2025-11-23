const express = require("express");
const https = require("https");
const fs = require("fs");
const path = require("path");
const { MongoClient, ObjectId } = require("mongodb");
const cors = require("cors");
const compression = require("compression");

const app = express();
const PORT = process.env.PORT || 3000;
const HTTPS_PORT = process.env.HTTPS_PORT || 3443;
const MONGODB_URI =
  process.env.MONGODB_URI ||
  "mongodb://admin:productdb2025@mongodb:27017/products?authSource=admin";

// SSL options for HTTPS
const sslOptions = {
  key: fs.readFileSync(path.join(__dirname, "key.pem")),
  cert: fs.readFileSync(path.join(__dirname, "cert.pem")),
};

let db;
let productsCollection;

// Middleware
app.use(cors());
app.use(compression());
app.use(express.json({ limit: "50mb" }));

// Connect to MongoDB
async function connectDB() {
  try {
    const client = await MongoClient.connect(MONGODB_URI, {
      maxPoolSize: 50,
      minPoolSize: 10,
      serverSelectionTimeoutMS: 5000,
    });

    db = client.db("products");
    productsCollection = db.collection("grocery_products");

    console.log("Connected to MongoDB successfully");

    // Create indexes if they don't exist
    await productsCollection.createIndex({ sku: 1 }, { unique: true });
    await productsCollection.createIndex({ ean13: 1 });
    await productsCollection.createIndex({ upc: 1 });
    await productsCollection.createIndex({
      name: "text",
      brand: "text",
      category: "text",
    });
    await productsCollection.createIndex({ store: 1 });
    await productsCollection.createIndex({ category: 1 });
    await productsCollection.createIndex({ brand: 1 });
    await productsCollection.createIndex({ price: 1 });

    console.log("Indexes created/verified");
  } catch (error) {
    console.error("MongoDB connection error:", error);
    process.exit(1);
  }
}

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

// Get all products (with pagination)
app.get("/api/products", async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 50;
    const skip = (page - 1) * limit;

    const products = await productsCollection
      .find({})
      .skip(skip)
      .limit(limit)
      .toArray();

    const total = await productsCollection.countDocuments();

    res.json({
      products,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit),
      },
    });
  } catch (error) {
    console.error("Error fetching products:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Get all products (no pagination) - for app compatibility
app.get("/api/products/all", async (req, res) => {
  try {
    const products = await productsCollection
      .find({})
      .project({ _id: 0 }) // Exclude MongoDB _id
      .toArray();

    res.json(products);
  } catch (error) {
    console.error("Error fetching all products:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Search products
app.get("/api/products/search", async (req, res) => {
  try {
    const query = req.query.q;
    const limit = parseInt(req.query.limit) || 50;

    if (!query) {
      return res.status(400).json({ error: "Search query required" });
    }

    // Check if query is numeric (barcode search)
    const isNumeric = /^\d+$/.test(query);

    let products;
    if (isNumeric) {
      // Search by SKU, UPC, or EAN13
      products = await productsCollection
        .find({
          $or: [
            { sku: { $regex: query, $options: "i" } },
            { upc: { $regex: query, $options: "i" } },
            { ean13: { $regex: query, $options: "i" } },
          ],
        })
        .limit(limit)
        .toArray();
    } else {
      // Text search
      products = await productsCollection
        .find({ $text: { $search: query } }, { score: { $meta: "textScore" } })
        .sort({ score: { $meta: "textScore" } })
        .limit(limit)
        .toArray();
    }

    res.json(products);
  } catch (error) {
    console.error("Error searching products:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Get product by barcode
app.get("/api/products/barcode/:barcode", async (req, res) => {
  try {
    const { barcode } = req.params;

    const product = await productsCollection.findOne({
      $or: [{ ean13: barcode }, { upc: barcode }, { sku: barcode }],
    });

    if (!product) {
      return res.status(404).json({ error: "Product not found" });
    }

    res.json(product);
  } catch (error) {
    console.error("Error fetching product by barcode:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Get product by SKU
app.get("/api/products/sku/:sku", async (req, res) => {
  try {
    const { sku } = req.params;

    const product = await productsCollection.findOne({ sku });

    if (!product) {
      return res.status(404).json({ error: "Product not found" });
    }

    res.json(product);
  } catch (error) {
    console.error("Error fetching product by SKU:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Get statistics
app.get("/api/stats", async (req, res) => {
  try {
    const total = await productsCollection.countDocuments();

    const stores = await productsCollection.distinct("store");
    const brands = await productsCollection.distinct("brand");
    const categories = await productsCollection.distinct("category");

    res.json({
      totalProducts: total,
      totalStores: stores.length,
      totalBrands: brands.length,
      totalCategories: categories.length,
      stores,
    });
  } catch (error) {
    console.error("Error fetching stats:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Filter products by store
app.get("/api/products/store/:store", async (req, res) => {
  try {
    const { store } = req.params;
    const limit = parseInt(req.query.limit) || 100;

    const products = await productsCollection
      .find({ store })
      .limit(limit)
      .toArray();

    res.json(products);
  } catch (error) {
    console.error("Error fetching products by store:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Filter products by category
app.get("/api/products/category/:category", async (req, res) => {
  try {
    const { category } = req.params;
    const limit = parseInt(req.query.limit) || 100;

    const products = await productsCollection
      .find({ category: new RegExp(category, "i") })
      .limit(limit)
      .toArray();

    res.json(products);
  } catch (error) {
    console.error("Error fetching products by category:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Bulk import products
app.post("/api/products/import", async (req, res) => {
  try {
    const products = req.body;

    if (!Array.isArray(products) || products.length === 0) {
      return res.status(400).json({ error: "Invalid products array" });
    }

    // Use bulk operations for better performance
    const operations = products.map((product) => ({
      updateOne: {
        filter: { sku: product.sku },
        update: { $set: product },
        upsert: true,
      },
    }));

    const result = await productsCollection.bulkWrite(operations, {
      ordered: false,
    });

    res.json({
      success: true,
      inserted: result.upsertedCount,
      updated: result.modifiedCount,
      total: products.length,
    });
  } catch (error) {
    console.error("Error importing products:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Start servers (both HTTP and HTTPS)
connectDB().then(() => {
  // HTTP Server on port 3000
  app.listen(PORT, "0.0.0.0", () => {
    console.log(`\n${"=".repeat(60)}`);
    console.log(`Product API - HTTP Server`);
    console.log(`${"=".repeat(60)}`);
    console.log(`Running on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
    console.log(`API endpoint: http://localhost:${PORT}/api/products`);
    console.log(`${"=".repeat(60)}\n`);
  });

  // HTTPS Server on port 3443
  https.createServer(sslOptions, app).listen(HTTPS_PORT, "0.0.0.0", () => {
    console.log(`${"=".repeat(60)}`);
    console.log(`Product API - HTTPS Server`);
    console.log(`${"=".repeat(60)}`);
    console.log(`Running on port ${HTTPS_PORT}`);
    console.log(`Health check: https://localhost:${HTTPS_PORT}/health`);
    console.log(`API endpoint: https://localhost:${HTTPS_PORT}/api/products`);
    console.log(`LAN Access: https://192.168.6.98:${HTTPS_PORT}/api`);
    console.log(`${"=".repeat(60)}\n`);
  });
});

// Graceful shutdown
process.on("SIGINT", async () => {
  console.log("Shutting down gracefully...");
  process.exit(0);
});
