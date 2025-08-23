//this file created to make sure that during the application start, all other services are ready
//like kafka,rabbitmq,databases,redis,websocket,etc;
//after starting all this services it will start main app;
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { ApiError } from "./apiError.js";
import { closeDb, connectDb } from "../db/mongo.db.js";
import { AptosConnect } from "../db/aptos.config.js";
let mongodbConenction;
const connectAll = () => __awaiter(void 0, void 0, void 0, function* () {
    try {
        mongodbConenction = yield connectDb();
        console.log("Mongodb is Runing");
        yield AptosConnect();
        console.log("aptos is runing");
    }
    catch (error) {
        throw new ApiError(500, `Service is down ${error}`);
    }
});
const closeAll = () => __awaiter(void 0, void 0, void 0, function* () {
    try {
        yield closeDb(mongodbConenction);
        console.log("mongodb connection is close");
    }
    catch (error) {
        throw new ApiError(500, `something went wrong while closeing conenction ${error}`);
    }
});
// this function close all the serverices in server using process in node js
process.on('SIGINT', () => __awaiter(void 0, void 0, void 0, function* () {
    yield closeAll();
    console.log("Disconnected All service");
    process.exit(0);
}));
process.on('SIGTERM', () => __awaiter(void 0, void 0, void 0, function* () {
    yield closeAll();
    console.log("Disconnected All service");
    process.exit(0);
}));
export default connectAll;
