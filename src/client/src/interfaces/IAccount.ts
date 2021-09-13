interface IAccount {
    /*
    id = Column(Integer, primary_key=True)
    plaid_item_id = Column(Integer, ForeignKey("plaid_items.id"), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    account_id = Column(String(32))
    name = Column(String(32))
    official_name = Column(String(64))
    subtype = Column(String(32))
    timestamp = Column(DateTime)
    */

   id: number;
   name: string;
   subtype: string;
   timestamp: Date;
}

export default IAccount;
