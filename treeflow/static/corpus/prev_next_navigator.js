<script>
  function logEventDetails(event) {
    console.log(`Event Triggered: ${event.type}`);
    console.log(`Control Key: ${event.ctrlKey}`);
    console.log(`Meta Key: ${event.metaKey}`);
    console.log(`Key: ${event.key}`);
  }

  document.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOMContentLoaded, adding keydown event listener.');

    document.addEventListener('keydown', function (event) {
      switch (event.key) {
        case 'ArrowLeft': // User pressed the left arrow key
          var prevPageLink = document.getElementById('prevPageLink');
          if (prevPageLink) {
            window.location.href = prevPageLink.href;
          }
          break;
        case 'ArrowRight': // User pressed the right arrow key
          var nextPageLink = document.getElementById('nextPageLink');
          if (nextPageLink) {
            window.location.href = nextPageLink.href;
          }
          break;
      }
    });
  });

</script>