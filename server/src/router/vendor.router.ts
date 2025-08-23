import { Router } from "express";
import { saveData,createWalletId,login, issueData } from "../controler/vendore.controler.js";
import { verfiyUser } from "../midelware/verfiy.midelware.js";
const router=Router();

router.route("/VendeorReg").post(saveData);
router.route("/issue").post(issueData);


export default router;