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
import { dataSave, checkUser } from "../db/query.nosql.js";
import bcrypt from "bcrypt";
import { Account, } from "@aptos-labs/ts-sdk";
import { AptosConnect, submitTnx } from "../db/aptos.config.js";
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
    const pass = yield bcrypt.hash(user.password, 10);
    const walletData = yield createWalletId();
    const data = yield dataSave(Object.assign(Object.assign({}, user), { password: pass, walletId: walletData.accountAddress, privateKey: walletData.privateKey }));
    return res.status(200).json(new ApiResponse(200, data, "Regerstion done"));
}));
const BlockData = (data) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        // Construct the payload for the Move function
        const payload = {
            function: "0x6b7bf296ecb04c37b5ac861ef63ca74cca1dda1694778fb29677c56de5202995::storeModule::store_document",
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
        const submitData = yield submitTnx(data, payload);
        return submitData;
    }
    catch (error) {
        console.error("Error in BlockData:", error);
        return error;
    }
});
const login = AsyncHandler((req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const { email, pass } = req.body;
    if (!email || !pass)
        throw new ApiError(400, "Not data is provied");
    const check = yield checkUser(email);
    if (!check)
        throw new ApiError(404, check);
    const compareCode = yield bcrypt.compare(pass, check === null || check === void 0 ? void 0 : check.password);
    if (!compareCode)
        throw new ApiError(401, "INVALID PASSWORD");
    return res.status(200).json(new ApiResponse(200, check, "user found"));
}));
const issueData = AsyncHandler((req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const testData = req.body;
    if (!testData)
        throw new ApiError(400, "invalid data");
    const saveDataonChain = yield BlockData(testData);
    return res.status(200).json(new ApiResponse(200, saveDataonChain));
}));
export { saveData, login, createWalletId, issueData };
