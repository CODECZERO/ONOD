import { Router } from "express";
import {verfiyUser} from "../midelware/verfiy.midelware.js";
import { loginUser, userUpdateData } from "../controler/user.controler.js";
const router=Router();

router.route("/createUser").post(userUpdateData);
router.route("/loginUser").post(loginUser);

export default router