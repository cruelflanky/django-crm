// Call the dataTables jQuery plugin
$(document).ready(function() {
	var $form = $(this);
	$('#create_profile_form').hide();

	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			const cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	const csrftoken = getCookie('csrftoken');

	$('#dataTableTeam').DataTable( {
	});

	$('#dataTable').DataTable( {
		searchPanes: {
			layout: 'columns-2',
			columns: [2,4]
		},
		dom: 'Plfrtip',
	});

	$('#dataTableDubli').DataTable({
		searchPanes: {
			layout: 'columns-6'
		},
		dom: 'Plfrtip',
		columnDefs: [
			{
				searchPanes: {
					show: true
				},
				targets: [0, 1, 2, 3, 4, 5]
			}
		]
	});

	$('#dataTableOrder').DataTable( {
		dom: 'Plfrtip',
		columnDefs: [
			{
				searchPanes: {
					show: true
				},
				targets: [1]
			},
			{
				searchPanes: {
					show: false
				},
				targets: [5]
			}
		]
	});

	var table = $('#dataTable1').DataTable({
		dom: 'Bfrtip',
		select: {
			style: 'multi'
		},
		buttons: [
			{
				text: 'Перепривязать выделенные',
				action: function () {
					var data = {};
					data["csrfmiddlewaretoken"] = csrftoken;
					var select = table.rows( { selected: true } );

					for (row in select.data()){
						if ($.isNumeric(row)){
							data[select.data()[row][0]] = select.data()[row][0];
						}
					}
					console.log(data);
					var url = "/relink_shops/";
					$.ajax({
						url: url,
						type: 'POST',
						data: data,
						cache: true,
						success: function (data) {
							console.log("OK");
							$('#shop_table').hide();
							$('#create_shop').hide();
							$('#create_team_form').hide();
							$('#form_show').removeAttr('hidden');
							$("#id_shops").val(data["shops"]);
							console.log(data);
						},
						error: function (){
							console.log("error");
						}
					})
				}
			},
			{
				extend: 'searchPanes',
				config: {
					cascadePanes: true
				}
			}
		],
	});
});
