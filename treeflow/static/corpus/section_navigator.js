// Scroll to top button
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.addEventListener('scroll', function () {
    const scrollToTopButton = document.querySelector('.scroll-to-top');
    if (window.scrollY > 200) {
        scrollToTopButton.classList.remove('hidden');
    } else {
        scrollToTopButton.classList.add('hidden');
    }
});

// Highlight tokens when a section is clicked
document.addEventListener('DOMContentLoaded', function () {
    const selector = document.getElementById('sectionTypeSelector');
    const sectionList = document.getElementById('sectionList');
    //const textId = '{{ text_id }}';


    function highlightSectionTokens(tokenIds) {
        const stringTokenIds = tokenIds.map(id => id.toString());
        const tokens = document.querySelectorAll('.token');
        tokens.forEach(token => {
            if (stringTokenIds.includes(token.dataset.tokenId)) {
                // Apply styles directly
                token.style.backgroundColor = '#fde047';
            } else {
                // Reset styles
                token.style.backgroundColor = '';
            }
        });
    }

    function fetchAndHighlightSectionTokens(sectionId) {
        fetch(`/corpus/get-tokens-for-section/${sectionId}`)
            .then(response => response.json())
            .then(data => {
                const tokenIds = data.tokens; // Assuming the backend sends an array of token IDs
                highlightSectionTokens(tokenIds);

                // Scroll to the first token of this section
                if (tokenIds.length > 0) {
                    const firstTokenId = tokenIds[0];
                    const firstTokenElement = document.querySelector(`.token[data-token-id="${firstTokenId}"]`);
                    if (firstTokenElement) {
                        firstTokenElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }
            })
            .catch(error => {
                console.error('Error fetching tokens for section:', error);
            });
    }

    function loadChildSections(sectionId, parentDiv) {
        // Check if child sections are already loaded
        const existingChildList = parentDiv.querySelector('.child-section-list');
        if (existingChildList) {
            // Remove the child list to 'close' the section
            parentDiv.removeChild(existingChildList);
            return; // Exit the function
        }
        fetch(`/corpus/get-child-sections/${sectionId}`)
            .then(response => response.json())
            .then(childSections => {
                const childSectionList = document.createElement('div');
                childSectionList.classList.add('child-section-list');

                childSections.forEach(childSection => {
                    const childDiv = document.createElement('div');
                    childDiv.classList.add('child-section-item');
                    childDiv.textContent = childSection.identifier || 'Untitled';
                    childDiv.dataset.sectionId = childSection.id;

                    // Add event listener to prevent event bubbling
                    childDiv.addEventListener('click', function (event) {
                        event.stopPropagation();
                        fetchAndHighlightSectionTokens(childSection.id);
                    });

                    childSectionList.appendChild(childDiv);
                });

                // Check if child sections are already loaded to avoid duplication
                if (!parentDiv.querySelector('.child-section-list')) {
                    parentDiv.appendChild(childSectionList);
                }
            })
            .catch(error => {
                console.error('Error fetching child sections:', error);
            });
    }

    function loadSectionsOfType(sectionType) {
        fetch(`/corpus/get-sections/${textId}/${sectionType}`)
            .then(response => response.json())
            .then(sections => {
                sectionList.innerHTML = '';
                sections.forEach(section => {
                    const sectionDiv = document.createElement('div');
                    sectionDiv.classList.add('section-item');
                    sectionDiv.textContent = section.identifier || 'Untitled';
                    sectionDiv.dataset.sectionId = section.id;

                    // Add event listener to load child sections    
                    sectionDiv.addEventListener('click', function () {
                        const isClosingSection = this.querySelector('.child-section-list');
                        loadChildSections(section.id, this);
                        // Only fetch and highlight tokens if the section is being opened
                        if (!isClosingSection) {
                            fetchAndHighlightSectionTokens(section.id);
                        }
                    });

                    sectionList.appendChild(sectionDiv);
                });

                if (sections.length === 0) {
                    sectionList.innerHTML = '<p>No sections found for this type.</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching sections:', error);
                sectionList.innerHTML = '<p>Error loading sections.</p>';
            });
    }

    selector.addEventListener('change', function () {
        loadSectionsOfType(this.value);
    });

    if (selector.options.length > 0) {
        loadSectionsOfType(selector.options[0].value);
    }
});
