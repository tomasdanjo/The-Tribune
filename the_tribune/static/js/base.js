document.addEventListener('DOMContentLoaded', function() {
  remove_injected_Attr()
});

function remove_injected_Attr(){
  document.querySelectorAll('textarea').forEach(function(textarea) {
    textarea.removeAttribute('style');
    textarea.removeAttribute('rows');
    
    textarea.removeAttribute('cpls');
  });
}

function autoResize(textarea) {
  // Reset height to default
  textarea.style.height = "2.5rem";
  // If content exceeds one line, expand
  textarea.style.height = `${textarea.scrollHeight}px`;
}