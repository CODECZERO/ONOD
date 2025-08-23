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
import { User } from "../model/user.model.js";
import Vendeor from "../model/vendor.model.js";
//user query here
const findWalletId = (uniqueId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        return yield User.find({ uniqueId });
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
        const findUser = Vendeor.find({ email }).lean();
        if (!findUser)
            return null;
        return findUser;
    }
    catch (error) {
        throw new ApiError(500, "Database error: " + error.message);
    }
});
export { findWalletId, dataSave, checkUser };
