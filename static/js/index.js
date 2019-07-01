class Pager {
    constructor({count, api, last=0}) {
        this.count = count;
        this.last = last;
        this.api = api;
    }

    next(callback) {
        Request.get(this.api, {count: this.count, last: this.last})
            .then(resp => {
                this.last = resp.next_value;
                callback(resp.object_list);
            });
    }
}
class IndexComponent {
    constructor({indexBoxId}) {
        this.indexBox = document.getElementById(indexBoxId);
        this.indexBox.innerHTML = '';

        this.pager = new Pager({count: 10, api: '/api/poem'});
        this.pager.next(this.display.bind(this));
    }

    display(poemList) {
        let indexItemTemplate = template`
        <a href="${2}">
            <div class="index-box__item-box">
                <div class="index-box__title">${0}</div>
                <div class="index-box__time">${1}</div>
            </div>
        </a>`;

        for (let poem of poemList) {
            let html = stringToHtml(indexItemTemplate(
                poem.title,
                new Time({timestamp: poem.create_time}).relative,
                `/writer/@${poem.id}`,
            ));
            this.indexBox.appendChild(html);
        }
    }
}