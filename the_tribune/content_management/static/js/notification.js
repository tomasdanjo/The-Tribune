




// Function to toggle the options menu
function toggleOptionsMenu(button) {
const menu = button.nextElementSibling;
menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

// Function to mark a notification as read and refresh the notifications container
function markAsRead(notificationId) {
fetch('/mark-as-read/', {
  method: 'POST',
  headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token  // Ensure CSRF token is defined in your template
  },
  body: JSON.stringify({ id: notificationId })
})
.then(response => response.json())
.then(data => {
  if (data.success) {
      closeOptionsMenu();
      fetchUnreadNotifications(); 
      fetchReadNotifications();  // Refresh the read notifications container
  } else {
      alert('Failed to mark notification as read');
  }
})
.catch(error => {
  console.error('Error:', error);
});
}

// Function to mark a notification as unread and refresh the notifications container
function markAsUnread(notificationId) {
fetch('/mark-as-unread/', {
  method: 'POST',
  headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token  // Ensure CSRF token is defined in your template
  },
  body: JSON.stringify({ id: notificationId })
})
.then(response => response.json())
.then(data => {
  if (data.success) {
      closeOptionsMenu();
      fetchReadNotifications();
      fetchUnreadNotifications();  // Refresh the unread notifications container
  } else {
      alert('Failed to mark notification as unread');
  }
})
.catch(error => {
  console.error('Error:', error);
});
}


// Function to close all options menus
function closeOptionsMenu() {
document.querySelectorAll('.options-menu').forEach(menu => {
menu.style.display = 'none';
});
}

// Close the menu when clicking outside
document.addEventListener('click', function(event) {
const optionsMenus = document.querySelectorAll('.options-menu');
optionsMenus.forEach(menu => {
if (!menu.contains(event.target) && !menu.previousElementSibling.contains(event.target)) {
menu.style.display = 'none';
}
});
});



function showReadNotifications(){
  const unreadContainer = document.getElementById('unread-notif-container');
  const readContainer = document.getElementById('read-notif-container');
  const unreadBtn = document.querySelector('#unread-tab');
  const readBtn = document.querySelector('#read-tab');


  unreadContainer.style.display = 'none';
  readContainer.style.display = 'block';
  readBtn.classList.add('active');
  unreadBtn.classList.remove('active');

  // Load read notifications if not already loaded
  if (readContainer.children.length <= 1) {
      fetchReadNotifications();
  }
}

function showUnreadNotifications(){
  const unreadContainer = document.getElementById('unread-notif-container');
  const readContainer = document.getElementById('read-notif-container');
  const unreadBtn = document.querySelector('#unread-tab');
  const readBtn = document.querySelector('#read-tab');

  unreadContainer.style.display = 'block';
  readContainer.style.display = 'none';
  unreadBtn.classList.add('active');
  readBtn.classList.remove('active');
}

function markAllAsRead(){
  const unreadContainer = document.getElementById('unread-notif-container');
  const readContainer = document.getElementById('read-notif-container');
  const unreadBtn = document.querySelector('#unread-tab');
  const readBtn = document.querySelector('#read-tab');
  fetch('/notifications/mark_all_read/', {
      method: 'POST',
      headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
      if (data.status === 'success') {
          // Clear unread notifications
          const notificationLinks = unreadContainer.querySelectorAll('a');
          notificationLinks.forEach(link => link.remove());

          // Fetch and populate read notifications
          fetchUnreadNotifications()
          fetchReadNotifications();
          document.getElementById('mark-all-btn').style.display = "none";

      }
  })
  .catch(error => console.error('Error:', error));
}

function addNotificationLinkListeners() {
  const unreadContainer = document.getElementById('unread-notif-container');
  const readContainer = document.getElementById('read-notif-container');
  const unreadBtn = document.querySelector('#unread-tab');
  const readBtn = document.querySelector('#read-tab');
  const notificationLinks = unreadContainer.querySelectorAll('a');
  notificationLinks.forEach(link => {
      link.addEventListener('click', function(e) {
          const notificationId = this.dataset.notificationId;
          
          // Mark this specific notification as read
          fetch(`/notifications/mark_read/${notificationId}/`, {
              method: 'POST',
              headers: {
                  'X-CSRFToken': getCookie('csrftoken'),
                  'Content-Type': 'application/json'
              }
          })
          .then(response => response.json())
          .then(data => {
              if (data.status === 'success') {
                  // Remove from unread, add to read
                  this.remove();
                  
                  // Optionally, update read notifications
                  fetchReadNotifications();
              }
          })
          .catch(error => console.error('Error:', error));
      });
  });
}

// Function to fetch and display read notifications using jQuery AJAX
function fetchReadNotifications() {
const readContainer = $('#read-notif-container');
$.ajax({
  url: '/notifications/read/',
  method: 'GET',
  success: function(html) {
      if (html.trim() !== "") {
          readContainer.html(html);
      } else {
          readContainer.html('<p>No read notifications</p>');
      }
  },
  error: function() {
      console.error('Error fetching read notifications.');
  }
});
}

// Function to fetch and display unread notifications using jQuery AJAX
function fetchUnreadNotifications() {
const unreadContainer = $('#unread-notif-container');
$.ajax({
  url: '/notifications/unread/',
  method: 'GET',
  success: function(html) {
      if (html.trim() !== "") {
          unreadContainer.html(html);
          $('#mark-all-btn').show();
      } else {
          unreadContainer.html('<p>No unread notifications</p>');
          $('#mark-all-btn').hide();
      }
  },
  error: function() {
      console.error('Error fetching unread notifications.');
  }
});
}

// Helper function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


document.addEventListener('DOMContentLoaded', function() {
  addNotificationLinkListeners();
});
