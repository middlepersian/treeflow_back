

document.addEventListener('DOMContentLoaded', function () {
    let startTokenId = null;
    let endTokenId = null;
    let isSelectingTokens = false;

    var csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfTokenMeta) {
        var csrfToken = csrfTokenMeta.getAttribute('content');
        console.log("CSRF token:", csrfToken);
        try {
            if (htmx && csrfToken) {
                htmx.config.include = (name, value, el) => {
                    if (name === "csrfmiddlewaretoken") {
                        return csrfToken;
                    }
                    return value;
                };
            } else {
                console.error("HTMX or CSRF token not available");
            }
        } catch (e) {
            console.error("Error configuring HTMX:", e);
        }
    } else {
        console.error("CSRF token meta tag not found");
    }



    // Declare the observer at the beginning
    const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.addedNodes && mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function (node) {
                    if (node.classList && node.classList.contains('token')) {
                        addTokenClickListeners();
                    }
                });
            }
        });
    });
    // Observer to observe the addition of new tokens
    function handleTokenClick(tokenElement) {
        console.log("Token clicked:", tokenElement.dataset.tokenId);
        const tokenId = tokenElement.dataset.tokenId;

        // When the first token is clicked, highlight it immediately
        if (startTokenId === null) {
            startTokenId = tokenId;
            tokenElement.style.backgroundColor = '#bbf7d0'; // Highlight the first token
        }
        // When the second token is clicked, highlight the range
        else if (endTokenId === null && tokenId !== startTokenId) {
            endTokenId = tokenId;
            highlightTokensBetween(startTokenId, endTokenId); // Highlight tokens between the range
        }
    }

    function highlightTokensBetween(startId, endId) {
        let inRange = false;
        document.querySelectorAll('.token').forEach(token => {
            if (token.dataset.tokenId === startId || token.dataset.tokenId === endId) {
                inRange = !inRange;
                token.style.backgroundColor = '#bbf7d0';
            }
            if (inRange || token.dataset.tokenId === endId) {
                token.style.backgroundColor = '#bbf7d0';
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
    document.getElementById('startTokenSelection').addEventListener('click', function () {
        let mode = this.getAttribute('data-mode');

        if (mode === 'select') {
            // Start selecting tokens logic
            isSelectingTokens = true;
            this.textContent = 'Finish Token Selection';
            this.setAttribute('data-mode', 'finish');
        } else if (mode === 'finish') {
            // Finish selecting tokens logic
            isSelectingTokens = false;
            let selectedTokens = Array.from(document.querySelectorAll('.token'))
                .filter(token => token.style.backgroundColor === 'rgb(187, 247, 208)');
            let selectedTokenIds = selectedTokens.map(token => token.dataset.tokenId);
            let selectedTokenTexts = selectedTokens.map(token => token.textContent).join(', ');

            // Use HTMX to fetch the modal content with the selected tokens as parameters
            htmx.ajax('GET', '/corpus/load_section_modal', {
                parameters: { tokens: selectedTokenIds.join(',') },
                target: '#modalContainer'
            });

            // Store selected token texts for display in the modal
            localStorage.setItem('selectedTokenTexts', selectedTokenTexts);

            // Reset the button for a new selection
            this.textContent = 'Start Token Selection';
            this.setAttribute('data-mode', 'select');
        }
    });

    // Function to show the modal
    function openModal() {
        // Ensure the modal exists in the DOM
        let modal = document.getElementById('sectionModal');
        if (modal) {
            modal.style.display = 'block';
            // Display the selected tokens
            let selectedTokenTexts = localStorage.getItem('selectedTokenTexts') || 'No tokens selected';
            document.getElementById('selectedTokensDisplay').textContent = selectedTokenTexts;
        } else {
            console.error('Modal not found in the DOM.');
        }
    }



    document.body.addEventListener('htmx:afterSwap', function (event) {
        if (event.target.id === 'modalContainer') {
            // Show the modal
            openModal();
        }
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