import BaseRepository from "./BaseRepository";
import AppStore from '../stores/AppStore';
import {setLinkToken} from "../slices/PlaidSlice";
import PlaidSetAccessTokenRequest from "../requests/PlaidSetAccessTokenRequest";
import PlaidSetAccessTokenResponse from "../responses/PlaidSetAccessTokenResponse";
import PlaidCreateLinkTokenResponse from "../responses/PlaidCreateLinkTokenRequest";
import PlaidGetInfoResponse from "../responses/PlaidGetInfoResponse";
import {addAccount, setAccounts} from "../slices/AccountSlice";
import Account from "../models/Account";

class PlaidRepository extends BaseRepository {

    constructor() {
        super();

        this.apiEndpoint = "plaid/";
    }

    /*
     * Get the Plaid key information from the server?
     */
    public async getInfoFromServer(): Promise<PlaidGetInfoResponse> {
        const response = await this.authenticatedRequest<null, PlaidGetInfoResponse>({
            url: this.endpoint + "info",
            method: "POST"
        }).then(response => (response as any).data as PlaidGetInfoResponse);
        return response;
    }

    /*
     * User wants to use Plaid to link a financial account, this will create a token for them
     * to use in their authorization flow
     */
    public async createLinkToken(): Promise<PlaidCreateLinkTokenResponse> {
        const response = await this.authenticatedRequest<null, PlaidCreateLinkTokenResponse>({
            url: this.endpoint + "create_link_token",
            method: "POST"
        }).then(response => (response as any).data as PlaidCreateLinkTokenResponse);

        return response;
    }

    /*
     * Plaid has given us access to the user's account, use the API server to exchange a public
     * token for a private token - the server stores the private token and returns a ref to a
     * Money Printer Account object
     */
    public async setAccessToken(publicToken: string): Promise<PlaidSetAccessTokenResponse> {
        const response = await this.authenticatedRequest<PlaidSetAccessTokenRequest, PlaidSetAccessTokenResponse>({
            url: this.endpoint + "set_access_token",
            method: "POST",
            data: {
                public_token: publicToken,
            }
        }).then(response => (response as any).data as PlaidSetAccessTokenResponse);

        if (response.success) {
            AppStore.dispatch(addAccount(new Account(response.data)));
        }

        return response;
    }
}

export default PlaidRepository;
