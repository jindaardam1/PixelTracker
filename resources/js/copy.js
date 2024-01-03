/**
 * Check if the text inside an <li> element is a valid email.
 * @param {HTMLElement} liElement - The <li> element to check.
 * @returns {boolean} - True if the text is a valid email, false otherwise.
 */
function isEmail(liElement) {
    // Regular expression for validating an email address
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // Get the text content inside the <li> element and trim any leading or trailing spaces
    const textInsideLi = liElement.textContent.trim();

    // Test if the text inside the <li> matches the email regular expression
    return emailRegex.test(textInsideLi);
}

/**
 * Handles the click event on the "Copy to Clipboard" button.
 * Iterates through all <li> elements, identifies valid emails, and copies them to the clipboard.
 */
function handleClick() {
    // Get all <li> elements on the page
    const liElements = document.querySelectorAll('li');

    // Array to store valid emails
    const validEmails = [];

    // Iterate over each <li> element and check if the text is an email
    liElements.forEach(function (liElement) {
        if (isEmail(liElement)) {
            validEmails.push(liElement.textContent.trim());
        }
    });

    // Copy emails to clipboard, separated by semicolon
    const emailsToCopy = validEmails.join(';');

    // Use the Clipboard API to copy the text to the clipboard
    navigator.clipboard.writeText(emailsToCopy)
        .then(() => {
            // You can log to the console or perform any other action
            console.log('Emails copied to clipboard:', emailsToCopy);
        })
        .catch(err => {
            console.error('Error copying to clipboard:', err);
        });
}

// Add an event listener to the button with the ID "buttonCopyToClipboard"
const copyButton = document.getElementById('buttonCopyToClipboard');
copyButton.addEventListener('click', handleClick);
