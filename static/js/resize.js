const textarea = document.getElementById('auto-resize');

textarea.value = '';
const initialHeight = textarea.scrollHeight;
textarea.style.height = initialHeight + "px";

textarea.addEventListener('input', function() {
    this.style.height = "auto";
    const newHeight = Math.max(this.scrollHeight, initialHeight)
    this.style.height = (newHeight) + "px";
});
