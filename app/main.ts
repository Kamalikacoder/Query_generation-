import express from "express";
import cors from "cors";
import queryRoutes from "./routes/query_routes";

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

/**
 * GET /
 * Welcome message and module status.
 */
app.get("/", (req, res) => {
  res.json({
    module: "Query Generation Module",
    status: "Active",
    purpose: "Convert clinical claims into PubMed-friendly queries",
    version: "1.0.0"
  });
});

/**
 * GET /health
 * Health check endpoint.
 */
app.get("/health", (req, res) => {
  res.json({ status: "healthy", timestamp: new Date().toISOString() });
});

// Routes
app.use("/api", queryRoutes);

export default app;
