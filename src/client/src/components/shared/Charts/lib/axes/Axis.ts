import * as d3 from "d3";
import IChartDimensions from "../../interfaces/IChartDimensions";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";

export interface IAxis {
    scale: d3.AxisScale<any>;
    domain?: d3.AxisDomain[];
    draw: (svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>) => void;
}

export interface IAxisProps<T, U extends Date | number> {
    dimensions: IChartDimensions;
    data: IFigureDataPoint[];
    mapper?: (datum: IFigureDataPoint, idx: number, arr: Iterable<IFigureDataPoint>) => U;
    scale: d3.AxisScale<any>;
    axis: (scale: d3.AxisScale<d3.AxisDomain>) => d3.Axis<d3.AxisDomain>;
}


abstract class Axis<T, U extends Date | number> implements IAxis {
    protected readonly props: IAxisProps<T, U>;

    protected _scale: d3.AxisScale<any>
    protected _axis: d3.Axis<d3.AxisDomain>;

    public get scale(): d3.AxisScale<any> {
        return this._scale;
    }

    public get domain(): d3.AxisDomain[] {
        return this._scale.domain();
    }

    protected constructor(props: IAxisProps<T, U>) {
        this.props = props
    }

    abstract draw(svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>): void;
}

export default Axis;
