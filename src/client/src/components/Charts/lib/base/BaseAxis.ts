import * as d3 from "d3";
import IAxisProps from "../../interfaces/IAxisProps";
import {Axis, ScaleLinear} from "d3";

abstract class BaseAxis {

    protected _props: IAxisProps;
    protected _scale: ScaleLinear<any, any>;
    protected _axis: Axis<any>;

    public get scaleLinear(): ScaleLinear<any, any> {
        return this._scale;
    }
    public get axis(): Axis<any> {
        return this._axis;
    }

    protected constructor(props: IAxisProps) {
        this._props = props;

        this.createScale();
        this.createAxis();
    }

    protected abstract createScale();

    protected abstract createAxis();

    public abstract draw(svg: d3.Selection<SVGGElement, unknown, null, undefined>);
}

export default BaseAxis;
