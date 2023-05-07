$(document).ready(function() {
    $('.task-checkbox').on('click', function() {
      var checkbox = $(this);
      var url = checkbox.data('url');
      var csrf_token = checkbox.data('csrf');
      var is_completed = checkbox.prop('checked');

      $.ajax({
        url: url,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrf_token,
            'is_completed': is_completed
        },
        success: function(response) {
            checkbox.prop('checked', response.completed);
        },
        error: function(xhr, status, error) {
            // handle the error
        }
      });
    });
  });
