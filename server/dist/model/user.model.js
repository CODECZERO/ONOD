import mongoose from "mongoose";
const userSchema = new mongoose.Schema({
    uniqueId: {
        type: String,
        require: true,
        index: true
    },
    walletId: {
        type: String,
        require: true,
        index: true
    },
    issuedDocument: {
        type: [{
                docType: {
                    type: String,
                    require: true
                },
                docHash: {
                    type: String,
                    require: true
                },
                createdAt: {
                    type: Date,
                    default: Date.now
                }
            }]
    }
}, { timestamps: true });
const User = mongoose.model("User", userSchema);
export { User };
