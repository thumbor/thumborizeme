(function() {
  function checkURL(value) {
    var urlregex = new RegExp("^(http:\/\/www.|https:\/\/www.|ftp:\/\/www.|www.){1}([0-9A-Za-z]+\.)");
    if (urlregex.test(value)) {
      return (true);
    }
    return (false);
  }

  var website = $('#website');
  var input = website.find('input');
  var submit = $('#submit');

  submit.bind('click', function(ev) {
    var url = input.val();
    //console.log(url);
    if (!checkURL(url)) {
      website.addClass('has-error');
      return;
    } else {
      website.removeClass('has-error');
    }

    $.ajax(url, function(data) {
      console.log(data);
    });

    ev.preventDefault();
  });
})();
