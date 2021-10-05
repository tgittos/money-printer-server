import * as d3 from "d3";
import IAxis from "../../interfaces/IAxis";
import IChartDimensions from "../../interfaces/IChartDimensions";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";

export interface IAxisProps<T, U extends Date | number> {
    dimensions: IChartDimensions
    data: IFigureDataPoint[];
    mapper: (datum: IFigureDataPoint, idx: number, arr: Iterable<IFigureDataPoint>) => U;
    scale: (range: Iterable<U>) => d3.AxisScale<any>;
    axis: (scale: d3.AxisScale<d3.AxisDomain>) => d3.Axis<d3.AxisDomain>;
}

abstract class Axis<T, U extends Date | number> implements IAxis {
    readonly props: IAxisProps<T, U>;

    protected readonly _scale: d3.AxisScale<d3.AxisDomain>;
    protected readonly _axis: d3.Axis<d3.AxisDomain>;

    public get scale(): d3.AxisScale<d3.AxisDomain> {
        return this._scale;
    }

    public get domain(): d3.AxisDomain[] {
        return this._scale.domain();
    }

    public get axis(): d3.Axis<d3.AxisDomain> {
        return this._axis;
    }

    protected constructor(props: IAxisProps<T, U>) {
        this.props = props;

        let range: Iterable<U> = [];

        if (this.props.scale == d3.scaleTime) {
            const extent = d3.extent(props.data,
                (datum, idx, arr) =>
                    this.props.mapper(datum, idx, arr).toString());
            range = extent as Iterable<U>;
        } else {
            const extent = d3.extent(props.data,
                (datum, idx, arr) =>
                    this.props.mapper(datum, idx, arr) as number);
            range = d3.range(extent[0], extent[1]) as Iterable<U>;
        }

        this._scale = this.props.scale(range);
        this._axis = this.props.axis(this._scale);
    }

    abstract draw(svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>): void;
}

export default Axis;
