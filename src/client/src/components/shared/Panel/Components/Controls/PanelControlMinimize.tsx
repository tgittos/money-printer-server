import React from "react";
import IconButton from "../../../Button/IconButton";
import {VscChromeMinimize} from "react-icons/all";

class PanelControlMinimize extends React.Component<any, any> {
    render() {
        return <IconButton icon={VscChromeMinimize} />;
    }
}

export default PanelControlMinimize;
