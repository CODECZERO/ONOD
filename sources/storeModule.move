module 0x6b7bf296ecb04c37b5ac861ef63ca74cca1dda1694778fb29677c56de5202995::storeModule {
    use std::string;
    use std::vector;
    use std::signer;

    struct Document has key {
        issuer: address,
        receiver: address,
        doc_type: string::String,
        doc_id: string::String,
        metadata: string::String,
        previous_versions: vector<string::String>,
        issued_at: u64,
    }

    public entry fun store_document(
        signer: &signer,
        receiver: address,
        doc_type: string::String,
        doc_id: string::String,
        metadata: string::String,
        previous_versions: vector<string::String>,
        issued_at: u64
    ) {
        let doc = Document {
            issuer: signer::address_of(signer),
            receiver,
            doc_type,
            doc_id,
            metadata,
            previous_versions,
            issued_at,
        };
        move_to(signer, doc);
    }
}
