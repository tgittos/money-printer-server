import React from 'react';
import styles from './Profiles.module.scss';
import {Col, Nav, Row, Tab} from "react-bootstrap";
import ProfileDetails from "../ProfileDetails/ProfileDetails";
import Accounts from "../Accounts/Accounts";
import Notifications from "../Notifications/Notifications";
import {IProfile} from "../../models/Profile";

interface IProfilesProps {
    profile: IProfile
}

interface IProfilesState {
    profile: IProfile
}

class Profiles extends React.Component<IProfilesProps, IProfilesState> {

    constructor(props: IProfilesProps) {
        super(props);

        this.state = {
            profile: props.profile
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
                                <Accounts></Accounts>
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
