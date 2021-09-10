export const SortAscending = (s1: ISymbol, s2: ISymbol) => {
    return s1.date < s2.date
        ? -1
        : s2.date < s1.date
            ? 1
            : 0;
}

export const SortDescending = (s1: ISymbol, s2: ISymbol) => {
    return s2.date < s1.date
        ? -1
        : s1.date < s2.date
            ? 1
            : 0;
}

interface ISymbol {
    symbol: string;
    open: number;
    high: number;
    low: number;
    close: number;
    date: Date;
}

export default ISymbol;
