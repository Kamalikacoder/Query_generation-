import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";
import app from "./app";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.resolve(__dirname, "../.env") });

const PORT = Number(process.env.PORT) || 4000;

app.listen(PORT, "0.0.0.0", () => {
  console.log(`\n🚀 Backend server started on http://localhost:${PORT}`);
  console.log("🛠️  Available endpoints:");
  console.log("   - GET  /api/health");
  console.log("   - POST /api/query/generate\n");
});
