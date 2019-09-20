class WriterComponent {
    constructor({appNameId, titleId, contentId, publishId, createTimeId, editId}) {
        this.appName = document.getElementById(appNameId);
        this.title = document.getElementById(titleId);
        this.content = document.getElementById(contentId);
        this.createTime = document.getElementById(createTimeId);

        this.publishBtn = document.getElementById(publishId);
        this.publishBtn.addEventListener('click', this.publish.bind(this));
        this.editBtn = document.getElementById(editId);
        this.editBtn.addEventListener('click', this.edit.bind(this));

        this.poemId = null;
    }

    readUIPrep() {
        this.editBtn.style.display = 'inherit';
        this.publishBtn.style.display = 'none';
        this.title.contentEditable = 'false';
        this.content.contentEditable = 'false';
    }

    editUIPrep() {
        this.editBtn.style.display = 'none';
        this.publishBtn.style.display = 'inherit';
        this.title.contentEditable = 'true';
        this.content.contentEditable = 'true';
    }

    read(poemId) {
        this.poemId = poemId;
        this.readUIPrep();

        Request.get(`/api/poem/@${this.poemId}`)
            .then(resp => {
                this.title.innerText = resp.title;
                this.content.innerText = resp.content;
                this.createTime.innerText = new Time({timestamp: resp.create_time}).getDateTime('cn', true);
            });
    }

    edit() {
        this.editUIPrep();
    }

    write() {
        this.poemId = null;
        this.editUIPrep();
        this.title.innerText = '';
        this.content.innerText = '';
        this.createTime.innerText = '';

        this.currentTime = new Time({timestamp: new Date().getTime() / 1000});
        this.title.setAttribute('placeholder', this.currentTime.getDateTime() + '的' + this.appName.innerText);
    }

    publish() {
        const title = this.title.innerText || this.title.getAttribute('placeholder');
        const content = this.content.innerText;
        if (content.length === 0) {
            alert('字数过少');
            return;
        }

        if (this.poemId === null) {
            Request.post('/api/poem/', {title: title, content: content})
                .then(resp => {
                    this.title.innerText = '';
                    this.content.innerText = '';
                    window.location.href = '/';
                });
        } else {
            Request.put(`/api/poem/@${this.poemId}`, {title: title, content: content})
                .then(resp => {
                    this.readUIPrep();
                });
        }
    }
}
