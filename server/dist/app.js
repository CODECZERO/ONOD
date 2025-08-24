import express from "express";
import cors from "cors";
import Vendeor from "./router/vendor.router.js";
import User from "./router/user.router.js";
const app = express();
// allowing data from specifie site to this backend
app.use(cors({
    origin: true, // This allows all origins
    credentials: true
}));
app.use(express.json({ limit: "16kb" }));
app.use(express.urlencoded({ extended: true, limit: "16kb" }));
// Routes
app.use("/api/v1/vendore", Vendeor);
app.use("api/v1/user", User);
app.set("trust proxy", 1);
app.use(express.static("public"));
app.use("/api/v1/vendore", Vendeor);
export default app;
