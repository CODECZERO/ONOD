module 0xa0d9331d0634419f53581c11c9d8ff6c8c57457f57d7911df07eb9b57afebe7a::storeModule {
    use std::string;
    use std::signer;
    use aptos_std::table_with_length;

    struct Document has store, drop, copy, key {
        issuer: address,
        receiver: address,
        doc_type: string::String,
        doc_id: string::String,
        metadata: string::String,
        previous_versions: vector<string::String>,
        issued_at: u64,
    }

    struct Store has key {
        documents: table_with_length::TableWithLength<string::String, Document>,
    }

    public entry fun init_store(account: &signer) {
        move_to(account, Store {
            documents: table_with_length::new(),
        });
    }

    public entry fun store_document(
        account: &signer,
        receiver: address,
        doc_type: string::String,
        doc_id: string::String,
        metadata: string::String,
        previous_versions: vector<string::String>,
        issued_at: u64
    ) acquires Store {
        let store = borrow_global_mut<Store>(signer::address_of(account));
        
        // Check if document exists and remove old version
        if (table_with_length::contains(&store.documents, doc_id)) {
            let _old_doc = table_with_length::remove(&mut store.documents, doc_id);
            // Old document is automatically dropped
        };

        let doc = Document {
            issuer: signer::address_of(account),
            receiver,
            doc_type,
            doc_id,
            metadata,
            previous_versions,
            issued_at,
        };
        
        table_with_length::add(&mut store.documents, doc_id, doc);
    }

    public fun get_document(owner: address, doc_id: string::String): Document acquires Store {
        let store = borrow_global<Store>(owner);
        *table_with_length::borrow(&store.documents, doc_id)
    }

    public fun has_document(owner: address, doc_id: string::String): bool acquires Store {
        let store = borrow_global<Store>(owner);
        table_with_length::contains(&store.documents, doc_id)
    }
}