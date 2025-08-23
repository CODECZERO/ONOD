import { Router } from "express";
import {verfiyUser} from "../midelware/verfiy.midelware.js";
const router=Router();

router.route("/Datahandel").post(verfiyUser,);

