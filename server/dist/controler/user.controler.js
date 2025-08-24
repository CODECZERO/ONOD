var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { AptosConnect } from "../db/aptos.config.js";
import { ApiError } from "../util/apiError.js";
import { createWalletId } from "./vendore.controler.js";
import BirthRecord from "../model/user.model.js";
const clinet = AptosConnect();
//this function take's a walletAdrress and give's
//user a unique id
const userUpdateData = (userData) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const creatWallet = yield createWalletId();
        const newRecord = Object.assign(Object.assign({}, userData), { walletId: creatWallet.accountAddress, privateKey: creatWallet.privateKey });
        const saveData = yield BirthRecord.create(newRecord);
        return saveData;
    }
    catch (error) {
        throw new ApiError(400, `some error occure user data update${error}`);
    }
});
/**
 * Finds a birth record using either uniqueID, walletId, or email.
 * It intelligently determines the identifier type to perform the search.
 * @param {string} identifier - The uniqueID, walletId, or email to search for.
 * @returns {Promise<IBirthRecord | null>} The found birth record document or null if not found.
 */
const findRecordByIdentifier = (identifier) => __awaiter(void 0, void 0, void 0, function* () {
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
        }
        else if (identifier.startsWith('0x')) {
            // If it starts with '0x', assume it's a wallet ID.
            query = { walletId: identifier };
        }
        else {
            // Otherwise, assume it's a uniqueID.
            query = { uniqueID: identifier };
        }
        // Search the database using the constructed query
        const foundRecord = yield BirthRecord.findOne(query).lean();
        // Return the found record (will be null if not found)
        return foundRecord;
    }
    catch (error) {
        // Handle any database or Mongoose errors and throw a consistent API error
        throw new ApiError(500, `Database error during record lookup: ${error.message}`);
    }
});
export { userUpdateData, findRecordByIdentifier };
