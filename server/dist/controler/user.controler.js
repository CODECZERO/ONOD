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
import AsyncHandler from "../util/asycHanlder.js";
const clinet = AptosConnect();
//this function take's a walletAdrress and give's
//user a unique id
const Uia = AsyncHandler((req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const walletId = req.body;
}));
