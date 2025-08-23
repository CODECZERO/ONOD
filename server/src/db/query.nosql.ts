import { ApiError } from "aptos";
import { IVendor } from "../controler/vendore.controler.js";
import { User } from "../model/user.model.js";
import Vendeor from "../model/vendor.model.js";
//user query here

const findWalletId=async(uniqueId:string)=>{
    try {
        return await User.find({uniqueId});
    } catch (error) {
        return error;
    }
}

const dataSave=async(data:IVendor)=>{
    try {
        return await Vendeor.create(data);
    } catch (error) {
        return error;
    }
}

const checkUser=async(email:string):Promise<IVendor|null>=>{
    try {
        const findUser=Vendeor.find({email}).lean<IVendor>();
        if(!findUser) return null;
        return findUser;
    } catch (error) {
         throw new ApiError(500, "Database error: " + (error as Error).message);
    }
}



export{
    findWalletId,
    dataSave,
    checkUser

}