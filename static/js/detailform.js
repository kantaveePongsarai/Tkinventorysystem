$(document).ready(function() {

    function calculateTotal(currentGroup) {
      var $table = currentGroup.closest('table');
      var groupTotal = 0;
  
      $table.find('.rowTotal').each(function() {
        groupTotal += parseFloat($(this).text()) || 0;
      });
  
      $table.find('.total, .subtotal').text(groupTotal.toFixed(2));
    }
  
    $(".document.active").delegate(".tdDelete", "click", function() {
      var $this = $(this);
      var $tbody = $this.closest('tbody');
      var $row = $this.closest('tr');
  
      if ($tbody.children().length > 1) {
        $row.find('.rowTotal').text('0');
        calculateTotal($this);
        $row.remove();
      }
    });
  
    $(".document.active").delegate(".trAdd", "click", function() {
      var $table = $(this).closest('table');
      var $lastRow = $table.find('tbody tr:last-child').clone();
  
      $table.find('tbody').append($lastRow);
      calculateTotal($(this));
    });
  
    $(".document.active").delegate(".amount", "keyup", function() {
      calculateTotal($(this));
    });
  
    $(".document.active .proposedWork").delegate("td:not(.description, .unit)", "keyup", function() {
      var $row = $(this).closest('tr');
      var tdValues = [];
  
      $row.find('td').each(function(index) {
        if (index > 4) return false;
        var value = parseFloat($(this).text()) || 0;
        tdValues[index] = value;
        if (index === 4) $(this).text((tdValues[0] * tdValues[3]).toFixed(2));
      });
  
      calculateTotal($(this));
    });
  
  });