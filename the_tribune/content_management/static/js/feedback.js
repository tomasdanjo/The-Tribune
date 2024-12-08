

function togglePopup(button,event) {
  event.stopPropagation();
  // Find the popup menu associated with this button
  const popupMenu = button.nextElementSibling;

  // Toggle the "active" class on the popup menu
  popupMenu.classList.toggle("active");

  // Close any other open popup menus
  document.querySelectorAll(".popup-menu").forEach((menu) => {
    if (menu !== popupMenu) {
      menu.classList.remove("active");
    }
  });

  // Close the replies container if it's open and not associated with this button
  document.querySelectorAll(".replies-container").forEach((container) => {
    if (container !== button.closest(".feedback-container").querySelector(".replies-container")) {
      container.style.display = "none";
    }
  });
}


document.addEventListener("click", function (event) {
  // Check if the clicked element is not part of the popup menu or the triple-dot button
  if (
    !event.target.closest(".popup-menu") &&
    !event.target.closest(".triple-dot-btn")
  ) {
    // Hide all active popup menus
    document.querySelectorAll(".popup-menu").forEach((menu) => {
      menu.classList.remove("active");
    });
  }

  // Ensure replies-container is not shown when clicked outside
  if (!event.target.closest(".feedback-container")) {
    document.querySelectorAll(".replies-container").forEach((container) => {
      container.style.display = "none";
    });
  }
});

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('textarea').forEach(function(textarea) {
    textarea.removeAttribute('style'); // Removes any inline style attributes
  });
});

function resolveFeedback(feedbackId) {
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
  const dropdown = document.querySelector(`#display-feedback`);
  const status = dropdown ? dropdown.value : "show-all";

  $.ajax({
    url: `/resolve_feedback/${feedbackId}/`, // Adjust the URL based on your project structure
    type: "POST",
    data: {
      csrfmiddlewaretoken: csrfToken,
      status: status,
    },
    beforeSend: function () {
      $("#feedbacks-container").html("<p>Updating feedbacks...</p>"); // Optional: loading message
    },
    success: function (response) {
      if (response.status === "success") {
        // Refresh the feedback container with updated feedbacks
        $("#feedbacks-container").html(response.feedback_html);
      } else {
        alert(response.message || "Failed to resolve feedback.");
      }
    },
    error: function () {
      alert("An error occurred while resolving the feedback.");
    },
  });
}

function deleteFeedback(feedbackId) {
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
  const dropdown = document.querySelector(`#display-feedback`);
  const status = dropdown ? dropdown.value : "show-all";

  $.ajax({
    url: `/delete_feedback/${feedbackId}/`, // Adjust the URL based on your project structure
    type: "POST",
    data: {
      csrfmiddlewaretoken: csrfToken,
      status: status,
    },
    beforeSend: function () {
      $("#feedbacks-container").html("<p>deleting feedback...</p>"); // Optional: loading message
    },
    success: function (response) {
      if (response.status === "success") {
        // Refresh the feedback container with updated feedbacks
        $("#feedbacks-container").html(response.feedback_html);
      } else {
        alert(response.message || "Failed to resolve feedback.");
      }
    },
    error: function () {
      alert("An error occurred while resolving the feedback.");
    },
  });
}

function editFeedback(feedbackId,event) {
  event.stopPropagation();

  const bodyContainer = document.getElementById(`body-container-${feedbackId}`);
  const originalComment = bodyContainer.querySelector("p").textContent;
  const feedbackContainer = document.getElementById(`body-container-${feedbackId}`).closest(".feedback-container");

  const repliesContainer = feedbackContainer.querySelector(".replies-container");
  if (repliesContainer) {
    repliesContainer.style.display = "none";
  }

  // Replace the body container content with a textarea and save/cancel buttons
  bodyContainer.innerHTML = `
        <textarea id="edit-textarea-${feedbackId}" class="textarea field edit-textarea">${originalComment}</textarea>
        <div class="edit-actions submit-btn-group">
            <button class="cancel-btn submit-btn" onclick="cancelEdit(${feedbackId}, '${originalComment}')">Cancel</button>
            <button class="save-btn submit-btn highlight-btn" onclick="saveFeedback(${feedbackId},event)">Save</button>
        </div>
    `;

  bodyContainer.classList.add("edit-active");

  const textareas = document.querySelectorAll("textarea.textarea");
  const feedbackTextarea = document.getElementById("feedback-text");
  const feedbackSubmitGroup = document.querySelector(
    "#feedback-form-container .submit-btn-group"
  );
  const feedbackMessage = document.getElementById("feedback-message");

  textareas.forEach((textarea) => {
    // Initial auto-resize
    autoResize(textarea);

    // Add event listeners for input and change
    textarea.addEventListener("input", () => autoResize(textarea));
    textarea.addEventListener("change", () => autoResize(textarea));
  });

  const textarea = document.getElementById(`edit-textarea-${feedbackId}`);
  textarea.addEventListener('click', (e) => {
    e.stopPropagation(); // Stops the event from propagating up to parent elements
    if (repliesContainer) {
      repliesContainer.style.display = "none"; // Ensures it stays hidden
    }
  });
  remove_injected_Attr();
}

function saveFeedback(feedbackId, event) {
  event.stopPropagation();
  const textarea = document.getElementById(`edit-textarea-${feedbackId}`);
  const updatedComment = textarea.value;

  // Send an AJAX request to update the feedback on the server
  fetch(`/feedback/update/${feedbackId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    body: JSON.stringify({ comment: updatedComment }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Update the UI with the new comment
        const bodyContainer = document.getElementById(`body-container-${feedbackId}`);
        bodyContainer.innerHTML = `<p>${updatedComment}</p>`;
        bodyContainer.classList.remove("edit-active");

        // Hide the popup menu after saving
        const feedbackContainer = bodyContainer.closest('.feedback-container');
        const popupBtn = feedbackContainer.querySelector('.triple-dot-btn');
        if (popupBtn) {
          togglePopup(popupBtn, event);
        }
      } else {
        alert("Failed to update feedback.");
      }
    })
    .catch((error) => console.error("Error:", error));

  remove_injected_Attr(); // Ensure this function is defined to remove any injected styles or attributes
}
 
function cancelEdit(feedbackId, originalComment) {
  // Restore the original comment
  const bodyContainer = document.getElementById(`body-container-${feedbackId}`);
  bodyContainer.innerHTML = `<p>${originalComment}</p>`;
  bodyContainer.classList.remove("edit-active");

  const feedbackContainer = bodyContainer.closest('.feedback-container');
  const popupBtn = feedbackContainer.querySelector('.triple-dot-btn');
  if (popupBtn) {
    togglePopup(popupBtn, event);
  }
}

function hideRepliesContainer(event) {
  event.stopPropagation();

  // Find the closest replies-container from the clicked button
  const repliesContainer = event.target.closest(".replies-container");

  if (repliesContainer) {
    const textarea = repliesContainer.querySelector("textarea");
    const submitBtnGroup = repliesContainer.querySelector(".submit-btn-group");

    // Hide replies container
    repliesContainer.style.display = "none";

    // Clear textarea
    if (textarea) {
      textarea.value = "";
    }

    // Hide submit button group
    if (submitBtnGroup) {
      submitBtnGroup.style.display = "none";
    }
  }
}

// Function to show reply form
function showReplyForm(event, feedbackContainers) {
  // Prevent event from propagating to document click handler
  event.stopPropagation();

  // Hide all other open reply containers
  feedbackContainers.forEach((container) => {
    if (container !== event.currentTarget) {
      container.querySelector(".replies-container").style.display = "none";
    }
  });

  // Toggle the clicked container's replies-container
  const repliesContainer = event.currentTarget.querySelector(".replies-container");
  repliesContainer.style.display = "block";
}

// Function to handle textarea focus
function handleTextareaFocus(event) {
  // Stop propagation to prevent closing
  event.stopPropagation();

  // Ensure replies-container is visible
  const repliesContainer = event.target.closest(".replies-container");
  repliesContainer.style.display = "block";

  // Show submit button group
  const submitBtnGroup = repliesContainer.querySelector(".submit-btn-group");
  submitBtnGroup.style.display = "flex";
}

// Function to handle clicks outside feedback containers
function handleOutsideClick(event, feedbackContainers) {
  feedbackContainers.forEach((container) => {
    const repliesContainer = container.querySelector(".replies-container");
    const isClickInside = container.contains(event.target);

    if (!isClickInside) {
      repliesContainer.style.display = "none";

      // Hide submit button group and reset textarea
      const submitBtnGroup = repliesContainer.querySelector(".submit-btn-group");
      submitBtnGroup.style.display = "none";

      const textarea = repliesContainer.querySelector("textarea");
      textarea.value = "";
    }
  });
}

// Function to initialize event listeners
function initializeFeedbackEventListeners() {
  const feedbackContainers = document.querySelectorAll(".feedback-container");

  // Attach event listeners to each feedback container
  feedbackContainers.forEach((container) => {
    container.addEventListener("click", (event) => showReplyForm(event, feedbackContainers));

    const textarea = container.querySelector(".textarea");
    textarea.addEventListener("focus", handleTextareaFocus);

    // Prevent textarea click from closing replies-container
    textarea.addEventListener("click", (event) => {
      event.stopPropagation();
    });
  });

  // Attach a click event listener to the document for handling clicks outside feedback containers
  document.addEventListener("click", (event) => handleOutsideClick(event, feedbackContainers));
}

// Call this function to initialize event listeners
initializeFeedbackEventListeners();

function addreply(feedbackId) {
  const textarea = document.querySelector(`#feedback-container-${feedbackId} .replies-container .textarea`);
  const replyText = textarea.value.trim();
  const feedbackMessage = document.getElementById('feedback-message');

  // Validate input
  if (!replyText) {
    feedbackMessage.textContent = 'Please enter a reply before submitting.';
    feedbackMessage.classList.add('text-red-500');
    textarea.focus();
    return;
  }

  // Send an AJAX request using jQuery
  $.ajax({
    url: `/reply/add/${feedbackId}/`,
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ reply: replyText }),
    headers: {
      'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    success: function (data) {
      console.log("Server response:", data); // Debug: Check response structure

      if (data.success) {
        // Update the replies container with the new replies
        const replyContainer = document.querySelector(`#feedback-container-${feedbackId} .reply-container`);
        replyContainer.innerHTML = data.replies_html;
        textarea.value = ''; // Clear the textarea after submission
      } else {
        feedbackMessage.textContent = 'Error submitting reply. Please try again.';
        feedbackMessage.classList.add('text-red-500');
      }
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
      feedbackMessage.textContent = 'An error occurred. Please try again later.';
      feedbackMessage.classList.add('text-red-500');
    }
  });
}

