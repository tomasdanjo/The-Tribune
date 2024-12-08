

function filter_feedback(selectedStatus) {
  console.log(selectedStatus);
 
  const articleId = document.querySelector('.dropdown').getAttribute('data-article-id');
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

  $.ajax({
      url: `/filter_feedbacks/${articleId}/`, // Dynamically set the URL
      type: "POST",
      data: {
          status: selectedStatus,
          csrfmiddlewaretoken: csrfToken, // CSRF token for security
      },
      beforeSend: function () {
          $('#feedbacks-container').html('<p>Loading feedback...</p>');
      },
      success: function (response) {
          if (response.status === 'success') {
              $('#feedbacks-container').html(response.feedback_html);
          } else {
              alert('Failed to filter feedback. Please try again.');
          }
      },
      error: function () {
          alert('An error occurred while fetching feedback. Please try again.');
      },
  });

}

function autoResize(textarea) {
  // Reset height to default
  textarea.style.height = '2.5rem';
  // If content exceeds one line, expand
  textarea.style.height = `${textarea.scrollHeight}px`;
}

document.addEventListener('DOMContentLoaded', () => {
    const textareas = document.querySelectorAll('textarea.textarea');
    const feedbackTextarea = document.getElementById('feedback-text');
    const feedbackSubmitGroup = document.querySelector('#feedback-form-container .submit-btn-group');
    const feedbackMessage = document.getElementById('feedback-message');

    textareas.forEach(textarea => {
        // Initial auto-resize
        autoResize(textarea);

        // Add event listeners for input and change
        textarea.addEventListener('input', () => autoResize(textarea));
        textarea.addEventListener('change', () => autoResize(textarea));
    });

    // Toggle visibility of submit-btn-group based on feedback textarea interaction
    feedbackTextarea.addEventListener('input', () => {
        if (feedbackTextarea.value.trim()) {
            feedbackSubmitGroup.style.display = 'flex';
            feedbackMessage.textContent = ''; // Clear validation message
        } else {
            feedbackSubmitGroup.style.display = 'none';
        }
    });

    const form = document.querySelector('.form-field');
    const textarea = form.querySelector('textarea[name="archive_reason"]');
    const archiveButton = form.querySelector('button[type="submit"]');

    archiveButton.addEventListener('click', function (event) {
        // Check if the textarea is empty
        if (textarea.value.trim() === "") {
            event.preventDefault(); // Prevent form submission
            alert("Please provide a reason before archiving."); // Display a warning
            textarea.focus(); // Focus the textarea for user input
        }
    });
});

function showArchiveForm() {
    document.getElementById("archive-form").style.display = "block";
    hidePublishForm();
}

function hideArchiveForm() {
    document.getElementById("archive-form").style.display = "none";
}

function showPublishForm() {
    document.getElementById("publish-form").style.display = "block";
    hideArchiveForm();
}

function hidePublishForm() {
    document.getElementById("publish-form").style.display = "none";
}



function clearFeedbackForm() {
    const feedbackTextarea = document.getElementById('feedback-text');
    const feedbackMessage = document.getElementById('feedback-message');
    const feedbackSubmitGroup = document.querySelector('#feedback-form-container .submit-btn-group');

    feedbackTextarea.value = '';
    feedbackMessage.textContent = '';
    feedbackSubmitGroup.style.display = 'none'; // Hide submit buttons after clearing
}

function submitFeedback(articleID) {
    const feedbackTextarea = document.getElementById('feedback-text');
    const feedbackText = feedbackTextarea.value.trim();
    const feedbackMessage = document.getElementById('feedback-message');
    const articleId = articleID// Assuming article ID is available in context

    // Validate feedback input
    if (!feedbackText) {
        feedbackMessage.textContent = 'Please enter feedback before submitting.';
        feedbackMessage.classList.add('text-red-500');
        feedbackTextarea.focus(); // Highlight input
        return;
    }

    $.ajax({
        url: `/submit_feedback/${articleId}/`, // Define this URL in Django to handle feedback
        type: "POST",
        data: {
            feedback: feedbackText,
            article_id: articleId,
            csrfmiddlewaretoken: '{{ csrf_token }}' // Ensure CSRF token is included
        },
        beforeSend: function() {
            feedbackMessage.textContent = 'Submitting...';
            feedbackMessage.classList.remove('text-red-500');
            feedbackMessage.classList.add('text-gray-500');
        },
        success: function(response) {
            if (response.status === 'success') {
                feedbackMessage.textContent = 'Feedback submitted successfully!';
                feedbackMessage.classList.remove('text-red-500');
                feedbackMessage.classList.add('text-green-500');
                clearFeedbackForm();
            } else {
                feedbackMessage.textContent = 'Error submitting feedback. Please try again.';
                feedbackMessage.classList.add('text-red-500');
            }

            $('#feedbacks-container').html(response.feedback_html);

            // Clear the textarea after submission
            $('#feedback-text').val('');
        },
        error: function() {
            feedbackMessage.textContent = 'An error occurred. Please try again later.';
            feedbackMessage.classList.add('text-red-500');
        }
    });
}