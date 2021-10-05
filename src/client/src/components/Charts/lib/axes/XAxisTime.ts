import XAxis, {IXAxisProps} from "./XAxis";
import IFigureDataPoint from "../../interfaces/IFigureDataPoint";
import * as d3 from "d3";

class XAxisTime extends XAxis<Date> {
    constructor(props: IXAxisProps<IFigureDataPoint, Date>) {
        super(props);

        const extent = d3.extent(props.data,
            (datum, idx, arr) =>
                this.props.mapper(datum, idx, arr) as Date);
        const s = this.props.scale as d3.ScaleTime<IFigureDataPoint, Date>;
        this._scale = s<IFigureDataPoint, Date>(extent[0], extent[1]);
        this._axis = this.props.axis(this._scale);
    }
}

export default XAxisTime