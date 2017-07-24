"use strict";

function InputArea(id, charsLeftContainer, addEventFunction) {
    this.elementId = id;
    this.charsContainer = charsLeftContainer;
    this.applyEvent = addEventFunction;
}

$(function() {
    /* Add char counters to text input areas */
    const elements = createElements();
    addInputEventsTo(elements);

    /* Add image validator to image field (activated on form submit) */
    const imageField = $('#id_image');
    imageField.change(function() {
        const _URL = window.URL || window.webkitURL;
        let image, file;
        if ((file = this.files[0])) {
            image = new Image();
            image.onload = function () {
                const allowedWidth = imageField.attr('data-width');
                const allowedHeight = imageField.attr('data-height');
                if (allowedWidth < this.width && allowedHeight < this.height) {
                    $('.recipe-image').find('.errorlist').remove();
                    $(`<ul class="errorlist">
                        <li>
                          Uploaded image is too big. <br/>
                          Allowed dimensions: ${allowedWidth} x ${allowedHeight}<br/> 
                          Uploaded image: ${this.width} x ${this.height}
                        </li>
                      </ul>`
                    ).insertAfter(imageField);
                }
            };
            image.src = _URL.createObjectURL(file);
        }
    });
});

function createElements() {
    const title = new InputArea('id_title', 'title_chars_left', addCharsLeftEvent);
    const description = new InputArea('id_description', 'description_chars_left', addCharsLeftEvent);
    const steps = new InputArea('id_steps', 'steps_chars_left', addCharsLeftEvent);

    return [title, description, steps]
}

function addCharsLeftEvent() {
    const $textArea = $(`#${this.elementId}`);
    const $outputArea = $(`#${this.charsContainer}`);
    $textArea.on('input', function() {
        showCharsLeft($textArea, maxLengthOf($textArea), $outputArea)
    }).on('blur', function() {
        $outputArea.hide();
    });
}

function showCharsLeft(element, maxLength, charsLeftDiv) {
    const textLength = element.val().length;
    const charsLeft = maxLength - textLength;

    if (charsLeft < maxLength) {
        charsLeftDiv.text(`${charsLeft} characters left`).show();
    } else {
        charsLeftDiv.text('');
    }
}

function maxLengthOf(element) {
    return element.attr('maxlength');
}

function addInputEventsTo(elements) {
    elements.forEach((element) => element.applyEvent());
}

