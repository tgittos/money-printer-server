export interface IPlaidInfo {
   access_token: string;
   item_item: string;
   products: string[];
}

interface IPlaidGetInfoResponse {
   success: boolean;
   data: IPlaidInfo;
}

export default IPlaidGetInfoResponse;