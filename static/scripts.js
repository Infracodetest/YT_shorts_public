document.getElementById('generate-form').addEventListener('submit', function() {
    showLoadingBar();
});

document.getElementById('improve-form').addEventListener('submit', function() {
    showLoadingBar();
});

document.getElementById('audio-form').addEventListener('submit', function() {
    showLoadingBar();
});

function showLoadingBar() {
    const loadingBar = document.getElementById('loading-bar');
    loadingBar.style.display = 'block';
    let width = 0;
    const interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
        } else {
            width++;
            loadingBar.style.width = width + '%';
        }
    }, 50);
}

function copyText(elementId) {
    const text = document.getElementById(elementId).innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    });
}
