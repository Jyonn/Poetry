class PageArranger {
    constructor({indexPageId, writerPageId}) {
        this.indexPage = document.getElementById(indexPageId);
        this.writerPage = document.getElementById(writerPageId);
    }

    index() {
        this.indexPage.style.left = '0';
        this.writerPage.style.left = '100vw';
    }

    writer() {
        this.indexPage.style.left = '-100vw';
        this.writerPage.style.left = '0';
    }
}