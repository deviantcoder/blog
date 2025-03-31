document.addEventListener('DOMContentLoaded', function () {
    var easyMDE = new EasyMDE({
        element: document.getElementById('id_content'),
        toolbar: [
            'bold', 'italic', 'heading', 'code', '|',
            'quote', 'unordered-list', 'ordered-list', '|',
            'link', 'image', 'horizontal-rule', '|',
            'preview', 'side-by-side', 'fullscreen', 'table',
        ],
        spellChecker: false,
        status: false,
        renderingConfig: {
            codeSyntaxHighlighting: true
        }
    });

    document.getElementById('postForm').addEventListener('submit', function (e) {
        var content = easyMDE.value().trim();
        document.getElementById('id_content').value = content;
        document.getElementById('id_content').removeAttribute('required');
    });
});