
document.addEventListener('DOMContentLoaded', function () {
    let startTokenId = null;
    let endTokenId = null;
    let isSelectingTokens = false;

    // Function to get the CSRF token
    function getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }


    // Function to open the modal and set selected token IDs
    function openSectionModal(selectedTokenIds) {
        // Set selected token IDs to the hidden field in the modal
        document.getElementById('hiddenSelectedTokensField').value = selectedTokenIds;
        // Make the modal visible by removing the 'hidden' class
        document.getElementById('sectionCreationModal').classList.remove('hidden');
    }

    function handleTokenClick(tokenElement) {
        console.log("Token clicked:", tokenElement.dataset.tokenId);
        const tokenId = tokenElement.dataset.tokenId;

        if (startTokenId === null) {
            startTokenId = tokenId;
            tokenElement.classList.add('bg-green-200'); // Highlighting
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
                token.classList.add('bg-green-200'); // Highlighting
            }
            if (inRange || token.dataset.tokenId === endId) {
                token.classList.add('bg-green-200'); // Highlighting
            }
        });
    }

    // Function to add event listeners to tokens
    function addTokenClickListeners() {
        document.querySelectorAll('.token').forEach(token => {
            token.addEventListener('click', function () {
                if (isSelectingTokens) {
                    handleTokenClick(this);
                }
            });
        });
    }

    // Add listeners to existing tokens
    addTokenClickListeners();

    // Event listener for the button
    document.getElementById('startTokenSelection').addEventListener('click', function () {
        let mode = this.getAttribute('data-mode');

        if (mode === 'select') {
            isSelectingTokens = true;
            this.textContent = 'Finish Token Selection';
            this.setAttribute('data-mode', 'finish');
        } else if (mode === 'finish') {
            isSelectingTokens = false;
            let selectedTokenIds = Array.from(document.querySelectorAll('.token.bg-green-200'))
                .map(token => token.dataset.tokenId)
                .join(',');

            // Open the modal with the selected token IDs
            openSectionModal(selectedTokenIds);

            // Reset the button text and mode
            this.textContent = 'Start Token Selection';
            this.setAttribute('data-mode', 'select');
        }
    });

    // Observe for dynamically added tokens
    const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.addedNodes && mutation.addedNodes.length > 0) {
                // Check if the added nodes contain tokens
                mutation.addedNodes.forEach(function (node) {
                    if (node.classList && node.classList.contains('token')) {
                        addTokenClickListeners();
                    }
                });
            }
        });
    });

    // Start observing
    observer.observe(document.body, { childList: true, subtree: true });


    // HTMX response event listener
    htmx.on('htmx:response', function (event) {
        if (event.detail.status === 200) {
            let jsonResponse = JSON.parse(event.detail.xhr.responseText);
            if (jsonResponse.redirect) {
                window.location.href = jsonResponse.redirect;
            }
        } else {
            // Handle other statuses or errors
        }
    });
});