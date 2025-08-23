var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { Account, Aptos, AptosConfig, Network, Ed25519PrivateKey, } from "@aptos-labs/ts-sdk";
import { HexString } from "aptos";
let client = null;
const AptosConnect = () => __awaiter(void 0, void 0, void 0, function* () {
    //connect aptos blockchain
    try {
        const connectionInstance = new AptosConfig({ network: Network.LOCAL });
        client = new Aptos(connectionInstance);
        return client;
    }
    catch (error) {
        console.log(`There is a error while connecting to netwrk ${error}`);
    }
});
// Helper function to properly format private key hex string
// Helper function to properly format private key hex string
const formatPrivateKeyHex = (keyString) => {
    let hex = keyString.trim();
    // Handle different private key formats
    if (hex.startsWith('ed25519-priv-0x')) {
        // Extract hex part from "ed25519-priv-0x..." format
        hex = hex.slice('ed25519-priv-0x'.length);
    }
    else if (hex.startsWith('0x')) {
        // Standard hex format
        hex = hex.slice(2);
    }
    // Remove any whitespace
    hex = hex.replace(/\s/g, '');
    // Validate hex characters
    if (!/^[0-9a-fA-F]*$/.test(hex)) {
        throw new Error('Invalid hex string: contains non-hex characters');
    }
    // Pad to even length
    if (hex.length % 2 !== 0) {
        hex = '0' + hex;
    }
    // For Ed25519 private keys, ensure 64 characters (32 bytes)
    if (hex.length < 64) {
        hex = hex.padStart(64, '0');
    }
    else if (hex.length > 64) {
        throw new Error(`Private key too long: expected 64 characters, got ${hex.length}`);
    }
    return '0x' + hex;
};
const submitTnx = (data, payload) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        // Validate inputs
        if (!data.privateKey) {
            throw new Error("Private key is required");
        }
        if (!client) {
            throw new Error("Client is not initialized");
        }
        // Create account from private key with proper formatting
        const formattedPrivateKey = formatPrivateKeyHex(data.privateKey);
        const key = HexString.ensure(formattedPrivateKey).toUint8Array();
        const privateKey = new Ed25519PrivateKey(key);
        const account = Account.fromPrivateKey({ privateKey });
        // Build transaction
        const txn = yield client.transaction.build.simple({
            sender: account.accountAddress,
            data: payload,
        });
        if (!txn) {
            throw new Error("Failed to build transaction");
        }
        // Sign and submit transaction
        const committedTxn = yield client.signAndSubmitTransaction({
            signer: account,
            transaction: txn,
        });
        if (!(committedTxn === null || committedTxn === void 0 ? void 0 : committedTxn.hash)) {
            throw new Error("Transaction submission failed - no hash returned");
        }
        console.log("Transaction submitted:", committedTxn.hash);
        // Wait for transaction confirmation
        const executedTxn = yield client.waitForTransaction({
            transactionHash: committedTxn.hash,
        });
        if (!executedTxn) {
            throw new Error("Transaction execution failed - transaction not found");
        }
        console.log("Transaction executed successfully:", executedTxn);
        return committedTxn.hash;
    }
    catch (error) {
        console.error("Transaction failed:", error);
        // Re-throw the error so callers can handle it appropriately
        if (error instanceof Error) {
            throw error;
        }
        else {
            throw new Error(`Transaction failed: ${String(error)}`);
        }
    }
});
const readTransaction = (transactionId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const transaction = yield (client === null || client === void 0 ? void 0 : client.getTransactionByHash({
            transactionHash: transactionId
        }));
        return transaction;
    }
    catch (error) {
        throw new Error(`Failed to read transaction: ${error}`);
    }
});
export { AptosConnect, submitTnx, readTransaction };
