import styles from "./Forecasting.module.scss";
import React from "react";

export interface IForecastingProps {

}

export interface IForecastingState {

}

class Forecasting extends React.Component<IForecastingProps, IForecastingState> {
    render() {
        return <div className={styles.Forecasting}>
            Forecasting component
        </div>
    }
}

export default Forecasting;
