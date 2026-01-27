// project/static/js/scripts.js

let currentMessage = null;

function showMessage(text, color) {
    if (currentMessage && currentMessage.parentNode) {
        currentMessage.remove();
    }

    const msg = document.createElement('div');
    msg.textContent = text;
    msg.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px;
        background: ${color === 'green' ? '#d4edda' : '#f8d7da'};
        color: ${color};
        border-radius: 8px;
        z-index: 11;
        font-weight: bold;
    `;

    document.body.appendChild(msg);
    currentMessage = msg;

    setTimeout(() => {
        if (msg.parentNode) {
            msg.remove();
        }
        currentMessage = null;
    }, 3000);
}