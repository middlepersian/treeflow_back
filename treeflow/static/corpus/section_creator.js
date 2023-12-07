

document.addEventListener('DOMContentLoaded', function () {
    let startTokenId = null;
    let endTokenId = null;
    let isSelectingTokens = false;
    let selectedTokens = []; // Array to hold selected tokens
    let selectedTokenIds = []; // Array to hold selected token IDs
    let selectedTokenTexts = ''; // String to hold selected token texts


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
            tokenElement.classList.add('bg-green-200'); // Highlight the first token using Tailwind class
        }
        // When the second token is clicked, highlight the range
        else if (endTokenId === null && tokenId !== startTokenId) {
            endTokenId = tokenId;
            highlightTokensBetween(startTokenId, endTokenId); // Highlight tokens between the range using Tailwind class
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

        // Log the value of textId
        console.log("Current textId:", textId);

        if (mode === 'select') {
            // Start selecting tokens logic
            isSelectingTokens = true;
            this.textContent = 'Finish Token Selection';
            this.setAttribute('data-mode', 'finish');
        } else if (mode === 'finish') {
            // Finish selecting tokens logic
            isSelectingTokens = false;
            selectedTokens = Array.from(document.querySelectorAll('.token'))
                .filter(token => token.classList.contains('bg-green-200'));
            selectedTokenIds = selectedTokens.map(token => token.dataset.tokenId);
            selectedTokenTexts = selectedTokens.map(token => token.textContent).join(', ');
    
            let queryString = `?tokens=${encodeURIComponent(selectedTokenIds.join(','))}&text_id=${encodeURIComponent(textId)}`;
            // Issue a GET request with the constructed query string
            htmx.ajax('GET', '/corpus/load_section_modal' + queryString, {
                target: '#modalContainer'
            }).then(() => {
                // After the modal content is loaded, set the value of the hidden input
                document.getElementById('modalTextId').value = textId;
                console.log('Modal content loaded');
            });
        
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
            document.getElementById('selectedTokensDisplay').textContent = selectedTokenTexts || 'No tokens selected';
        } else {
            console.error('Modal not found in the DOM.');
        }
    }


    function deselectAllTokens() {
        document.querySelectorAll('.token').forEach(token => {
            token.classList.remove('bg-green-200'); // Reset the token using Tailwind class
        });
        startTokenId = null; // Reset start token ID
        endTokenId = null;   // Reset end token ID
        selectedTokenIds = []; // Reset selected token IDs
    }


    function closeModal() {
        console.log('Closing modal');
        var modal = document.getElementById('sectionModal');
        if (modal) {
            modal.style.display = 'none';
            deselectAllTokens(); // Deselect tokens when closing the modal
            isSelectingTokens = false; // Reset the token selection flag
            selectedTokenTexts = ''; // Reset the selected token texts
        }
    }
    

    document.body.addEventListener('htmx:afterSwap', function (event) {
        console.log('htmx:afterSwap event triggered', event);
        if (event.target.id === 'modalContainer') {
            // Show the modal
            openModal();
            // Bind closeModal to the Cancel button in the modal
            const cancelButton = document.querySelector('#sectionModal button[onclick="closeModal()"]');
            if (cancelButton) {
                cancelButton.onclick = closeModal; // Bind closeModal function

            } else {
                console.error('Cancel button not found in the modal.');
            }
        }
    });

    // Start observing
    observer.observe(document.body, { childList: true, subtree: true });
  
});