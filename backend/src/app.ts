import cors from "cors";
import express from "express";
import queryRoutes from "./routes/query.routes";
import { errorHandler, notFoundHandler } from "./middleware/error.middleware";

const app = express();

app.use(cors({ origin: ["http://localhost:5173", "http://127.0.0.1:5173"] }));
app.use(express.json());

app.get("/api/health", (_, res) => {
  return res.json({ success: true, message: "backend running" });
});

app.use("/api/query", queryRoutes);
app.use(notFoundHandler);
app.use(errorHandler);

export default app;
