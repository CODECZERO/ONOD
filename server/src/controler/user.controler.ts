import { AptosConnect } from "../db/aptos.config.js";
import { ApiError } from "../util/apiError.js";
import { ApiResponse } from "../util/apiResponse.js";
import AsyncHandler from "../util/asycHanlder.js";

const clinet=AptosConnect();


//this function take's a walletAdrress and give's
//user a unique id

const Uia=