import { AptosConnect } from "../db/aptos.config.js";
import { ApiError } from "../util/apiError.js";
import { ApiResponse } from "../util/apiResponse.js";
import AsyncHandler from "../util/asycHanlder.js";
import { Request,Response } from "express";
import { createWalletId } from "./vendore.controler.js";
import BirthRecord from "../model/user.model.js";
import { BlockDataTS,BlockData } from "./vendore.controler.js";
const clinet=AptosConnect();


interface IBirthRecord {
  uniqueID: string;
  walletId: string;
  privateKey: string;
  transId: string[];
  babyName: string;
  gender: string;
  birthDate: Date;
  timeOfBirth: string;
  placeOfBirth: string;
  fatherName: string;
  fatherId: string;
  fatherContact: string;
  fatherEmail: string;
  motherName: string;
  motherId: string;
  motherContact: string;
  motherEmail: string;
  address: string;
  city: string;
  state: string;
  country: string;
  createdAt?: Date; // Added by `timestamps: true`
  updatedAt?: Date; // Added by `timestamps: true`
}

interface SaveBlock extends BlockDataTS{
    
}
//this function take's a walletAdrress and give's
//user a unique id



const userUpdateData=async(userData:IBirthRecord)=>{
    try {
        const creatWallet=await createWalletId();
        const newRecord={
            ...userData,
            walletId:creatWallet.accountAddress,
            privateKey:creatWallet.privateKey,
        };
        const saveData=await BirthRecord.create(newRecord);
        return saveData;
    } catch (error) {
        throw new ApiError(400,`some error occure user data update${error}`);
    }
};


/**
 * Finds a birth record using either uniqueID, walletId, or email.
 * It intelligently determines the identifier type to perform the search.
 * @param {string} identifier - The uniqueID, walletId, or email to search for.
 * @returns {Promise<IBirthRecord | null>} The found birth record document or null if not found.
 */
const findRecordByIdentifier = async (identifier: string): Promise<IBirthRecord | null> => {
    try {
        let query;

        // Determine the type of identifier and build the query object
        if (identifier.includes('@')) {
            // If it contains '@', assume it's an email.
            // Check both father and mother emails.
            query = {
                $or: [
                    { fatherEmail: identifier },
                    { motherEmail: identifier }
                ]
            };
        } else if (identifier.startsWith('0x')) {
            // If it starts with '0x', assume it's a wallet ID.
            query = { walletId: identifier };
        } else {
            // Otherwise, assume it's a uniqueID.
            query = { uniqueID: identifier };
        }

        // Search the database using the constructed query
        const foundRecord = await BirthRecord.findOne(query).lean<IBirthRecord>();

        // Return the found record (will be null if not found)
        return foundRecord;

    } catch (error) {
        // Handle any database or Mongoose errors and throw a consistent API error
        throw new ApiError(500, `Database error during record lookup: ${(error as Error).message}`);
    }
};

export {
    userUpdateData,findRecordByIdentifier

}