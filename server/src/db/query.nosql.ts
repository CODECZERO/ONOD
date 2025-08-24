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

const getWalletAndPrivateKey = async (identifier: string) => {
 try {
   // Check if identifier is email (contains @) or uniqueID
   const isEmail = identifier.includes('@');
   
   const query = isEmail 
     ? { email: identifier }
     : { uniqueID: identifier };
   
   const vendor = await Vendeor.findOne(query).lean<IVendor>();
   
   if (!vendor) {
     throw new ApiError(404, "Vendor not found");
   }

   return {
     uniqueID: vendor.uniqueID,
     privateKey: vendor.privateKey,
     walletId: vendor.walletId
   };
 } catch (error) {
   if (error instanceof ApiError) {
     throw error;
   }
   throw new ApiError(500, "Database error: " + (error as Error).message);
 }
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