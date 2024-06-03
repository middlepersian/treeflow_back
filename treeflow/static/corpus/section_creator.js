document.addEventListener('DOMContentLoaded', function () {
    let startTokenId = null;
    let endTokenId = null;
    let isSelectingTokens = false;
    let selectedTokens = [];
    let selectedTokenIds = [];
    let selectedTokenTexts = '';

    var csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
    var csrfToken = csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : null;

    if (csrfToken) {
        htmx.config.include = (name, value, el) => {
            if (name === "csrfmiddlewaretoken") {
                return csrfToken;
            }
            return value;
        };
    } else {
        console.error("CSRF token not available");
    }

    function addTokenClickListeners() {
        document.querySelectorAll('.token').forEach(token => {
            token.addEventListener('click', function () {
                if (isSelectingTokens) {
                    handleTokenClick(this);
                }
            });
        });
    }

    function handleTokenClick(tokenElement) {
        const tokenId = tokenElement.dataset.tokenId;
        if (startTokenId === null) {
            startTokenId = tokenId;
            tokenElement.classList.add('bg-green-200');
        } else if (endTokenId === null && tokenId !== startTokenId) {
            endTokenId = tokenId;
            highlightTokensBetween(startTokenId, endTokenId);
        }
    }

    function highlightTokensBetween(startId, endId) {
        let inRange = false;
        document.querySelectorAll('.token').forEach(token => {
            if (token.dataset.tokenId === startId || token.dataset.tokenId === endId) {
                inRange = !inRange;
                token.classList.add('bg-green-200');
            }
            if (inRange || token.dataset.tokenId === endId) {
                token.classList.add('bg-green-200');
            }
        });
    }

    document.getElementById('startTokenSelection').addEventListener('click', function () {
        let mode = this.getAttribute('data-mode');
        if (mode === 'select') {
            isSelectingTokens = true;
            this.textContent = 'Finish Token Selection';
            this.setAttribute('data-mode', 'finish');
        } else if (mode === 'finish') {
            isSelectingTokens = false;
            selectedTokens = Array.from(document.querySelectorAll('.token.bg-green-200'));
            selectedTokenIds = selectedTokens.map(token => token.dataset.tokenId);
            selectedTokenTexts = selectedTokens.map(token => token.textContent).join(', ');
            let queryString = `?tokens=${encodeURIComponent(selectedTokenIds.join(','))}&text_id=${encodeURIComponent(textId)}`;
            htmx.ajax('GET', '/corpus/load_section_modal_create/' + queryString, {
                target: '#modalContainer'
            }).then(() => {
                document.getElementById('modalTextId').value = textId;
            });
            this.textContent = 'Start Token Selection';
            this.setAttribute('data-mode', 'select');
        }
    });

    function closeModal() {
        var modal = document.getElementById('sectionModal');
        if (modal) {
            modal.classList.add('hidden');
            deselectAllTokens();
            isSelectingTokens = false;
            selectedTokenTexts = '';
        }
    }

    function deselectAllTokens() {
        document.querySelectorAll('.token.bg-green-200').forEach(token => {
            token.classList.remove('bg-green-200');
        });
        startTokenId = null;
        endTokenId = null;
        selectedTokenIds = [];
    }

    document.body.addEventListener('htmx:afterSwap', function (event) {
        if (event.target.id === 'modalContainer') {
            openModal();
            const cancelButton = document.querySelector('#sectionModal button[onclick="#sectionModal button[onclick="closeModal()"]');
            if (cancelButton) {
                cancelButton.onclick = closeModal;
            } else {
                console.error('Cancel button not found in the modal.');
            }
        }
    });

    function openModal() {
        let modal = document.getElementById('sectionModal');
        if (modal) {
            modal.classList.remove('hidden');
            document.getElementById('selectedTokensDisplay').textContent = selectedTokenTexts || 'No tokens selected';
        } else {
            console.error('Modal not found in the DOM.');
        }
    }

    addTokenClickListeners();

    // Define the observer for observing changes in the DOM
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'childList') {
                console.log('A child node has been added or removed.');
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
