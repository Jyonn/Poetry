class DayNight {
    constructor({appNameId, footTextId}) {
        this.body = document.body;
        this.appName = document.getElementById(appNameId);
        this.footText = document.getElementById(footTextId);
        this.is_day = true;

        if (Store.load('dayNight') === 'night') {
            this.night();
        }
    }

    toggle() {
        if (this.is_day) {
            this.night();
        } else {
            this.day();
        }
    }

    day() {
        this.body.classList.remove('night');
        this.body.classList.add('day');
        this.is_day = true;
        if (this.appName) {
            this.appName.innerText = '投明';
        }
        if (this.footText) {
            this.footText.innerText = '暗';
        }
        Store.save('dayNight', 'day');
    }

    night() {
        this.body.classList.remove('day');
        this.body.classList.add('night');
        this.is_day = false;
        if (this.appName) {
            this.appName.innerText = '投暗';
        }
        if (this.footText) {
            this.footText.innerText = '明';
        }
        Store.save('dayNight', 'night');
    }
}