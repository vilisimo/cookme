window.addEventListener('DOMContentLoaded', setup, false);

function setup() {
    const recipe_title = document.getElementById('id_title');
    let max_length = recipe_title.getAttribute('maxlength');
    console.log(parseInt(max_length));

    /* Recipe creation listeners */
    let chars_left_div = document.getElementById('title_chars_left');
    recipe_title.addEventListener('input', function() {
        maxLength(recipe_title, chars_left_div, max_length)
    }, false);
}

function maxLength(element, chars_left_div, max_length) {
    let text_length = element.value.length;
    let left = max_length - text_length;

    if (left < max_length) {
        chars_left_div.textContent = `${left} characters left`;
    } else {
        chars_left_div.textContent = '';
    }
    console.log(left);
}