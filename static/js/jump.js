class Jump {
    static _base_jump(url) {
        window.location.href = url;
    }
    static center() {
        Jump._base_jump('/');
    }
    static oauth() {
        Jump._base_jump('https://sso.6-79.cn/oauth/?app_id=IOWQrFWG');
    }
}
