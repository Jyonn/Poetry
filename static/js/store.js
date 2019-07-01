class Store {
    static load(key) {
        return window.localStorage.getItem(key);
    }

    static save(key, value) {
        window.localStorage.setItem(key, value);
    }
}