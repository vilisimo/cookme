window.addEventListener('DOMContentLoaded', attachEventHandlers, false);

function Element(id, charsLeftContainer) {
    this.elementId = id;
    this.charsContainer = charsLeftContainer;
}

function attachEventHandlers() {
    const title = new Element('id_title', 'title_chars_left');
    const description = new Element('id_description', 'description_chars_left');
    const steps = new Element('id_steps', 'steps_chars_left');

    addCharsLeftEventTo(title);
    addCharsLeftEventTo(description);
    addCharsLeftEventTo(steps);
}

function addCharsLeftEventTo(element) {
    const textArea = document.getElementById(element.elementId);
    const outputArea = document.getElementById(element.charsContainer);

    textArea.addEventListener('input', function() {
        showCharsLeft(textArea, maxLengthOf(textArea), outputArea)
    }, false);
}

function maxLengthOf(element) {
    return element.getAttribute('maxlength');
}

function showCharsLeft(element, maxLength, charsLeftDiv) {
    const textLength = element.value.length;
    const left = maxLength - textLength;

    if (left < maxLength) {
        charsLeftDiv.textContent = `${left} characters left`;
    } else {
        charsLeftDiv.textContent = '';
    }
}