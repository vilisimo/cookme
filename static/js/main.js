function Element(id, charsLeftContainer) {
    this.elementId = id;
    this.charsContainer = charsLeftContainer;
}

$(function() {
    const title = new Element('id_title', 'title_chars_left');
    const description = new Element('id_description', 'description_chars_left');
    const steps = new Element('id_steps', 'steps_chars_left');

    addCharsLeftEventTo(title);
    addCharsLeftEventTo(description);
    addCharsLeftEventTo(steps);
});

function addCharsLeftEventTo(element) {
    const $textArea = $(`#${element.elementId}`);
    const $outputArea = $(`#${element.charsContainer}`);
    $textArea.on('input', function() {
        showCharsLeft($textArea, maxLengthOf($textArea), $outputArea)
    });
}

function showCharsLeft(element, maxLength, charsLeftDiv) {
    const textLength = element.val().length;
    const charsLeft = maxLength - textLength;

    if (charsLeft < maxLength) {
        charsLeftDiv.text(`${charsLeft} characters left`);
    } else {
        charsLeftDiv.text('');
    }
}

function maxLengthOf(element) {
    return element.attr('maxlength');
}