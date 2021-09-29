import React from "react";

const styles = {
    ColorChip: {
        backgroundColor: '#fff',
        display: 'inline-block',
        width: '150px',
        height: '80px'
    }
}

const ColorChip = props => {
    styles.ColorChip.backgroundColor = this.props.value;
    return <div>
        <div className={styles.ColorChip}>
            { this.props.value }
        </div>
        <span>{ this.props.name }</span>
    </div>
};

export default ColorChip;
