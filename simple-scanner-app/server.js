const https = require("https");
const fs = require("fs");
const path = require("path");
const http = require("http");

const PORT = 8443;

// SSL options
const options = {
  key: fs.readFileSync(path.join(__dirname, "key.pem")),
  cert: fs.readFileSync(path.join(__dirname, "cert.pem")),
};

// MIME types
const mimeTypes = {
  ".html": "text/html",
  ".js": "text/javascript",
  ".json": "application/json",
  ".css": "text/css",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
};

const server = https.createServer(options, (req, res) => {
  // Add CORS headers
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  let filePath = "." + req.url;
  if (filePath === "./") {
    filePath = "./index.html";
  }

  // Handle parent directory requests for JSON files
  if (filePath.startsWith("./../")) {
    filePath = "." + filePath.substring(3);
  }

  const extname = String(path.extname(filePath)).toLowerCase();
  const contentType = mimeTypes[extname] || "application/octet-stream";

  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code == "ENOENT") {
        // Try to find in parent directory
        const parentPath = path.join(__dirname, "..", path.basename(filePath));
        fs.readFile(parentPath, (err, parentContent) => {
          if (err) {
            res.writeHead(404, { "Content-Type": "text/html" });
            res.end("<h1>404 Not Found</h1>", "utf-8");
          } else {
            res.writeHead(200, { "Content-Type": contentType });
            res.end(parentContent, "utf-8");
          }
        });
      } else {
        res.writeHead(500);
        res.end("Server Error: " + error.code);
      }
    } else {
      res.writeHead(200, { "Content-Type": contentType });
      res.end(content, "utf-8");
    }
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`HTTPS Server running at:`);
  console.log(`  https://localhost:${PORT}`);
  console.log(`  https://192.168.6.98:${PORT}`);
  console.log(
    `\nNote: You'll need to accept the self-signed certificate warning in your browser.`
  );
});
