import { json, Request, Response } from "express";
import AsyncHandler from "../util/asycHanlder.js";
import { ApiError } from "../util/apiError.js";
import { ApiResponse } from "../util/apiResponse.js";
import { dataSave, checkUser, getWalletAndPrivateKey,storeTransactionId } from "../db/query.nosql.js";
import bcrypt from "bcrypt";
import {
  Account,
  AccountAddress,
  InputGenerateTransactionPayloadData,
  PrivateKey,
  PublicKey,
} from "@aptos-labs/ts-sdk";
import { AptosConnect, readTransaction, submitTnx } from "../db/aptos.config.js";

const client = AptosConnect();
interface IVendor {
  uniqueID?: string;
  walletId?: string;
  privateKey?:string;
  chainData: [string];
  password: string;
  orgName: string;
  regNo: string;
  orgType: string;
  name: string;
  contact: number;
  email: string;
  orgAddr: string;
  city: string;
  state: string;
  country: string;
  websiteUrl: string;
}

interface BlockDataTS {
  issuer: string;
  privateKey?: string;
  receiver: string;
  docType: string;
  docId: string;
  metaData: object;
  chain: string[];
  issued_at?: number;
}

const createWalletId = async () => {
  const user = await Account.generate();
  const wallet = {
    privateKey: user.privateKey.toString(),
    publicKey: user.publicKey.toString(),
    accountAddress: user.accountAddress.toString(),
  };
  return wallet;
};

const saveData = AsyncHandler(async (req: Request, res: Response) => {
  const user: IVendor = req.body;
   const existingUser = await checkUser(user.email); // `checkUser` should use `Vendor.findOne()`
  if (existingUser) {
    throw new ApiError(400, "User with this email already exists");
  }
  const pass = await bcrypt.hash(user.password, 10);
  const walletData = await createWalletId();
  const data = await dataSave({
    ...user,
    password: pass,
    walletId: walletData.accountAddress,
    privateKey:walletData.privateKey,
  });
  return res.status(200).json(new ApiResponse(200, data, "Regerstion done"));
});

const BlockData = async (data: BlockDataTS) => {
  try {
    // Try to store document directly (if store exists)
    const storePayload: InputGenerateTransactionPayloadData = {
      function: "0xa0d9331d0634419f53581c11c9d8ff6c8c57457f57d7911df07eb9b57afebe7a::storeModule::store_document",
      typeArguments: [],
      functionArguments: [
        data.receiver,
        data.docType,
        data.docId,
        JSON.stringify(data.metaData),
        data.chain,
        Math.floor(new Date().getTime() / 1000).toString(),
      ],
    };
    
    try {
      const submitData = await submitTnx(data, storePayload);
      return submitData;
    } catch (error) {
      // If it fails with MutBorrowGlobal, try init_store first
      if (error.message.includes('MutBorrowGlobal')) {
        const initPayload = {
          function: "0xa0d9331d0634419f53581c11c9d8ff6c8c57457f57d7911df07eb9b57afebe7a::storeModule::init_store",
          typeArguments: [],
          functionArguments: [],
        };
        await submitTnx(data, initPayload);
        return await submitTnx(data, storePayload);
      }
      throw error;
    }
    
  } catch (error) {
    console.error("Error in BlockData:", error);
    return error;
  }
};

const storeOtherFu=AsyncHandler(async(req:Request,res:Response)=>{
  const data:BlockDataTS=req.body;
  console.log(data)
  const datasaver=BlockData(data);
  return res.status(200).json(new ApiResponse(200,datasaver,"datasave"));
})
const login = AsyncHandler(async (req, res) => {
  const { email, password } = req.body; // Use 'password' to match the frontend payload
  // Step 1: Check for missing credentials from the request body
  
  if (!email || !password) {
      throw new ApiError(400, "Email and password are required.");
  }

  // Step 2: Find the user in the database
  const user = await checkUser(email);
  // Step 3: Check if the user was found
  if (!user) {
      throw new ApiError(404, "Invalid email or password.");
  }

  // Step 4: Compare the provided password with the stored hashed password
  const passwordMatch = await bcrypt.compare(password, user?.password);

  // Step 5: Check if the passwords match
  if (!passwordMatch) {
      throw new ApiError(401, "Invalid email or password.");
  }

  // Step 6: If all checks pass, return a successful response
  return res.status(200).json(new ApiResponse(200, user, "Login successful."));
});

const issueData = AsyncHandler(async (req: Request, res: Response) => {
  const testData: BlockDataTS = req.body;
  if (!testData) throw new ApiError(400, "invalid data");
  const findDataIssuer= await getWalletAndPrivateKey(testData.issuer);
  const createAcoount=await createWalletId();
  //create code wallet here and then store it
  const findDataReciver= await getWalletAndPrivateKey(createAcoount.accountAddress);
  const updateData:BlockDataTS={
    ...testData,
    issuer:findDataIssuer?.walletId as string,
    privateKey:findDataIssuer?.privateKey as string,
    receiver:findDataReciver?.walletId as string
  }
  if(!updateData) throw new ApiError(404,"Invaild data");
  const saveDataonChain = await BlockData(updateData);
  const saveData=await storeTransactionId(updateData.issuer,saveDataonChain as string);
  return res.status(200).json(new ApiResponse(200, saveData));
});

const readTra=AsyncHandler(async(req:Request,res:Response)=>{
  const {transId}=req.body;
  if(!transId) throw new ApiError(400,"Invalid id");
  const read=await readTransaction(transId);
  return res.status(200).json(new ApiResponse(200,read));
})



export { IVendor, BlockDataTS, saveData, login, createWalletId, issueData,readTra,BlockData,storeOtherFu };
