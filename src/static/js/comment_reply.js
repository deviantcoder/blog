document.addEventListener('DOMContentLoaded', () => {
    const replyButtons = document.querySelectorAll('.reply-btn');
    const cancelButtons = document.querySelectorAll('.cancel-reply');

    replyButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const commentId = btn.getAttribute('data-comment-id');
            const formContainer = document.getElementById(`reply-form-${commentId}`);
            document.querySelectorAll('.reply-form-container').forEach(container => {
                if (container !== formContainer) container.style.display = 'none';
            });
            formContainer.style.display = formContainer.style.display === 'block' ? 'none' : 'block';
            formContainer.querySelector('textarea').focus();
        });
    });

    cancelButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const commentId = btn.getAttribute('data-comment-id');
            const formContainer = document.getElementById(`reply-form-${commentId}`);
            formContainer.style.display = 'none';
        });
    });
});