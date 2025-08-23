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
import { AptosConnect } from "../db/aptos.config.js";
const verfiyUser = AsyncHandler((req, res, next) => __awaiter(void 0, void 0, void 0, function* () {
    //find's if user exist on block-chain or not;
    const user = req.body;
    if (!user.walletId)
        throw new ApiError(400, "Invalid user");
    const client = yield AptosConnect();
    const verfiy = yield (client === null || client === void 0 ? void 0 : client.account.getAccountInfo({ accountAddress: user === null || user === void 0 ? void 0 : user.walletId }));
    if (!verfiy)
        req.body = false;
    req.body = verfiy;
    next();
}));
export { verfiyUser, };
