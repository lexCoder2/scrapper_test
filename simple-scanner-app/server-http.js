const express = require("express");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 8080;

// Serve static files from current directory
app.use(express.static(__dirname));

// Handle all routes by serving index.html
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.listen(PORT, "0.0.0.0", () => {
  console.log("\n" + "=".repeat(60));
  console.log("📱 Product Scanner App - HTTP Server");
  console.log("=".repeat(60));
  console.log(`\n✅ Server running at:`);
  console.log(`   http://localhost:${PORT}`);
  console.log(`   http://192.168.6.98:${PORT}`);
  console.log(`\n📡 API Connection: http://192.168.6.98:3000/api`);
  console.log(`\n⚠️  Note: Use this HTTP server for LAN access`);
  console.log(`   - No certificate warnings`);
  console.log(`   - No mixed content issues`);
  console.log(`   - Works on all devices\n`);
  console.log("=".repeat(60) + "\n");
});
