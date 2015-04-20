/*global window, confirm, jQuery */

(function ($) {
  "use strict";

  $.fn.serializeObject = function () {
      var o = {};
      var a = this.serializeArray();
      $.each(a, function () {
        if (o[this.name] !== undefined) {
          if (!o[this.name].push) {
            o[this.name] = [o[this.name]];
          }
          o[this.name].push(this.value || '');
        } else {
          o[this.name] = this.value || '';
        }
      });
      return o;
  };

  $(function(){

    var seek = {};

    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Prepare data
    $.each(window.data, function(c, item){
        seek[item.id] = item;
    });

    // Delete items
    $('.btn-delete').click(function(){
      $(this).button('toggle');
      var item = $(this).parents('tr')[0], id = item.onclick(), data = seek[id];
      var confirmation = confirm('Are you sure to delete this item #' + data.id + '?');
      if (!confirmation) {
        $(this).button('toggle');
        return false;
      }
      $.ajax({
        url: window.base_url + '/' + data.id,
        method: 'DELETE',
        success: function () {
          $('#item-' + data.id).hide(600);
          // window.location.reload();
        }
      });
    });

    // Reset a form
    $('.btn-reset').click(function(e){
      e.preventDefault();
      $(this).parents('form').trigger('reset');
    });

    // Create an item
    $('.form-create').submit(function(e) {
      e.preventDefault();
      var data = $(this).serializeObject();
      console.log(data);
    });

  });
  
}(jQuery));
