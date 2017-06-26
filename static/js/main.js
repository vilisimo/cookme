"use strict";

function InputArea(id, charsLeftContainer, addEventFunction) {
    this.elementId = id;
    this.charsContainer = charsLeftContainer;
    this.applyEvent = addEventFunction;
}

$(function() {
    const elements = createElements();
    addEventsTo(elements);
});

function createElements() {
    const title = new InputArea('id_title', 'title_chars_left', addCharsLeftEvent);
    const description = new InputArea('id_description', 'description_chars_left', addCharsLeftEvent);
    const steps = new InputArea('id_steps', 'steps_chars_left', addCharsLeftEvent);

    return [title, description, steps]
}

function addEventsTo(elements) {
    elements.forEach((element) => element.applyEvent());
}

function addCharsLeftEvent() {
    const $textArea = $(`#${this.elementId}`);
    const $outputArea = $(`#${this.charsContainer}`);
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