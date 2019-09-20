class IndexComponent {
    constructor({indexBoxId, poemCountId, avatarId}) {
        this.indexBox = document.getElementById(indexBoxId);
        this.poemCount = document.getElementById(poemCountId);
        this.avatar = document.getElementById(avatarId);

        this.loadData();
        this.indexBox.addEventListener('scroll', this.scrollListener.bind(this));
    }

    loadData() {
        this.indexBox.innerHTML = '';
        this.pager = new Pager({count: 10, api: '/api/poem/'});
        this.pager.next(this.display.bind(this));
        Request.get('/api/user/')
            .then(resp => {
                this.avatar.style.backgroundImage = `url('${resp.avatar}')`;
            });
    }

    reloadData() {
        this.loadData();
    }

    display(resp) {
        if (this.pager.last === null) {
            this.indexBox.removeEventListener('scroll', this.scrollListener.bind(this));
        }
        this.poemCount.innerText = resp.total_count;

        let poemList = resp.object_list;
        let indexItemTemplate = template`
        <div class="index-box__item-box" onclick="writerComponent.read('${2}'); pageArranger.writer();">
            <div class="index-box__title">${0}</div>
            <div class="index-box__time">${1}</div>
        </div>`;

        for (let poem of poemList) {
            let html = stringToHtml(indexItemTemplate(
                poem.title,
                new Time({timestamp: poem.create_time}).relative,
                poem.id,
            ));
            this.indexBox.appendChild(html);
        }
    }

    scrollListener() {
        if (this.indexBox.scrollHeight - this.indexBox.clientHeight - this.indexBox.scrollTop < 55 * 5) {
            this.pager.next(this.display.bind(this));
        }
    }
}
