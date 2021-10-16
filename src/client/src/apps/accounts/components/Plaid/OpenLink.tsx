import React, {FunctionComponent, useEffect, useCallback} from "react";
import {
    usePlaidLink,
    PlaidLinkOptions,
    PlaidLinkOnSuccess,
    PlaidLinkOnExit,
    PlaidLinkError
} from "react-plaid-link";
import Env from '../../../../env';
import PlaidService from "../../../../services/PlaidService";

export interface IOpenLinkProps {
    token: string;
}

const OpenLink: FunctionComponent<IOpenLinkProps> = ({ token }) => {
    const plaidService = new PlaidService();

    const onSuccess = useCallback<PlaidLinkOnSuccess>(
        async (public_token: string, metadata: any) => {
        const result = await plaidService.setAccessToken(public_token);
        localStorage.removeItem('link_token');
    }, []);

    const onExit = useCallback<PlaidLinkOnExit>(
    (error: PlaidLinkError) => {
        if (error) {
            console.log(' * OpenLink::onExit - got error:', error);
        }
        localStorage.removeItem('link_token');
    }, []);

    let isOauth = false;

    const config: Parameters<typeof usePlaidLink>[0] = {
        token: token!,
        onSuccess,
        onExit
    };

    if (window.location.href.includes("?oauth_state_id=")) {
        // TODO: figure out how to delete this ts-ignore
        // @ts-ignore
        config.receivedRedirectUri = window.location.href;
        isOauth = true;
    }

    const { open, ready, error } = usePlaidLink(config);

    useEffect(() => {
        if (!ready) {
            return;
        }
        if (Env.DEBUG) {
            console.log('OpenLink::useEffect - attempting to open PlaidLink with config:', config);
        }
        open();
    }, [ready, open]);

    return <></>;
}

export default OpenLink;