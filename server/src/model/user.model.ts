import mongoose from "mongoose";
import { customAlphabet } from "nanoid";

// Generate a unique ID similar to the one in your Streamlit app
const nanoid = customAlphabet("0123456789", 12);

const birthRecordSchema = new mongoose.Schema({
  // --- Core Blockchain-Related Attributes ---
  uniqueID: {
    type: String,
    index: true,
    unique: true,
    default: () =>nanoid(),
  },
  walletId: {
    type: String,
    required: true,
    unique: true, // Wallet IDs should also be unique
  },
  privateKey: {
    type: String,
    required: true,
  },
  transId: [
    {
      type: String,
    },
  ],
  
  // --- Birth Registration Attributes from Streamlit ---
  babyName: {
    type: String,
    required: true,
  },
  gender: {
    type: String,
    required: true,
  },
  birthDate: {
    type: Date, // Use Date type for better date handling
    required: true,
  },
  timeOfBirth: {
    type: String,
    required: true,
  },
  placeOfBirth: {
    type: String,
    required: true,
  },
  fatherName: {
    type: String,
    required: true,
  },
  fatherId: {
    type: String,
    required: true,
  },
  fatherContact: {
    type: String,
    required: true,
  },
  fatherEmail: {
    type: String,
    required: true,
  },
  motherName: {
    type: String,
    required: true,
  },
  motherId: {
    type: String,
    required: true,
  },
  motherContact: {
    type: String,
    required: true,
  },
  motherEmail: {
    type: String,
    required: true,
  },
  address: {
    type: String,
    required: true,
  },
  city: {
    type: String,
    required: true,
  },
  state: {
    type: String,
    required: true,
  },
  country: {
    type: String,
    required: true,
    default: "India",
  },
  
}, {
  timestamps: true, // Automatically adds createdAt and updatedAt fields
});

const BirthRecord = mongoose.model("BirthRecord", birthRecordSchema);

export default BirthRecord;