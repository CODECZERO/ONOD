import {Aptos,AptosConfig,Network} from "@aptos-labs/ts-sdk";
import AsyncHandler from "../util/asycHanlder.js";
import {NextFunction,Request,Response} from "express";
import {ApiError} from "../util/apiError.js";
import { AptosConnect } from "../db/aptos.config.js";
import { ApiResponse } from "../util/apiResponse.js";

interface userData{
  walletId:string
}

const verfiyUser=AsyncHandler(async(req:Request,res:Response):Promise<boolean>=>{
  //find's if user exist on block-chain or not;
  const user:userData=req.body;
  if(!user.walletId) throw new ApiError(400,"Invalid user");
  const client=await AptosConnect();
  const verfiy=await client?.account.getAccountInfo({accountAddress:user?.walletId});
  if(!verfiy) return false;
  return true;
})

export {
    userData,
    verfiyUser,
}