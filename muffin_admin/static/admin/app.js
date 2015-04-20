/*global window, confirm, jQuery */

(function ($) {
  "use strict";

  $(function(){

    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Delete items
    $('.btn-delete').click(function(){
      $(this).button('toggle');
      var item = $(this).parents('tr')[0], id = $(item).data('pk'), modal=$(this).parents('.modal');
      $.ajax({
        url: window.base_url + '?pk=' + id,
        method: 'DELETE',
        success: function () {
          modal.modal('toggle');
          $('#item-' + id).hide(600);
        }
      });
    });

    // Reset a form
    $('.btn-reset').click(function(e){
      e.preventDefault();
      var parents = $(this).parents('.modal');
      parents.find('form').trigger('reset');
      parents.find('.has-error').removeClass('has-error');
      parents.find('.help-block').remove();
    });

    // Submit modal forms
    $(window.document).on('click', 'button[type="submit"]', function(){
      $(this).parents('.modal').find('form').submit();
    });

    // Parse modal forms
    $(window.document).on('submit', 'form', function(e){
      e.preventDefault();
      var $this = $(this),
          posting = $.post($this.attr('action'), $this.serialize());

      $this.find('.has-error').removeClass('has-error');
      $this.find('.help-block').remove();

      posting.done(function(){ window.location.reload();}).fail(function(data){
        var errors = data.responseJSON;
        $.each(errors, function(c, errors) {
          var parent = $this.find('#' + c).parent();
          parent.addClass('has-error');
          $.each(errors, function(c, e){
              parent.append('<p class="help-block">' + e + '</p>');
          });
        });
      });
    });

  });
  
}(jQuery));
