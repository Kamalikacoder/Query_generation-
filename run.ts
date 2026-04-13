import app from "./app/main";

const PORT = 3000;

app.listen(PORT, "0.0.0.0", () => {
  console.log(`
🚀 Query Generation Module is running!
📡 URL: http://0.0.0.0:${PORT}
🛠️  Endpoints:
   - GET  /
   - GET  /health
   - POST /api/generate-query
  `);
});
