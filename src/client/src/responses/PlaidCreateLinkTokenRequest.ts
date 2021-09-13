export interface IPlaidLinkToken {
    request_id: string,
    link_token: string,
    expiration: Date
}

interface IPlaidCreateLinkTokenResponse {
    success: boolean;
    data: IPlaidLinkToken;
}

export default IPlaidCreateLinkTokenResponse
