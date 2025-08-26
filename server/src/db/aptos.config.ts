import {
  Account,
  Aptos,
  AptosConfig,
  InputGenerateTransactionPayloadData,
  Network,
  Ed25519PrivateKey,
} from "@aptos-labs/ts-sdk";
import { BlockDataTS } from "../controler/vendore.controler.js";
import { HexString } from "aptos";

let client: Aptos | null = null;

const AptosConnect = async () => {
  //connect aptos blockchain
  try {
    const connectionInstance = new AptosConfig({ network: Network.DEVNET });
    client = new Aptos(connectionInstance);
    return client;
  } catch (error) {
    console.log(`There is a error while connecting to netwrk ${error}`);
  }
};

// Helper function to properly format private key hex string
// Helper function to properly format private key hex string
const formatPrivateKeyHex = (keyString: string): string => {
  let hex = keyString.trim();
  
  // Handle different private key formats
  if (hex.startsWith('ed25519-priv-0x')) {
    // Extract hex part from "ed25519-priv-0x..." format
    hex = hex.slice('ed25519-priv-0x'.length);
  } else if (hex.startsWith('0x')) {
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
  } else if (hex.length > 64) {
    throw new Error(`Private key too long: expected 64 characters, got ${hex.length}`);
  }
  
  return '0x' + hex;
};

const submitTnx = async (
  data: BlockDataTS,
  payload: InputGenerateTransactionPayloadData
): Promise<string> => {
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

    console.log("Account address:", account.accountAddress.toString());
    console.log("Payload:", JSON.stringify(payload, null, 2));

    // Build transaction
    const txn = await client.transaction.build.simple({
      sender: account.accountAddress,
      data: payload,
      options: {
        maxGasAmount: 200000,
        gasUnitPrice: 100,
      }
    });

    if (!txn) {
      throw new Error("Failed to build transaction");
    }

    console.log("Transaction built successfully");

    // Sign and submit transaction
    const committedTxn = await client.signAndSubmitTransaction({
      signer: account,
      transaction: txn,
    });

    if (!committedTxn?.hash) {
      throw new Error("Transaction submission failed - no hash returned");
    }

    console.log("Transaction submitted:", committedTxn.hash);

    // Wait for transaction confirmation with success check
    const executedTxn = await client.waitForTransaction({
      transactionHash: committedTxn.hash,
      options: {
        timeoutSecs: 30,
        checkSuccess: true,  // This will throw if transaction fails
      }
    });

    if (!executedTxn) {
      throw new Error("Transaction execution failed - transaction not found");
    }

    // Double check success (redundant with checkSuccess: true, but good practice)
    if (!executedTxn.success) {
      console.error("Transaction failed with VM status:", executedTxn.vm_status);
      console.error("Full transaction:", JSON.stringify(executedTxn, null, 2));
      throw new Error(`Transaction execution failed: ${executedTxn.vm_status}`);
    }

    console.log("Transaction executed successfully:", executedTxn.hash);
    console.log("Gas used:", executedTxn.gas_used);
    
    return committedTxn.hash;

  } catch (error) {
    console.error("Transaction failed:", error);
    
    // Enhanced error logging for debugging
    if (error instanceof Error) {
      console.error("Error message:", error.message);
      
      // Check if it's an Aptos transaction error with additional details
      if ('transaction' in error) {
        const txnError = error as any;
        if (txnError.transaction) {
          console.error("Failed transaction details:");
          console.error("- VM Status:", txnError.transaction.vm_status);
          console.error("- Gas used:", txnError.transaction.gas_used);
          console.error("- Success:", txnError.transaction.success);
          
          // Log the payload that failed
          if (txnError.transaction.payload) {
            console.error("- Failed payload:", JSON.stringify(txnError.transaction.payload, null, 2));
          }
        }
      }
    }
    
    // Re-throw the error so callers can handle it appropriately
    if (error instanceof Error) {
      throw error;
    } else {
      throw new Error(`Transaction failed: ${String(error)}`);
    }
  }
};
const readTransaction = async (transactionId: string) => {
  try {
    const transaction = await client?.getTransactionByHash({
      transactionHash: transactionId
    });

    return transaction;
  } catch (error) {
    throw new Error(`Failed to read transaction: ${error}`);
  }
};
export { AptosConnect, submitTnx,readTransaction };
