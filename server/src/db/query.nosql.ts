import { ApiError } from "aptos";
import { IVendor } from "../controler/vendore.controler.js";
import BirthRecord  from "../model/user.model.js";
import Vendeor from "../model/vendor.model.js";
//user query here

const findWalletId=async(uniqueId:string)=>{
    try {
        return await BirthRecord.find({uniqueId});
    } catch (error) {
        return error;
    }
}

const dataSave=async(data:IVendor)=>{
    try {
        return await Vendeor.create(data);
    } catch (error) {
        return error;
    }
}

const checkUser=async(email:string)=>{
    try {
        const findUser = await Vendeor.findOne({ email });
        if(!findUser) return null;
        return findUser;
    } catch (error) {
         throw new ApiError(500, "Database error: " + (error as Error).message);
    }
}

// Define a common interface for the documents we're querying
interface IWalletHolder extends Document {
  uniqueID: string;
  privateKey: string;
  walletId: string;
  email: string;
}

/**
 * Finds the wallet and private key associated with a given email address.
 * It searches both the Vendor and User collections.
 *
 * @param {string} email The email of the entity to find.
 * @returns {Promise<{uniqueID: string, privateKey: string, walletId: string} | null>}
 * The wallet details if found, otherwise null.
 */
const getWalletAndPrivateKey = async (email: string) => {
  const query = { email: email };

  // 1. Search for a vendor with the provided email
  const vendor = await Vendeor.findOne(query).lean<IWalletHolder>();
  if (vendor) {
    return {
      uniqueID: vendor.uniqueID,
      privateKey: vendor.privateKey,
      walletId:vendor.walletId,
    };
  }

  // 2. If no vendor is found, search for a user
  const user = await BirthRecord.findOne(query).lean<IWalletHolder>();
  if (user) {
    return {
      uniqueID: user.uniqueID,
      privateKey: user.privateKey,
      walletId:user.walletId,
    };
  }

  // 3. If neither is found, return null
  return null;
};


const storeTransactionId = async (identifier: string, transactionId: string) => {
 try {
   // Check identifier type: email, uniqueID, or walletAddress
   let query;
   
   if (identifier.includes('@')) {
     // Email
     query = { email: identifier };
   } else if (identifier.startsWith('0x')) {
     // Wallet address (starts with 0x)
     query = { walletAddress: identifier };
   } else {
     // UniqueID (numeric)
     query = { uniqueID: identifier };
   }

   // Add transaction ID to vendor (prevents duplicates)
   const vendor = await Vendeor.findOneAndUpdate(
     query,
     { $addToSet: { transId: transactionId } }, // $addToSet prevents duplicates
     { new: true }
   );

   if (!vendor) {
     throw new Error("Vendor not found");
   }

   return vendor;
 } catch (error) {
   console.error("Error storing transaction:", error);
   throw new Error(`Failed to store transaction: ${(error as Error).message}`);
 }
};
export{
    findWalletId,
    dataSave,
    checkUser,
    getWalletAndPrivateKey,
    storeTransactionId,


}