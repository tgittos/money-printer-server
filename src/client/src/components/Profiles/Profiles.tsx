import React from 'react';
import styles from './Profiles.module.scss';
import {Col, Nav, Row, Tab} from "react-bootstrap";
import ProfileDetails from "../ProfileDetails/ProfileDetails";
import Accounts from "../Accounts/Accounts";
import Notifications from "../Notifications/Notifications";
import {IProfile} from "../../models/Profile";
import AccountRepository from "../../repositories/AccountRepository";
import Account from "../../models/Account";

interface IProfilesProps {
    profile: IProfile
}

interface IProfilesState {
    profile: IProfile,
    accounts: Account[]
}

class Profiles extends React.Component<IProfilesProps, IProfilesState> {

    private accountRepository: AccountRepository;

    constructor(props: IProfilesProps) {
        super(props);

        this.state = {
            profile: props.profile,
            accounts: []
        }

        this._onAccountListUpdated = this._onAccountListUpdated.bind(this);

        this.accountRepository = new AccountRepository();
    }

    componentDidMount() {
        this.accountRepository.listAccounts().then(this._onAccountListUpdated);
    }

    private _onAccountListUpdated(accounts: Account[]) {
        if (accounts) {
            this.setState(prev => ({
                ...prev,
                accounts: accounts
            }));
        }
    }

    render() {
        return <div className={styles.Profiles}>
            <Tab.Container id="profiles" defaultActiveKey="first">
                <Row>
                    <Col sm={4}>
                        <Nav className="flex-column">
                            <Nav.Item>
                                <Nav.Link eventKey="first">Personal Details</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="second">Accounts</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="third">Notifications</Nav.Link>
                            </Nav.Item>
                        </Nav>
                    </Col>
                    <Col sm={8}>
                        <Tab.Content>
                            <Tab.Pane eventKey="first">
                                <ProfileDetails profile={this.props.profile}></ProfileDetails>
                            </Tab.Pane>
                            <Tab.Pane eventKey="second">
                                <Accounts accounts={this.state.accounts}></Accounts>
                            </Tab.Pane>
                            <Tab.Pane eventKey="third">
                                <Notifications></Notifications>
                            </Tab.Pane>
                        </Tab.Content>
                    </Col>
                </Row>
            </Tab.Container>
        </div>
    }
}

export default Profiles;
