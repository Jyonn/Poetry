class WriterComponent {
    constructor({appNameId, titleId, contentId, publishId, createTimeId}) {
        this.appName = document.getElementById(appNameId);
        this.title = document.getElementById(titleId);
        this.content = document.getElementById(contentId);
        this.createTime = document.getElementById(createTimeId);

        this.publishBtn = document.getElementById(publishId);
        this.publishBtn.addEventListener('click', this.publish.bind(this));
    }

    read(poemId) {
        this.publishBtn.style.display = 'none';
        this.title.contentEditable = 'false';
        this.content.contentEditable = 'false';

        Request.get(`/api/poem/@${poemId}`)
            .then(resp => {
                this.title.innerText = resp.title;
                this.content.innerText = resp.content;
                this.createTime.innerText = new Time({timestamp: resp.create_time}).getDateTime('cn', true);
            });
    }

    write() {
        this.publishBtn.style.display = 'inherit';
        this.title.contentEditable = 'true';
        this.content.contentEditable = 'true';
        this.title.innerText = '';
        this.content.innerText = '';
        this.createTime.innerText = '';

        this.currentTime = new Time({timestamp: new Date().getTime() / 1000});
        this.title.setAttribute('placeholder', this.currentTime.getDateTime() + '的' + this.appName.innerText);
    }

    publish() {
        const title = this.title.innerText || this.title.getAttribute('placeholder');
        const content = this.content.innerText;
        console.log(content.length);
        if (content.length === 0) {
            alert('字数过少');
            return;
        }
        Request.post('/api/poem/', {title: title, content: content})
            .then(resp => {
                this.title.innerText = '';
                this.content.innerText = '';
                window.location.href = '/';
            });
    }
}
