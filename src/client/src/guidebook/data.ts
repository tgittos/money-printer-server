import ICandleDataPoint from "../src/components/Charts/interfaces/ICandleDataPoint";
import moment from "moment";
import ILineDataPoint from "../src/components/Charts/interfaces/ILineDataPoint";

type Generator = () => number;

interface IGenDataOpts<T> {
    n: number;
    pct1: number;
    pct2: number;
    propertySelector: (obj: T) => number;
    pointConstructor: (d: Date, g: Generator) => T;
    gaps: boolean;
}

function genData<T>(seed: T, opts: IGenDataOpts<T> = {
        n: 500,
    } as IGenDataOpts<T>): T[] {
    const fakeData: T[] = [seed];
    const { n, propertySelector, pointConstructor, gaps } = opts;

    const pct1 = opts.pct1 ?? 0.05;
    const pct2 = opts.pct2 ?? 1.1;

    function next(): number {
        const lastDataPoint = fakeData[fakeData.length-1];
        const lastVal = propertySelector(lastDataPoint);
        let nextVal = lastVal;
        const pct = (1.0 + Math.random() * pct2) * pct1;
        const selector = Math.random() * 3;
        if (selector > 2) {
            nextVal = lastVal + lastVal * pct;
        } else if (selector > 1) {
            nextVal = lastVal - lastVal * pct;
        }
        return nextVal;
    }

    for (let i = opts.n-1; i > 0; i--) {
        const d = moment().subtract(i, 'days').toDate();
        fakeData.push(pointConstructor(d, next));
    }

    if (gaps) {
        // randomly nuke some data points
        for (let i = 0; i < n; i++){
            if (Math.random() * 20 < 1) {
                fakeData[i] = undefined;
            }
        }
    }

    return fakeData;
}

export const lineGenerator = (n: number = 500, gaps = false) => genData<ILineDataPoint>({
    x: moment.utc().subtract(n, 'days').toDate(),
    y: Math.random() * 5000
} as ILineDataPoint, {
    n,
    gaps,
    propertySelector: p => p.y,
    pointConstructor: (d, next) => ({
            x: d,
            y: next()
        } as ILineDataPoint),
} as IGenDataOpts<ILineDataPoint>);

export const candleGenerator = (n: number = 500, gaps = false) => {
    const v = Math.random() * 5000;
    return genData<ICandleDataPoint>({
        x: moment.utc().subtract(n, 'days').toDate(),
        open: v,
        close: v,
        high: v,
        low: v
    }, {
        n,
        gaps,
        propertySelector: p => p.close,
        pointConstructor: (d, next) => ({
            x: d,
            open: next(),
            close: next(),
            high: next(),
            low: next()
        } as ICandleDataPoint)
    } as IGenDataOpts<ICandleDataPoint>)
};