// Ajax/jQuery functions

function showTitles(search_input) {
    var search_input = search_input;
    $('#search').html()
}

function getTitles() {
    $.get('/dashboard/<user_id>', showTitles);
}

$('#search').on('submit', getTitles)