import React, { useEffect, useContext } from "react";
import { usePlaidLink } from "react-plaid-link";
import Button from "plaid-threads/Button";

import Context from "../../Context";
import PlaidRepository from "../../../repositories/PlaidRepository";
import AppStore from "../../../stores/AppStore";
import {addAccount, setAccounts} from "../../../slices/AccountSlice";

const Link = () => {
  const plaidRepository = new PlaidRepository();
  const { linkToken } = AppStore.getState().plaid;

  const onSuccess = async (public_token: string) => {
    // send public_token to server
    const response = await plaidRepository.setAccessToken(public_token);
    if (!response.success) {
      // let the plaid app know that we failed to set an access token
      return;
    }
    AppStore.dispatch(addAccount(response.data));
  };

  let isOauth = false;
  const config: Parameters<typeof usePlaidLink>[0] = {
    token: linkToken!,
    onSuccess,
  };

  if (window.location.href.includes("?oauth_state_id=")) {
    // TODO: figure out how to delete this ts-ignore
    // @ts-ignore
    config.receivedRedirectUri = window.location.href;
    isOauth = true;
  }

  const { open, ready } = usePlaidLink(config);

  useEffect(() => {
    if (isOauth && ready) {
      open();
    }
  }, [ready, open, isOauth]);

  return (
    <Button type="button" large onClick={() => open()} disabled={!ready}>
      Launch Link
    </Button>
  );
};

Link.displayName = "Link";

export default Link;
