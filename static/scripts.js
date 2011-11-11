        var chromeNotify = false;

        var currentNotifications = [];

        var notifications = {};
        
        //var url = "http://news-alertomatic.appspot.com/data.json";
        var url = "http://headline-alertomatic.appspot.com/data.json";
        //var url = "http://localhost:9521/data.json";

        var checkFeedTimer;
        var checkFeedTime = 60000; // 1 minute - 60000;
        var dismissNotification = 300000; // 5 minutes


        function createNotificationInstance(options) {
          if (options.notificationType == 'simple') {
            //console.log("notify simple");
            return window.webkitNotifications.createNotification('', options.title, options.message);
          } else if (options.notificationType == 'html') {
            //console.log("notify html " + options.data);
            return window.webkitNotifications.createHTMLNotification('FileName');
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
                        console.log(this.title + " has been removed");
                        var itemToRemove = notifications[this];

                        // send notification to user
                        if(chromeNotify) {
                            msgUser(itemToRemove, "Disappeared");
                        }

                        removeItem(this);

                        currentNotifications = currentNotifications.filter(this);
            
                    }
                  });

                  // add new item
                  $.each(result, function(item) {

                    // if you haven't seen it before
                    if ($.inArray(this.url, currentNotifications) == -1){
                        //console.log(this.title + " has been added");
                        // send notification to user
                        if(chromeNotify) {
                            msgUser(this, "Appeared");
                        }

                      // track notification
                      currentNotifications.push(this.url);
                           
                      trackNotification(this);
                     
                      addItem(this);

                    // if you have seen it before - update it
                    } else {
                        console.log(this.title + " has been updated");
                        updateItem(this);
                        
                    }

                  });

                  updateTime(data.lastModified);

              },
              error: function(){
                  $('error').html("Sorry we couldn't update this time...");
              }
            });
        }

        function getNotification(url) {
            return notifications[url];
        }

        function trackNotification(item){
            if(!notifications.has(item.url)){
                notifications[item.url] = item;
            }
        }

        function updateTime(time) {
            $('.time').html(time);
        }

        function updateItem(item) {
           var url = item.url;
           var currentItem = getNotification(url);

           var newPosition = item.position;
           var newCategory = item.category;


           var whichRow = $('a[href$="'+ url +'"]').parents('tr');

         /*  if (newPosition !== currentItem.position || newCategory !== currentItem.category) {
            currentItem.position = newPosition;
            currentItem.category = newCategory;
            // replace row, but in future should show changes to user
            removeItem(item);
            addItem(item);
           }*/

        }

        function addItem(item) {
             var row = '<tr><td class="rank">' + item.position + '</td><td class="headline"><a href="' + item.url + '" title="' + item.title + '">' + item.title + '</a></td><td class="category"><a href="' + item.feed_url + '" title="' + item.category + '">' + item.category + '</a></td><td class="since">' + item.created_at + '</td></tr>';
             $('tbody').prepend(row);
        }

        function removeItem(item) {
           var row = $('a[href$="'+ item.url +'"]').parents('tr');
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
            window.clearInterval(checkFeedTimer);
        }

        

