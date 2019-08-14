class DayNight {
    constructor({appNameId, footTextId}) {
        this.body = document.body;
        this.appName = document.getElementById(appNameId) | document.createElement('div');
        this.footText = document.getElementById(footTextId) | document.createElement('div');
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
        this.appName.innerText = '投明';
        this.footText.innerText = '暗';
        Store.save('dayNight', 'day');
    }

    night() {
        this.body.classList.remove('day');
        this.body.classList.add('night');
        this.is_day = false;
        this.appName.innerText = '投暗';
        this.footText.innerText = '明';
        Store.save('dayNight', 'night');
    }
}