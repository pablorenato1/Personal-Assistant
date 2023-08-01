// event_handler.js

// Function to handle the event listeners for previous, play/pause, and next buttons
function addEventListeners() {
  const previousButton = document.querySelector("#previous-button");
  const pauseAndPlayButton = document.querySelector("#btn-play-pause");
  const nextButton = document.querySelector("#next-button");

  previousButton.addEventListener("click", () => {
      callBackgroundFunction("prev");
  });

  pauseAndPlayButton.addEventListener("click", () => {
      callBackgroundFunction("play");
  });

  nextButton.addEventListener("click", () => {
      callBackgroundFunction("next");
  });
}






function callBackgroundFunction(command) {
  // Send an AJAX request to your Django view
  var xhr = new XMLHttpRequest();
  xhr.open("GET", `/playback/?command=${command}`, true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        // Update the HTML tag with the result
        // document.getElementById("resultTag").textContent = xhr.responseText;
      } else {
        // Handle error cases
        // document.getElementById("resultTag").textContent = "Error occurred.";
      }
    }
  };

  xhr.send();
}
