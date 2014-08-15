(function() {
  function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
  }

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

  var social = $('.social');

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

  function updateUrl(url) {
    input.val(url);
    disable();

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
        var tweet = '';

        if (data["images-webp-size"] > data["images-size"]) {
          tweet = "Check your website details too!";
          result.removeClass('panel-success').addClass('panel-danger');
          resultText.html("By upgrading your image server to thumbor you would go from <strong>" + data["images-size"] + "kb</strong> to <strong>" + data["images-webp-size"] + "kb</strong> for <strong>" + data["images-count"] + "</strong> images (using WebP images).");
        } else {
          tweet = url + " could be saving " + (data["images-size"] - data["images-webp-size"]) + "kb by using thumbor!";
          result.removeClass('panel-danger').addClass('panel-success');
          resultText.html("By upgrading your image server to thumbor you would go from <strong>" + data["images-size"] + "kb</strong> to <strong>" + data["images-webp-size"] + "kb</strong> for <strong>" + data["images-count"] + "</strong> images, thus saving <strong>" + percentage + "%</strong> (using WebP images).");
        }

        progress.hide();
        result.fadeIn();

        social.html('');

        social.append('<a href="https://twitter.com/share" class="twitter-share-button" data-url="http://thumborize.me?url=' + url + '" data-text="' + tweet + '" data-hashtags="thumbor">Tweet</a>');

        social.append('<div ' +
            'class="fb-like" ' +
            'data-href="http://thumborize.me/?url=' + encodeURIComponent(url) + ' ' +
            'data-width="200" ' +
            'data-layout="button_count" ' +
            'data-show-faces="false" ' +
            'data-send="false"></div>');

        FB.XFBML.parse()
        twttr.widgets.load()

        enable();
      }
    });
  }

  console.log(submit);
  submit.bind('click', function(ev) {
    if (submit.attr('disabled') == 'disabled') {
      return;
    }

    var url = input.val();

    history.pushState({}, url + " - report", "?url=" + url);

    updateUrl(url);

    ev.preventDefault();
  });

  var url = getParameterByName('url');

  if (url != null) {
    updateUrl(url);
  }
})();
