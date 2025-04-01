document.addEventListener('DOMContentLoaded', function() {
    const headerImageInput = document.getElementById('id_header_image');
    const preview = document.getElementById('imagePreview');
    const previewImage = document.getElementById('previewImage');

    if ('{{ form.instance.header_image }}' && previewImage) {
        preview.style.display = 'block';
    }
    
    headerImageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                preview.style.display = 'block';
                previewImage.src = e.target.result;
            }
            
            reader.readAsDataURL(file);
        }
    });
});