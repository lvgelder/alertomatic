        var chromeNotify = false;
        var currentNotifications = [];
        var notifications = {};
        //var url = "http://news-alertomatic.appspot.com/data.json";
        var url = "http://localhost:9521/data.json";

        var checkFeedTime = 1000;
        var checkFeedTimer;
        var dismissNotification = 300000; // 5 minutes


        function createNotificationInstance(options) {
          if (options.notificationType == 'simple') {
            //console.log("notify simple");
            return window.webkitNotifications.createNotification('', options.title, options.message);
          } else if (options.notificationType == 'html') {
            //console.log("notify html " + options.data);
            return window.webkitNotifications.createHTMLNotification("<div><a href='sdf'>sdf</a>sdf</div>");
          }
        }

        function msgUser(item, state){
            var title = item.category + ': ' + item.title;
            var msg = state + ' and ranked ' + item.position;
            
            var notification = createNotificationInstance({ notificationType: 'simple', title: title, message: msg });

            notification.show();
           
            window.setTimeout(function() {
                notification.cancel();
            }, dismissNotification);
        }

        function fetchData(){

            $.ajax({
              type: "GET",
              url: url,
              success: function(data){
                  var result = $.parseJSON(data).results;
                  // add new items

                  // check if item has been removed
                  $.each(currentNotifications, function(item) {
                    if ($.inArray(this, result) != -1){

                        var itemToRemove = notifications[this];

                        // send notification to user
                        if(chromeNotify) {
                            msgUser(itemToRemove, "Disappeared");
                        }

                        removeItem(this);

                        currentNotifications.pop(this);
                    }
                  });

                  $.each(result, function(item) {

                    // if you haven't seen it before
                    if ($.inArray(this.url, currentNotifications) == -1){
                      //var message = "<div><a href='" + this.url + "'>" + this.title + "</a>" + this.position + "</div>";

                      // send notification to user
                          if(chromeNotify) {
                            msgUser(this, "Appeared");
                        }

                      // track notification
                      currentNotifications.push(this.url);
                      notifications[this.url] = this;

                      addItem(this);

                    // if you have seen it before - update it?
                    } else {

                      updateItem(this);
                        
                    }

                  });

              },
              error: function(){
                  $('error').html("Sorry we couldn't update this time...");
              }
            });
        }

        function updateItem(item) {
           var row = '<td class="rank">' + item.position + '</td><td class="headline"><a href="' + item.url + '" title="' + item.title + '">' + item.title + '</a></td><td class="category"><a href="' + item.feed_url + '" title="' + item.category + '">' + item.category + '</a></td><td class="since">' + item.created_at + '</td>';
           var whichRow = $(item.url).parents('tr');
           whichRow.html(row);
        }

        function addItem(item) {
             var row = '<tr><td class="rank">' + item.position + '</td><td class="headline"><a href="' + item.url + '" title="' + item.title + '">' + item.title + '</a></td><td class="category"><a href="' + item.feed_url + '" title="' + item.category + '">' + item.category + '</a></td><td class="since">' + item.created_at + '</td></tr>';
             $('table').prepend(row);
        }

        function removeItem(item) {
           var row = $(item.url).parents('tr');
           row.remove();
        }

        function checkFeed() {
          checkFeedTimer = window.setInterval(function() {
            fetchData();
          }, checkFeedTime);
        }

        function startNotify() {

          if (window.webkitNotifications.checkPermission() == 0) {
              //console.log("Permission + Notifications are supported!");
              chromeNotify = true;
          } else {
              //console.log("Notifications are not supported for this Browser/OS version yet." );
              window.webkitNotifications.requestPermission();
          }
        }

        function stopNotify(){
            chromeNotify = false;
            //window.clearInterval(checkFeedTimer);
        }

         $(document).ready(function(){
            //initialise with those already on the page
            currentNotifications.push($('a').attr('href'));

            checkFeed();

            $('#start').click(function(event) {
                event.stopPropagation();
                startNotify();
            });

            $('#stop').click(function(event) {
                event.stopPropagation();
                stopNotify();
            });

        });
      

