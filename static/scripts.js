$(document).ready(function(){
      var currentNotifications = [];
      var notifications = {};
      var url = "http://news-alertomatic.appspot.com/data.json";
      var timer;

      function checkCurrentNotifications() {

      }

      function createNotificationInstance(options) {
        if (options.notificationType == 'simple') {
          console.log("notify simple");
          return window.webkitNotifications.createNotification('', options.title, options.message);
        } else if (options.notificationType == 'html') {
          console.log("notify html " + options.data);

          return window.webkitNotifications.createHTMLNotification("<div><a href='sdf'>sdf</a>sdf</div>");
        }
      }

      function fetchData(){

          $.ajax({
            type: "GET",
            url: url,
            success: function(data){
                var result = $.parseJSON(data).results;

                $.each(result, function(item) {

                    var url = this.url;

                    if ($.inArray(url, currentNotifications) == -1){
                        //var message = "<div><a href='" + this.url + "'>" + this.title + "</a>" + this.position + "</div>";
                        var msg = 'Appeared and currently ranked ' + this.position;

                        createNotificationInstance({ notificationType: 'simple', title: this.title, message: msg }).show();
                        currentNotifications.push(url);
                        notifications[this.url] = {title : this.title, position: this.position};
                        var row = '<tr><td class="rank">' + this.position + '</td><td class="headline"><a href="' + this.url + '" title="' + this.title + '">' + this.title + '</a></td><td class="category"><a href="' + this.feed_url + '" title="' + this.category + '">' + this.category + '</a></td><td class="since">' +  this.created_at  + '</td></tr>';
                        $('table').prepend(row);
                    } else {

                        //createNotificationInstance({ notificationType: 'simple', title: this.title, message: msg }).show();
                    }

                });
            },
            error: function(){
                console.log("Failed to load data");
            }
          });
      }

      $('#start').click(function(event) {
        event.stopPropagation();
        if (window.webkitNotifications.checkPermission() == 0) {
            console.log("Permission + Notifications are supported!");
                timer = window.setInterval(function() {
                        fetchData();
                }, 1000);
        } else {
            console.log("Notifications are not supported for this Browser/OS version yet." );
            window.webkitNotifications.requestPermission();
        }
      });

      $('#stop').click(function(event) {
          event.stopPropagation();
          window.clearInterval(timer);
      });



});
