class Time {
    constructor({timestamp}) {
        this.time = new Date(timestamp * 1000);
    }

    static addZero(number) {
        if (number < 10) {
            return `0${number}`;
        } else {
            return `${number}`;
        }
    }

    getTwelveTime() {
        let hours = this.time.getHours();
        let twelveHours = (hours < 12) ? hours : hours - 12;
        if (twelveHours === 0) {
            twelveHours = 12;
        }
        return `${hours < 12 ? '上午' : '下午'}${twelveHours}:${Time.addZero(this.time.getMinutes())}`
    }

    getDate(format='cn', withYear=false) {
        let dateStr;
        if (format === 'cn') {
            dateStr = `${this.time.getMonth() + 1}月${this.time.getDate()}日`
        } else {
            dateStr = `${this.time.getMonth() + 1}/${this.time.getDate()}`
        }
        if (withYear) {
            dateStr = `${this.time.getFullYear()}` + '/年'[format==='cn'] + dateStr;
        }
        return dateStr;
    }

    getTime(format='cn', withMinute=true) {
        if (format === 'cn') {
            if (withMinute) {
                return `${this.time.getHours()}时${Time.addZero(this.time.getMinutes())}分`
            } else {
                return `${this.time.getHours()}时`
            }
        } else {
            return `${this.time.getHours()}:${Time.addZero(this.time.getMinutes())}`
        }
    }

    getDateTime(format='cn', withYear=false, withMinute) {
        return `${this.getDate(format, withYear)} ${this.getTime(format, withMinute)}`;
    }

    get relative() {
        let current = new Date();
        let zero = new Date();
        zero.setHours(0, 0, 0, 0);

        let year = new Date();
        year.setHours(0, 0, 0, 0);
        year.setMonth(0, 1);

        let delta = (current.getTime() - this.time.getTime()) / 1000;
        let zeroDelta = (zero.getTime() - this.time.getTime()) / 1000;
        let yearDelta = (year.getTime() - this.time.getTime()) / 1000;

        if (zeroDelta <= 0) {
            if (delta < 60) {
                return '刚刚'
            } else if (delta < 60 * 60) {
                return `${Math.floor(delta / 60)}分钟前`;
            } else {
                return `${this.getTwelveTime()}`;
            }
        } else if (zeroDelta < 60 * 60 * 24) {
            return `昨天${this.getTwelveTime()}`;
        } else {
            return `${this.getDate('cn', yearDelta > 0)}`;
        }
    }
}