import React, { useEffect, useContext, useCallback } from "react";

import Header from "./Headers";
import Products from "./ProductTypes/Products";
import Items from "./ProductTypes/Items";
import Context from "./../Context";

import styles from "./PlaidApp.module.scss";
import Env from "../../env";
import PlaidRepository from "../../repositories/PlaidRepository";
import Link from "./Link";

export interface IPlaidAppProps {

};

export interface IPlaidAppState {
  linkSuccess: boolean;
  isItemAccess: boolean;
  linkToken: string | null;
  accessToken: string | null;
  itemId: string | null;
  isError: boolean;
  backend: boolean;
  products: string[];
  linkTokenError: {
    error_message: string;
    error_code: string;
    error_type: string;
  };

};

class PlaidApp extends React.Component<IPlaidAppProps, IPlaidAppState> {

  private plaidRepo: PlaidRepository;

  constructor(props: IPlaidAppProps) {
    super(props);

    this.state = {
      linkSuccess: false,
      isItemAccess: true,
      linkToken: "", // Don't set to null or error message will show up briefly when site loads
      accessToken: null,
      itemId: null,
      isError: false,
      backend: true,
      products: ["transactions"],
      linkTokenError: {
        error_type: "",
        error_code: "",
        error_message: "",
      },
    };

    this.plaidRepo = new PlaidRepository();

    this.init();
  }

  private async init() {
    const { paymentInitiation } = await this.getInfo(); // used to determine which path to take when generating token
    // do not generate a new token for OAuth redirect; instead
    // setLinkToken from localStorage
    if (window.location.href.includes("?oauth_state_id=")) {
      this.setState(prev => ({
        ...prev,
        linkToken: localStorage.getItem("link_token")
      }));
    }
    await this.generateToken(paymentInitiation);
  };

  private async getInfo(): any {
      const response = await this.plaidRepo.getInfoFromServer();
      if (!response.ok) {
        this.setState(prev => ({
          ...prev,
          backend: false
        }));
        return { paymentInitiation: false };
      }
      const data = await response;
      const paymentInitiation: boolean = data.products.includes(
          "payment_initiation"
      );
      this.setState(prev => ({
        ...prev,
        products: data.products,
      }))
      return { paymentInitiation };
  }

  private async generateToken(paymentInitiation) {
      const response = await this.plaidRepo.createLinkToken();
      console.log('got response:', response);
      if (!response) {
        this.setState(prev => ({
          ...prev,
          linkToken: null
        }));
        return;
      }

      this.setState(prev => ({
        ...prev,
        linkToken: response.link_token
      }));

      localStorage.setItem("link_token", response.link_token); //to use later for Oauth
  }

  render() {
    console.log('this.state:', this.state);
    return <div>
      <div className={styles.container}>
        <Link />
        {this.state.linkSuccess && this.state.isItemAccess && (
            <>
              <Products />
              <Items />
            </>
        )}
      </div>
    </div>
  }
}

export default PlaidApp;
