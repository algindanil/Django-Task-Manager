$(document).ready(function() {
    $('.habit-controls').on('click', function() {
      var habit = $(this);
      var url = habit.data('url');
      var csrf_token = habit.data('csrf');

      $.ajax({
        url: url,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrf_token,
        },
        success: function(response) {
            $('#currency-amount').text(parseFloat(response.currency_amount).toFixed(1));
            $('#lvl').text('LVL ' + response.lvl);
        },
        error: function(xhr, status, error) {
            // handle the error
        }
      });
    });
  });
