(function() {
  function checkURL(s) {
    var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
    return regexp.test(s);
  }

  var website = $('#website');
  var input = website.find('input');
  var submit = $('#submit');

  var result = $('.result');
  var resultTitle = result.find('.result-url');
  var resultText = result.find('.result-text');

  var progress = $('.study-progress');

  result.hide();
  progress.hide()

  function disable() {
    submit.attr('disabled', 'disabled');
    input.attr('readonly', 'readonly');
  }

  function enable() {
    submit.removeAttr('disabled');
    input.removeAttr('readonly');
  }

  submit.bind('click', function(ev) {
    if (submit.attr('disabled') == 'disabled') {
      return;
    }

    disable();

    var url = input.val();
    if (!checkURL(url)) {
      website.addClass('has-error');
      enable();
      return;
    } else {
      website.removeClass('has-error');
    }

    result.hide();
    progress.fadeIn();

    $.ajax("/report?url=" + url, {
      dataType: 'json',
      success: function(data) {
        resultTitle.text(url);

        var percentage = 100 - (Math.round((data["images-webp-size"] / data["images-size"]) * 100 * 100, 2) / 100);

        if (data["images-webp-size"] > data["images-size"]) {
          result.removeClass('panel-success').addClass('panel-danger');
          resultText.html("By upgrading your image server to thumbor you would go from <strong>" + data["images-size"] + "kb</strong> to <strong>" + data["images-webp-size"] + "kb</strong> for <strong>" + data["images-count"] + "</strong> images (using WebP images).");
        } else {
          result.removeClass('panel-danger').addClass('panel-success');
          resultText.html("By upgrading your image server to thumbor you would go from <strong>" + data["images-size"] + "kb</strong> to <strong>" + data["images-webp-size"] + "kb</strong> for <strong>" + data["images-count"] + "</strong> images, thus saving <strong>" + percentage + "%</strong> (using WebP images).");
        }

        progress.hide();
        result.fadeIn();
        enable();
      }
    });

    ev.preventDefault();
  });
})();
