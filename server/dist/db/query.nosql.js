var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { ApiError } from "aptos";
import BirthRecord from "../model/user.model.js";
import Vendeor from "../model/vendor.model.js";
//user query here
const findWalletId = (uniqueId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        return yield BirthRecord.find({ uniqueId });
    }
    catch (error) {
        return error;
    }
});
const dataSave = (data) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        return yield Vendeor.create(data);
    }
    catch (error) {
        return error;
    }
});
const checkUser = (email) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const findUser = yield Vendeor.findOne({ email });
        if (!findUser)
            return null;
        return findUser;
    }
    catch (error) {
        throw new ApiError(500, "Database error: " + error.message);
    }
});
/**
 * Finds the wallet and private key associated with a given email address.
 * It searches both the Vendor and User collections.
 *
 * @param {string} email The email of the entity to find.
 * @returns {Promise<{uniqueID: string, privateKey: string, walletId: string} | null>}
 * The wallet details if found, otherwise null.
 */
const getWalletAndPrivateKey = (email) => __awaiter(void 0, void 0, void 0, function* () {
    const query = { email: email };
    // 1. Search for a vendor with the provided email
    const vendor = yield Vendeor.findOne(query).lean();
    if (vendor) {
        return {
            uniqueID: vendor.uniqueID,
            privateKey: vendor.privateKey,
            walletId: vendor.walletId,
        };
    }
    // 2. If no vendor is found, search for a user
    const user = yield BirthRecord.findOne(query).lean();
    if (user) {
        return {
            uniqueID: user.uniqueID,
            privateKey: user.privateKey,
            walletId: user.walletId,
        };
    }
    // 3. If neither is found, return null
    return null;
});
const storeTransactionId = (identifier, transactionId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        // Check identifier type: email, uniqueID, or walletAddress
        let query;
        if (identifier.includes('@')) {
            // Email
            query = { email: identifier };
        }
        else if (identifier.startsWith('0x')) {
            // Wallet address (starts with 0x)
            query = { walletAddress: identifier };
        }
        else {
            // UniqueID (numeric)
            query = { uniqueID: identifier };
        }
        // Add transaction ID to vendor (prevents duplicates)
        const vendor = yield Vendeor.findOneAndUpdate(query, { $addToSet: { transId: transactionId } }, // $addToSet prevents duplicates
        { new: true });
        if (!vendor) {
            throw new Error("Vendor not found");
        }
        return vendor;
    }
    catch (error) {
        console.error("Error storing transaction:", error);
        throw new Error(`Failed to store transaction: ${error.message}`);
    }
});
export { findWalletId, dataSave, checkUser, getWalletAndPrivateKey, storeTransactionId, };
