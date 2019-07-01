class Pager {
    constructor({count, api, last=0}) {
        this.count = count;
        this.last = last;
        this.api = api;
        this.fetching = false;
    }

    next(callback) {
        if (this.last === null || this.fetching) {
            return;
        }
        this.fetching = true;
        Request.get(this.api, {count: this.count, last: this.last})
            .then(resp => {
                this.last = resp.next_value;
                this.fetching = false;
                callback(resp);
            })
            .catch(() => {
                this.fetching = false;
            })
    }
}