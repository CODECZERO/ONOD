import { Router } from "express";
import { saveData, issueData } from "../controler/vendore.controler.js";
const router = Router();
router.route("/VendeorReg").post(saveData);
router.route("/issue").post(issueData);
export default router;
