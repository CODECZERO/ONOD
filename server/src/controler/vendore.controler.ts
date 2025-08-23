import { json, Request, Response } from "express";
import AsyncHandler from "../util/asycHanlder.js";
import { ApiError } from "../util/apiError.js";
import { ApiResponse } from "../util/apiResponse.js";
import { dataSave, checkUser } from "../db/query.nosql.js";
import bcrypt from "bcrypt";
import {
  Account,
  AccountAddress,
  InputGenerateTransactionPayloadData,
  PrivateKey,
  PublicKey,
} from "@aptos-labs/ts-sdk";
import { configDotenv } from "dotenv";
import { AptosConnect, submitTnx } from "../db/aptos.config.js";

const client = AptosConnect();
interface IVendor {
  uniqueID?: string;
  walletId?: string;
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
  privateKey: string;
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
    // Construct the payload for the Move function
    const payload: InputGenerateTransactionPayloadData = {
      function:
        "0x6b7bf296ecb04c37b5ac861ef63ca74cca1dda1694778fb29677c56de5202995::storeModule::store_document",
      typeArguments: [],
      functionArguments: [
        data.receiver, // address string (0x...)
        data.docType, // string
        data.docId, // string
        JSON.stringify(data.metaData), // string
        data.chain, // vector<string>
        Math.floor(new Date().getTime() / 1000),
      ],
    };

    // Submit transaction
    const submitData = await submitTnx(data, payload);
  
    return submitData;
  } catch (error) {
    console.error("Error in BlockData:", error);
    return error;
  }
};

const login = AsyncHandler(async (req: Request, res: Response) => {
  const { email, pass } = req.body;
  if (!email || !pass) throw new ApiError(400, "Not data is provied");
  const check: IVendor | null = await checkUser(email);
  if (!check) throw new ApiError(404, check);
  const compareCode = await bcrypt.compare(pass, check?.password);
  if (!compareCode) throw new ApiError(401, "INVALID PASSWORD");
  return res.status(200).json(new ApiResponse(200, check, "user found"));
});

const issueData = AsyncHandler(async (req: Request, res: Response) => {
  const testData: BlockDataTS = req.body;
  if (!testData) throw new ApiError(400, "invalid data");
  const saveDataonChain = await BlockData(testData);
  return res.status(200).json(new ApiResponse(200, saveDataonChain));
});

export { IVendor, BlockDataTS, saveData, login, createWalletId, issueData };
