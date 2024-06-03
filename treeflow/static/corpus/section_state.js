const appState = {
    selectedSectionId: null,
    selectedTokens: [],
    selectedTokenIds: [],
    selectedTokenTexts: '',
    startTokenId: null,
    endTokenId: null,
    isSelectingTokens: false,
    csrfToken: document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
};

function dispatchCustomEvent(eventName, detail) {
    const event = new CustomEvent(eventName, { detail });
    document.dispatchEvent(event);
}

function updateTokenSelection(startId, endId, isSelected) {
    if (!isSelected) {
        deselectAllTokens();
    } else {
        appState.startTokenId = startId;
        appState.endTokenId = endId || startId; // Ensure we handle selections of single tokens.
        highlightTokensBetween(appState.startTokenId, appState.endTokenId);
    }
}

function highlightTokensBetween(startId, endId) {
    const tokens = document.querySelectorAll('.token');
    let inRange = false;
    tokens.forEach(token => {
        const tokenId = token.dataset.tokenId;
        if (tokenId === startId || tokenId === endId) {
            inRange = !inRange; // Toggle inRange when we hit a boundary token.
            token.classList.add('bg-green-200');
        }
        if (inRange || tokenId === endId) {
            token.classList.add('bg-green-200');
        }
    });
    updateSelectedTokens();
}

function updateSelectedTokens() {
    const selectedTokens = document.querySelectorAll('.token.bg-green-200');
    appState.selectedTokenIds = Array.from(selectedTokens, token => token.dataset.tokenId);
    appState.selectedTokenTexts = Array.from(selectedTokens, token => token.textContent).join(', ');
}

function deselectAllTokens() {
    document.querySelectorAll('.token').forEach(token => {
        token.classList.remove('bg-green-200');
    });
    appState.startTokenId = null;
    appState.endTokenId = null;
    appState.selectedTokenIds = [];
    appState.selectedTokenTexts = '';
}

document.addEventListener('sectionSelected', function (e) {
    appState.selectedSectionId = e.detail.sectionId;
    console.log(`Section ${appState.selectedSectionId} selected for editing.`);
});

document.addEventListener('tokensSelected', function (e) {
    appState.selectedTokens = e.detail.tokens;
    console.log(`Tokens selected: ${appState.selectedTokens.join(', ')}`);
});

document.addEventListener('startTokenSelection', function () {
    appState.isSelectingTokens = true;
});

document.addEventListener('finishTokenSelection', function () {
    appState.isSelectingTokens = false;
    // Update the UI or handle other operations needed when selection finishes
    updateSelectedTokens(); // Ensure we update the selected tokens' state when finishing selection.
});
