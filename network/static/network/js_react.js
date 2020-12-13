
document.addEventListener("DOMContentLoaded", function(event) {
    console.log("DOM fully loaded and parsed");
    render_content();
  });

// Global variables
let pagination_counter = 1;
let start = 0;
let finish = 10;

// Create post interface on profile

// Render posts
function render_content() {
    fetch('http://127.0.1:8000/api', {method: 'GET'})
    .then(function(response){
        return response.json();
    })
    .then(response => {
        let all_posts = response;
        let count_elements = response.length;
        call_pagination(count_elements, all_posts);
        render_element();
        likes_in_post(count_elements);
    })
}
// Clear post info after rendering
function clear_post_info() {
    post_info.splice(0, post_info.length);
}
// Pagination
function call_pagination(count_elements, all_posts) {
    let posts_left = count_elements -= start;
    if (posts_left < 10) {
        count_elements += start;
        document.getElementById('next_btn').style.display = 'none';
        console.log(start);
        console.log(count_elements);
        for (i = start; i < count_elements; i++) {
            let data = all_posts[i];
            console.log(data);
            console.log(posts_left);
            save_data(data);
        }
    }
    else if (posts_left >= 10) {
        for (i = start; i < finish; i++) {
            let data = all_posts[i];
            console.log(data);
            save_data(data);
        }
    }
    else {
        save_data('error');
    }
}
// Next page
function next() {
    pagination_counter++;
    start += 10;
    finish += 10;
    document.getElementById('page_counter').innerText = pagination_counter;
    document.getElementById('previous_btn').setAttribute('class', 'btn btn-light');
    clear_post_info();
    render_content();
}
// Previous page
function previous() {
    document.getElementById('next_btn').style.display = "block";
    clear_post_info();
    if (pagination_counter <= 1) {
        document.getElementById('previous_btn').setAttribute('class', 'btn btn-light disabled');
    }
    else {
        pagination_counter--;
        start -= 10;
        finish -= 10;
        document.getElementById('page_counter').innerText = pagination_counter;
        render_content();
        if (pagination_counter <= 1) {
            previous();
        }
    }
}

// Display liked post button different
function likes_in_post(count_elements) {
    for(p = 0; p < count_elements; p++ ){
        let id = post_info[p]['id']
        let user_in_session = document.getElementById('user_in_session').innerHTML;
        let get_likes_in_post = document.getElementById(id).querySelector('.usr_interaction').querySelector('.like_btn').getAttribute('data-likes');
        if (get_likes_in_post.split(',').includes(user_in_session)) {
            let like_btnn = document.getElementById(id).querySelector('.usr_interaction').querySelector('.like_btn');
            like_btnn.setAttribute('class', 'btn btn-primary like_btn');
            like_btnn.childNodes[0].textContent = "Liked ";
        }
        else {
            console.log('none');
        }
    }
}

// New like
function new_like(user, id) {
    fetch(`http://127.0.1:8000/api/interaction/${id}`, {
        method: 'PUT',
        body: JSON.stringify({"user": user, "like": true}),
    })
    .then( function(response) {
        return response.json();
    })
    .then(response => {
        alert('Support this user liking more of his posts!');
        window.location.href = `/profile/${response}`;
    })
}

// Like posts
function like(user, id) {
    fetch(`http://127.0.1:8000/api/interaction/${id}`, {
        method: 'PUT',
        body: JSON.stringify({"user": user, "like": true}),
    })
    .then(function(response) {
        return response.json();
    })
    .then(response => {
        let ret = response.split(',').length;
        document.getElementById(id).querySelector('.usr_interaction').querySelector('.like_btn').querySelector('.badge').innerHTML = ret;
        console.log(`Likes in this post ${response}`);
        like_post(id, response);
    })
}

// If the post is liked, the button should display other style
function like_post(id, response) {
        let user_in_session = document.getElementById('user_in_session').innerHTML;
        if (response.split(',').includes(user_in_session)) {
            let like_btnn = document.getElementById(id).querySelector('.usr_interaction').querySelector('.like_btn');
            like_btnn.setAttribute('class', 'btn btn-primary like_btn');
            like_btnn.childNodes[0].textContent = "Liked ";
        }
        else {
            let like_btnn = document.getElementById(id).querySelector('.usr_interaction').querySelector('.like_btn');
            like_btnn.setAttribute('class', 'btn btn-outline-success like_btn');
            like_btnn.childNodes[0].textContent = "Like ";
        }
}
