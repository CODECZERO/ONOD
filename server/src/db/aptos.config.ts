import{Aptos,AptosConfig,Network} from "@aptos-labs/ts-sdk";

let client:Aptos|null=null;

const AptosConnect=async()=>{
  //connect aptos blockchain
  try {
    const connectionInstance=new AptosConfig({network:Network.TESTNET});
    client=new Aptos(connectionInstance);
    return client;
  } catch (error){
    console.log(`There is a error while connecting to netwrk ${error}`);
  }  
}


export {
  AptosConnect

}

