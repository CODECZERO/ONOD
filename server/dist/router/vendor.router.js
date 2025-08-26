import { Router } from "express";
import { saveData, login, issueData, readTra, storeOtherFu } from "../controler/vendore.controler.js";
const router = Router();
router.route("/vendeorReg").post(saveData);
router.route("/VendeorLogin").post(login);
router.route("/issue").post(issueData);
router.route("/readData").post(readTra);
router.route("/trainIssue").post(storeOtherFu);
export default router;
