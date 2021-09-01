import BaseRepository from "./BaseRepository";

class SymbolRepository extends BaseRepository {
    constructor() {
        super();

        this.apiEndpoint = "symbols/"
    }
}