document.addEventListener('DOMContentLoaded', function() {
    const tagInput = document.querySelector('#id_tags');
    const tagContainer = document.querySelector('#tag-container');
    const tagInputField = document.querySelector('#tag-input-field');
    const form = document.querySelector('#postForm');
    const tagSearchUrl = form.getAttribute('data-tag-search-url'); // Get the URL from the form

    let suggestionsDropdown = document.createElement('div');
    suggestionsDropdown.className = 'dropdown-menu';
    tagContainer.appendChild(suggestionsDropdown);

    tagInput.style.display = 'none';

    let tags = tagInput.value ? tagInput.value.split(',').map(t => t.trim()).filter(t => t) : [];
    updateTagDisplay();

    tagInputField.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && this.value.trim()) {
            e.preventDefault();
            const newTag = this.value.trim().toLowerCase();
            if (tags.length < 5 && !tags.includes(newTag)) {
                tags.push(newTag);
                updateTagDisplay();
                this.value = '';
                suggestionsDropdown.classList.remove('show');
            } else if (tags.length >= 5) {
                alert('Maximum 5 tags allowed.');
            }
        }
    });

    tagInputField.addEventListener('input', function() {
        const query = this.value.trim();
        if (query.length > 0) {
            fetch(`${tagSearchUrl}?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsDropdown.innerHTML = '';
                    if (data.length > 0) {
                        data.forEach(tag => {
                            const suggestionItem = document.createElement('div');
                            suggestionItem.className = 'dropdown-item';
                            suggestionItem.textContent = tag.text;
                            suggestionItem.addEventListener('click', () => {
                                if (tags.length < 5 && !tags.includes(tag.text)) {
                                    tags.push(tag.text.toLowerCase());
                                    updateTagDisplay();
                                    tagInputField.value = '';
                                    suggestionsDropdown.classList.remove('show');
                                }
                            });
                            suggestionsDropdown.appendChild(suggestionItem);
                        });
                        suggestionsDropdown.classList.add('show');
                    } else {
                        suggestionsDropdown.classList.remove('show');
                    }
                })
                .catch(error => console.error('Error fetching suggestions:', error));
        } else {
            suggestionsDropdown.classList.remove('show');
        }
    });

    document.addEventListener('click', function(e) {
        if (!tagContainer.contains(e.target)) {
            suggestionsDropdown.classList.remove('show');
        }
    });

    tagInputField.addEventListener('focus', function() {
        if (this.value.trim().length > 0) {
            suggestionsDropdown.classList.add('show');
        }
    });

    function updateTagDisplay() {
        tagContainer.innerHTML = '';
        if (tags.length > 0) {
            tags.forEach(tag => {
                const tagElement = document.createElement('span');
                tagElement.className = 'tag';
                tagElement.innerHTML = `${tag} <span class="tag-remove" data-tag="${tag}">×</span>`;
                tagContainer.appendChild(tagElement);
            });
        }
        tagContainer.appendChild(tagInputField);
        tagContainer.appendChild(suggestionsDropdown);
        tagInput.value = tags.join(', ');
        
        // Add remove functionality
        document.querySelectorAll('.tag-remove').forEach(btn => {
            btn.addEventListener('click', function() {
                const tagToRemove = this.getAttribute('data-tag');
                tags = tags.filter(t => t !== tagToRemove);
                updateTagDisplay();
            });
        });
    }
});