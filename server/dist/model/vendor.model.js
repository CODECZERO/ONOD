import mongoose from "mongoose";
import { customAlphabet } from "nanoid";
const nanoid = customAlphabet("0123456789", 12); // only digits, 12 characters long
const venSchema = new mongoose.Schema({
    uniqueID: {
        type: String,
        index: true,
        unique: true,
        default: () => nanoid(),
    },
    transId: [
        {
            type: String,
        }
    ],
    password: {
        type: String,
        require: true,
    },
    privateKey: {
        type: String,
        require: true
    },
    orgName: {
        type: String,
        require: true,
    },
    regNo: {
        type: String,
        require: true,
    },
    orgType: {
        type: String,
        require: true,
    },
    name: {
        type: String,
        require: true,
    },
    contact: {
        type: Number,
        require: true,
    },
    email: {
        type: String,
        require: true,
    },
    orgAddr: {
        type: String,
        require: true,
    },
    city: {
        type: String,
        require: true,
    },
    state: {
        type: String,
        require: true,
    },
    country: {
        type: String,
        require: true,
    },
    websiteUrl: {
        type: String,
        require: true,
    },
});
const Vendeor = mongoose.model("Vendor", venSchema);
export default Vendeor;
