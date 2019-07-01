class WriterComponent {
    constructor({titleId, contentId, publishId, readOnly=false, poemId=null}) {
        this.title = document.getElementById(titleId);
        this.content = document.getElementById(contentId);
        // this.cancelBtn = document.getElementById(cancelId);
        this.publishBtn = document.getElementById(publishId);

        this.readOnly = readOnly;
        this.poemId = poemId;
        this.createTime = new Time({timestamp: new Date().getTime() / 1000});

        if (this.readOnly) {
            this.publishBtn.style.display = 'none';
            this.title.contentEditable = 'false';
            this.content.contentEditable = 'false';
            this.view();
        } else {
            this.publishBtn.style.display = 'inherit';
            this.title.contentEditable = 'true';
            this.content.contentEditable = 'true';
            this.title.innerText = this.createTime.yearToMinute + '的投明';
            this.publishBtn.addEventListener('click', this.publish.bind(this));
        }
    }

    view() {
        Request.get(`/api/poem/@${this.poemId}`)
            .then(resp => {
                this.title.innerText = resp.title;
                this.content.innerText = resp.content;
                this.createTime = new Time({timestamp: resp.create_time});
            });
    }

    publish() {
        if (this.readOnly) {
            return;
        }
        const title = this.title.innerText;
        const content = this.content.innerText;
        Request.post('/api/poem', {title: title, content: content})
            .then(resp => {
                this.title.innerText = '';
                this.content.innerText = '';
                window.location.href = '/';
            });
    }

    // sizeChanger() {
    //     console.log('changing');
    //     if (this.title.innerText.length <= 12) {
    //         this.title.style.fontSize = '30px';
    //     } else {
    //         this.title.style.fontSize = '20px';
    //     }
    // }
}
