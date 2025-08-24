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
import { ApiResponse } from "../util/apiResponse.js";
import AsyncHandler from "../util/asycHanlder.js";
import { createWalletId } from "./vendore.controler.js";
import BirthRecord from "../model/user.model.js";
import { BlockData } from "./vendore.controler.js";
import { nanoid } from "nanoid";
import bcrypt from "bcrypt";
import { checkUser } from "../db/query.nosql.js";
const clinet = AptosConnect();
//this function take's a walletAdrress and give's
//user a unique id
const userUpdateData = (userData) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const creatWallet = yield createWalletId();
        const pass = nanoid(12);
        const password = yield bcrypt.hash(pass, 12);
        const newRecord = Object.assign(Object.assign({}, userData), { walletId: creatWallet.accountAddress, privateKey: creatWallet.privateKey, password: password });
        const saveData = yield BirthRecord.create(newRecord);
        const saveDataK = {
            issuer: userData.issuer,
            receiver: creatWallet.accountAddress,
            docType: "Birth_Certificate",
            docId: saveData.uniqueID,
            metaData: {
                // Core immutable birth data
                babyName: saveData.babyName,
                gender: saveData.gender,
                birthDate: saveData.birthDate.toISOString(),
                timeOfBirth: saveData.timeOfBirth,
                placeOfBirth: saveData.placeOfBirth,
                // Parental information
                fatherName: saveData.fatherName,
                fatherId: saveData.fatherId,
                motherName: saveData.motherName,
                motherId: saveData.motherId,
                // Address information
                address: saveData.address,
                city: saveData.city,
                state: saveData.state,
                country: saveData.country,
                // System metadata
                mongoId: saveData._id.toString(),
                registrationTimestamp: saveData.createdAt.toISOString(),
                issuerWallet: process.env.GOVERNMENT_ISSUER_WALLET,
                // Contact information (mutable data)
                contactInfo: {
                    fatherContact: saveData.fatherContact,
                    fatherEmail: saveData.fatherEmail,
                    motherContact: saveData.motherContact,
                    motherEmail: saveData.motherEmail,
                },
            },
            chain: [], // Empty for new documents, will contain previous versions for amendments
            privateKey: creatWallet.privateKey, // If needed for transaction signing
            issued_at: Math.floor(new Date().getTime() / 1000),
        };
        yield BlockData(saveDataK);
        return saveData;
    }
    catch (error) {
        throw new ApiError(400, `some error occure user data update${error}`);
    }
});
//this fucntion will whatsapp user , their email and passwrod
//or it's equivalnet number
const regUser = AsyncHandler((req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const userData = req.body;
    if (!userData)
        throw new ApiError(400, "Bad data");
    const result = yield userUpdateData(userData);
    if (!result)
        throw new ApiError(404, "user not found");
    return res.status(200).json(new ApiResponse(200, result));
}));
const loginUser = AsyncHandler((req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const { email, password } = req.body;
    if (!email || !password)
        throw new ApiError(400, "Bad request");
    const getUser = yield checkUser(email);
    if (!getUser)
        throw new ApiError(404, "user not found");
    const comp = yield bcrypt.compare(password, getUser === null || getUser === void 0 ? void 0 : getUser.password);
    if (!comp)
        throw new ApiError(401, "unautohrized code ");
    return getUser;
}));
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
        if (identifier.includes("@")) {
            // If it contains '@', assume it's an email.
            // Check both father and mother emails.
            query = {
                $or: [{ fatherEmail: identifier }, { motherEmail: identifier }],
            };
        }
        else if (identifier.startsWith("0x")) {
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
export { userUpdateData, findRecordByIdentifier, regUser, loginUser };
