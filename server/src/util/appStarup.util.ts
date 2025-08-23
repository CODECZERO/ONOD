//this file created to make sure that during the application start, all other services are ready
//like kafka,rabbitmq,databases,redis,websocket,etc;
//after starting all this services it will start main app;

import { ApiError } from "./apiError.js";
import { closeDb, connectDb } from "../db/mongo.db.js";
import { AptosConnect } from "../db/aptos.config.js";

let mongodbConenction: typeof import("mongoose");

const connectAll = async () => {
    try {
        mongodbConenction = await connectDb();
        console.log("Mongodb is Runing");
        await AptosConnect();
        console.log("aptos is runing");

    } catch (error) {
        throw new ApiError(500, `Service is down ${error}`);
    }
}

const closeAll = async () => {//this function close all connection in server;
    try {
        await closeDb(mongodbConenction);
        console.log("mongodb connection is close");
    } catch (error) {
        throw new ApiError(500, `something went wrong while closeing conenction ${error}`);
    }
}


// this function close all the serverices in server using process in node js
process.on('SIGINT', async () => {
    await closeAll();
    console.log("Disconnected All service");
    process.exit(0);
});

process.on('SIGTERM', async () => {
    await closeAll();
    console.log("Disconnected All service");
    process.exit(0);
});


export default connectAll;