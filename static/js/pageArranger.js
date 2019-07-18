class PageArranger {
    constructor({indexPageId, writerPageId}) {
        this.indexPage = document.getElementById(indexPageId);
        this.writerPage = document.getElementById(writerPageId);
    }

    index() {
        activate(this.indexPage);
        deactivate(this.writerPage);
    }

    writer() {
        activate(this.writerPage);
        deactivate(this.indexPage);
    }
}