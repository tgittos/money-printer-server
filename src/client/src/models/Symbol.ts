export interface ISymbol {
    symbol: string;
    open: number;
    openTime: number;
    change: number;
    changePercent: number;
    high: number;
    highTime: number;
    low: number;
    lowTime: number;
    close: number;
    closeTime: number;
    week52High: number;
    week52Low: number;
    ytdChange: number
    latestPrice: number;
    latestVolume: number;
    lastTime: string;
    latestUpdate: number;
    currency: string;
    date: Date | null;
}

class Symbol implements ISymbol {
    symbol: string;
    open: number;
    openTime: number;
    change: number;
    changePercent: number;
    high: number;
    highTime: number;
    low: number;
    lowTime: number;
    close: number;
    closeTime: number;
    week52High: number;
    week52Low: number;
    ytdChange: number
    latestPrice: number;
    latestVolume: number;
    lastTime: string;
    latestUpdate: number;
    currency: string;

    get date(): Date {
        return new Date(this.closeTime);
    }

    constructor(serverObj: ISymbol = {} as ISymbol) {
        this.symbol = serverObj.symbol;
        this.open = serverObj.open;
        this.openTime = serverObj.openTime;
        this.change = serverObj.change;
        this.changePercent = serverObj.changePercent;
        this.high = serverObj.high;
        this.highTime = serverObj.highTime;
        this.low = serverObj.low;
        this.lowTime = serverObj.lowTime;
        this.close = serverObj.close;
        this.closeTime = serverObj.closeTime;
        this.week52High = serverObj.week52High;
        this.week52Low = serverObj.week52Low;
        this.ytdChange = serverObj.ytdChange;
        this.latestPrice = serverObj.latestPrice;
        this.latestVolume = serverObj.latestVolume;
        this.lastTime = serverObj.lastTime;
        this.latestUpdate = serverObj.latestUpdate;
        this.currency = serverObj.currency;
    }
}

export default Symbol;


/*
[{"avgTotalVolume":56801147,"calculationPrice":"tops","change":0.45,"changePercent":0.001,"close":453,"closeSource":"cfiifloa","closeTime":1677009565081,"companyN
ame":"SSgA Active Trust - S&P 500 ETF TRUST ETF","currency":"USD","delayedPrice":458.75,"delayedPriceTime":1707985311828,"extendedChange":1.09,"extendedChangePercent":0.00247,"extendedPrice":458.07,"extendedPri
ceTime":1667961513624,"high":470.14,"highSource":"dep n tiieae5erydm lcu1","highTime":1643838965990,"iexAskPrice":456.85,"iexAskSize":204,"iexBidPrice":469.1,"iexBidSize":201,"iexClose":471.73,"iexCloseTime":16
38352419331,"iexLastUpdated":1703675117459,"iexMarketPercent":0.0186195307191649,"iexOpen":454.93,"iexOpenTime":1652600532346,"iexRealtimePrice":473.62,"iexRealtimeSize":72,"iexVolume":479842,"lastTradeTime":16
80350814917,"latestPrice":456.54,"latestSource":"IEX real time price","latestTime":"2:16:39 PM","latestUpdate":1703918836984,"latestVolume":27023323,"low":453,"lowSource":"amtceiX  EerlieIrp ","lowTime":1657802
055486,"marketCap":405551632399,"oddLotDelayedPrice":473.35,"oddLotDelayedPriceTime":1656549715606,"open":470.14,"openTime":1661080064367,"openSource":"olacfifi","peRatio":null,"previousClose":454,"previousVolu
me":49589465,"primaryExchange":"A ACNSEYR","symbol":"SPY","volume":25852979,"week52High":461.88,"week52Low":319.21,"ytdChange":0.22761261090752077}]

 */