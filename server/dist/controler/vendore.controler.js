var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import AsyncHandler from "../util/asycHanlder.js";
import { ApiError } from "../util/apiError.js";
import { ApiResponse } from "../util/apiResponse.js";
import { dataSave, checkUser, getWalletAndPrivateKey, storeTransactionId } from "../db/query.nosql.js";
import bcrypt from "bcrypt";
import { Account, } from "@aptos-labs/ts-sdk";
import { AptosConnect, readTransaction, submitTnx } from "../db/aptos.config.js";
const client = AptosConnect();
const createWalletId = () => __awaiter(void 0, void 0, void 0, function* () {
    const user = yield Account.generate();
    const wallet = {
        privateKey: user.privateKey.toString(),
        publicKey: user.publicKey.toString(),
        accountAddress: user.accountAddress.toString(),
    };
    return wallet;
});
const saveData = AsyncHandler((req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const user = req.body;
    const existingUser = yield checkUser(user.email); // `checkUser` should use `Vendor.findOne()`
    if (existingUser) {
        throw new ApiError(400, "User with this email already exists");
    }
    const pass = yield bcrypt.hash(user.password, 10);
    const walletData = yield createWalletId();
    const data = yield dataSave(Object.assign(Object.assign({}, user), { password: pass, walletId: walletData.accountAddress, privateKey: walletData.privateKey }));
    return res.status(200).json(new ApiResponse(200, data, "Regerstion done"));
}));
const BlockData = (data) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        // Try to store document directly (if store exists)
        const storePayload = {
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
            const submitData = yield submitTnx(data, storePayload);
            return submitData;
        }
        catch (error) {
            // If it fails with MutBorrowGlobal, try init_store first
            if (error.message.includes('MutBorrowGlobal')) {
                const initPayload = {
                    function: "0xa0d9331d0634419f53581c11c9d8ff6c8c57457f57d7911df07eb9b57afebe7a::storeModule::init_store",
                    typeArguments: [],
                    functionArguments: [],
                };
                yield submitTnx(data, initPayload);
                return yield submitTnx(data, storePayload);
            }
            throw error;
        }
    }
    catch (error) {
        console.error("Error in BlockData:", error);
        return error;
    }
});
const storeOtherFu = AsyncHandler((req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const data = req.body;
    console.log(data);
    const datasaver = BlockData(data);
    return res.status(200).json(new ApiResponse(200, datasaver, "datasave"));
}));
const login = AsyncHandler((req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const { email, password } = req.body; // Use 'password' to match the frontend payload
    // Step 1: Check for missing credentials from the request body
    if (!email || !password) {
        throw new ApiError(400, "Email and password are required.");
    }
    // Step 2: Find the user in the database
    const user = yield checkUser(email);
    // Step 3: Check if the user was found
    if (!user) {
        throw new ApiError(404, "Invalid email or password.");
    }
    // Step 4: Compare the provided password with the stored hashed password
    const passwordMatch = yield bcrypt.compare(password, user === null || user === void 0 ? void 0 : user.password);
    // Step 5: Check if the passwords match
    if (!passwordMatch) {
        throw new ApiError(401, "Invalid email or password.");
    }
    // Step 6: If all checks pass, return a successful response
    return res.status(200).json(new ApiResponse(200, user, "Login successful."));
}));
const issueData = AsyncHandler((req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const testData = req.body;
    if (!testData)
        throw new ApiError(400, "invalid data");
    const findDataIssuer = yield getWalletAndPrivateKey(testData.issuer);
    const createAcoount = yield createWalletId();
    //create code wallet here and then store it
    const findDataReciver = yield getWalletAndPrivateKey(createAcoount.accountAddress);
    const updateData = Object.assign(Object.assign({}, testData), { issuer: findDataIssuer === null || findDataIssuer === void 0 ? void 0 : findDataIssuer.walletId, privateKey: findDataIssuer === null || findDataIssuer === void 0 ? void 0 : findDataIssuer.privateKey, receiver: findDataReciver === null || findDataReciver === void 0 ? void 0 : findDataReciver.walletId });
    if (!updateData)
        throw new ApiError(404, "Invaild data");
    const saveDataonChain = yield BlockData(updateData);
    const saveData = yield storeTransactionId(updateData.issuer, saveDataonChain);
    return res.status(200).json(new ApiResponse(200, saveData));
}));
const readTra = AsyncHandler((req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const { transId } = req.body;
    if (!transId)
        throw new ApiError(400, "Invalid id");
    const read = yield readTransaction(transId);
    return res.status(200).json(new ApiResponse(200, read));
}));
export { saveData, login, createWalletId, issueData, readTra, BlockData, storeOtherFu };
