let products = [
{
	'id' : 1,
	'price' : 3.99,
	'pic' : 1,
	'name': 'Honey Bee',
	'desc' : 'Lvl-1 Chat'
},
{
	'id' : 2,
	'price' : 6.99,
	'pic' : 2,
	'name': 'Silver bee',
	'desc' : 'Lvl-2 Chat'
},
{
	'id' : 3,
	'price' : 9.99,
	'pic' : 3,
	'name': 'Queen Bee',
	'desc' : 'Lvl-3 Chat'
},
{
	'id' : 4,
	'price' : 2.99,
	'pic' : 4,
	'name': 'Jade Wasp',
	'desc' : 'Lvl-1 Messenger'
},
{
	'id' : 5,
	'price' : 4.99,
	'pic' : 5,
	'name': 'Ruby Wasp',
	'desc' : 'Lvl-2 Messenger'
},
{
	'id' : 6,
	'price' : 6.99,
	'pic' : 6,
	'name': 'Purple Hornet',
	'desc' : 'Lvl-3 Messenger'
}
]


function display_prods(lm, rm) {
    document.querySelector('.prod_view').style.display = 'none';
    document.querySelector('.prod_image').innerHTML = '';
    document.querySelector('.prod_info').innerHTML = '';

    document.getElementById('p_table').style.display = 'grid';

	document.getElementById('p_table').innerHTML = '';

	for (let j=0; j < (products.length/3); j++){

	for (let i=0; i<3; i++){
		if ( lm <= (i+j*3) && (i+j*3) < rm) {
		document.getElementById('p_table').innerHTML += "<td id='p" + String(i+j*3) + "' onclick='inspect_prod(" + String(i+j*3) + ");'" + ">" + '<h2>' + products[i+j*3]['name'] + '</h2>' + "<img src='/media/img/prods/" + products[i+j*3]['pic'] + ".png' />" + '<p>'+ products[i+j*3]['desc'] + '</p><br>' +
		'<p>'+ products[i+j*3]['price'] + '$ </p>' +
		"<div class='button-order'style='margin: 10px;'>Purchase</div>" + '</td>';
		}
	}

}
	for (let j=0; j < products.length/3; j++){
		var row = document.getElementById(j);
		if (row.innerHTML === ''){
			row.parentNode.removeChild(row);
		}
	}

}


function inspect_prod(id) {

	document.getElementById('p_table').style.display = 'none';
	document.querySelector('.prod_info').innerHTML += '<h2>' + products[id]['name'] + '</h2>' + '<p>'+ products[id]['desc'] + '</p><br>' +
		'<p>'+ products[id]['price'] + '$ </p>' +
		"<div class='b_pack'><div class='button-order back'style='margin: 10px;' onclick='hide_view();'>Back</div>" + "<div class='button-order'style='margin: 10px;'>Purchase</div></div>";
	document.querySelector('.prod_image').innerHTML += "<img src='/media/img/prods/" + products[id]['pic'] + ".png' />";
	document.querySelector('.prod_view').style.display = 'flex';
}

function hide_view() {
    document.querySelector('.prod_view').style.display = 'none';
    document.querySelector('.prod_image').innerHTML = '';
    document.querySelector('.prod_info').innerHTML = '';

    document.getElementById('p_table').style.display = 'grid';

}



for (let i=0; i < 3; i++){
    document.getElementById('c'+String(i)).onclick = () => {
    switch(i){
            case 0:
                display_prods(0, products.length);
                break;
            case 1:
                display_prods(0, 3);
                break;
            case 2:
                display_prods(3, products.length);
                break;
        }
    }


}

