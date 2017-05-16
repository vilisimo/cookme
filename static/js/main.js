function get_body() {
    return document.getElementsByTagName('body')[0];
}

function focusSearch() {
    const body = get_body();
    if (body.className === 'home') {
        const search_bar = document.getElementById('id_q');
        if (search_bar !== null) {
            search_bar.focus();
        }
    }
}