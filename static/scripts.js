$(document).ready(function(){

var notifier = {
			initialise: function() {

					if (window.webkitNotifications) {
					  console.log("Notifications are supported!");
					}
					else {
					  console.log("Notifications are not supported for this Browser/OS version yet.");
					}

			}

};

notifier.initialise();



			// whole row clickable
      $("tr").click(function(){
         window.location = $(this).find('a').attr('href');
      });
      
      $.ajax({
        type: "GET"
        url : "http://news-alertomatic.appspot.com/data.json",
        dataType: 'json',
        success: function(data){
            console.log(data);
        }
      });
      
// table sorting
    /*  var sorter = new TINY.table.sorter('sorter');
      sorter.head = 'head';
      sorter.init('table',1);*/

});