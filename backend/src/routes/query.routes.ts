import { Router } from "express";
import { generateQueryController } from "../controllers/query.controller";

const router = Router();
router.post("/generate", generateQueryController);

export default router;
