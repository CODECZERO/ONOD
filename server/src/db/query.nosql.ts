import { User } from "../model/user.model.js";

//user query here

const findWalletId=async(uniqeId:string)=>{
    try {
        return await User.findOne()
    } catch (error) {
        
    }
}