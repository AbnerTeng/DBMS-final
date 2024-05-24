document.querySelectorAll('input[name="action"]').forEach(function (radio) {
    radio.addEventListener('change', function () {
        if (this.value === 'remove_background') {
            document.getElementById('imageUpload').style.display = 'block';
            document.getElementById('urlInput').style.display = 'none';
            document.getElementById('eventSelect').style.display = 'none';
            document.getElementById('receiverUpload').style.display = 'none';
        } else if (this.value === 'generate_qrcode') {
            document.getElementById('imageUpload').style.display = 'none';
            document.getElementById('urlInput').style.display = 'block';
            document.getElementById('eventSelect').style.display = 'none';
            document.getElementById('receiverUpload').style.display = 'none';
        } else {
            document.getElementById('imageUpload').style.display = 'none';
            document.getElementById('urlInput').style.display = 'none';
            document.getElementById('eventSelect').style.display = 'block';
            document.getElementById('receiverUpload').style.display = 'block';
        }
    });
});