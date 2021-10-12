import React from "react";

const styles = {
    ColorChip: {
        width: '150px',
        height: '80px',
        margin: '2px',
        padding: '5px'
    },
    ChipName: {
        display: 'inline-block',
        width: '100%',
        textAlign: "center" as const
    }
}

class ColorChip extends React.Component<{ name: string, value: string },{}> {
    render() {
        const s = Object.assign({}, styles.ColorChip, {
            background: this.props.value
        });
        return <div style={{display: 'inline-block'}}>
            <div style={s}>
                {this.props.value}
            </div>
            <span style={styles.ChipName}>{this.props.name}</span>
        </div>
    }
};

export default ColorChip;
