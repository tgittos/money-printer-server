import PlaidGetInfoResponse from "../responses/PlaidGetInfoResponse";
import PlaidCreateLinkTokenResponse from "../responses/PlaidCreateLinkTokenRequest";
import PlaidSetAccessTokenResponse from "../responses/PlaidSetAccessTokenResponse";
import PlaidSetAccessTokenRequest from "../requests/PlaidSetAccessTokenRequest";
import HttpService from "./HttpService";
import {AppDispatch} from "../store/AppStore";
import {AddAccounts} from "../store/actions/AccountActions";

class PlaidService {

    readonly http: HttpService;

    private get endpoint(): string {
        return this.http.baseApiEndpoint + "/oauth/";
    }

    constructor() {
        this.http = new HttpService();
    }

    /*
     * Get the Plaid key information from the server?
     */
    public async getInfoFromServer(): Promise<PlaidGetInfoResponse> {
        const response = await this.http.authenticatedRequest<null, PlaidGetInfoResponse>({
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
        const response = await this.http.authenticatedRequest<null, PlaidCreateLinkTokenResponse>({
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
        const response = await this.http.authenticatedRequest<PlaidSetAccessTokenRequest, PlaidSetAccessTokenResponse>({
            url: this.endpoint + "set_access_token",
            method: "POST",
            data: {
                public_token: publicToken,
            }
        }).then(response => (response as any).data as PlaidSetAccessTokenResponse);

        if (response.success) {
            // this.dispatch(AddAccounts([response.data]));
        }

        return response;
    }

}

export default PlaidService;