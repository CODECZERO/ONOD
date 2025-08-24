import { Router } from "express";
import { saveData,createWalletId,login, issueData, readTra } from "../controler/vendore.controler.js";
import { verfiyUser } from "../midelware/verfiy.midelware.js";
const router=Router();

router.route("/vendeorReg").post(saveData);
router.route("/VendeorLogin").post(login);
router.route("/issue").post(issueData);
router.route("/readData").get(readTra);


export default router;