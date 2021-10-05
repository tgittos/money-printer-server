import XAxis, {IXAxisProps} from "./XAxis";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";
import * as d3 from "d3";

class XAxisNumeric extends XAxis<number> {
    constructor(props: IXAxisProps<IFigureDataPoint, number>) {
        super(props);

        const extent = d3.extent(props.data,
            (datum, idx, arr) =>
                this.props.mapper(datum, idx, arr) as number);
        const range = d3.range(extent[0], extent[1]) as Iterable<U>;
        this._scale = this.props.scale(range);
        this._axis = this.props.axis(this._scale);
    }
}

export default XAxisNumeric;