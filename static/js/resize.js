const textarea = document.getElementById('auto-resize');

textarea.value = ''

textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});
