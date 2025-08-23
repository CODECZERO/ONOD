import { AptosConnect } from "../db/aptos.config.js";
import { ApiError } from "../util/apiError.js";
import { ApiResponse } from "../util/apiResponse.js";
import AsyncHandler from "../util/asycHanlder.js";
import { Request,Response } from "express";
const clinet=AptosConnect();


//this function take's a walletAdrress and give's
//user a unique id

const Uia=AsyncHandler(async(req:Request,res:Response)=>{
    const walletId=req.body;
});