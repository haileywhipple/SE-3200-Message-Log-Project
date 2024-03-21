console.log("connected")

var buttons = document.getElementsByTagName("button");
for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", (event) => {
        const button = event.target
        if (button.className == "path") {
            button.className += ' clicked'
        } else if (button.className == "path clicked") {
            button.className = "path"
        }
    });
}

var generate = document.getElementById('generate');
var complete = document.getElementById('complete');
var check = document.getElementById('check');
var logout = document.getElementById('logout');

function showSolvedMaze(data) {
    var mae = document.getElementById('maze');
    var length = mae.children.length;

    while (mae.hasChildNodes()) {
        mae.removeChild(mae.firstChild);
    }

    var row = 0;
    var div = document.createElement('div');
    div.className = 'rows';
    console.log(data)
    for(let i = 0; i < data.length; i++) {
        var button = document.createElement('button');
        if (data[i] == 'path clicked') {
            data[i] = 'path';
        }

        button.className = data[i];
        button.type = 'button';
        div.appendChild(button);
        row += 1;
        if (row == length-1) {
            row = 0;
            mae.appendChild(div);
            div = document.createElement('div');
            div.className = 'rows';
        }
    }

    console.log(mae)
}

function generateMaze() {
    generatePressed = false;
    var maze = document.getElementById('maze');
    maze = maze.childNodes;

    var li = ['generate', document.getElementById('username_nav').innerHTML];

    for(let mazeChild = 0; mazeChild < maze.length; mazeChild++) {
        var child = maze[mazeChild];
        if (child.className == 'rows') {
            child = child.childNodes;
            for(let i = 0; i < child.length; i++) {
                var but = child[i];
                if (but.nodeType == 1) {
                    li.push(but.className);
                }
            }
            li.push('\n');
        }
    }

    var data = "name=" + encodeURIComponent(li);
    fetch("http://localhost:5000/maze", {
        method: "POST", 
        body: data,
        redirect: "follow",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        }).then(function(response){
            window.location.reload();
        })
}

function completeMaze() {
    var maze = document.getElementById('maze');
    maze = maze.childNodes;

    var li = ['complete', document.getElementById('username_nav').innerHTML];

    for(let mazeChild = 0; mazeChild < maze.length; mazeChild++) {
        var child = maze[mazeChild];
        if (child.className == 'rows') {
            child = child.childNodes;
            for(let i = 0; i < child.length; i++) {
                var but = child[i];
                if (but.nodeType == 1) {
                    li.push(but.className);
                }
            }
            li.push('\n');
        }
    }

    var data = "name=" + encodeURIComponent(li);
    fetch("http://localhost:5000/maze", {
        method: "POST", 
        body: data,
        redirect: "follow",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        }).then(function(response){
            console.log(response)
        })

    fetch("http://localhost:5000/completemaze")
        .then(function(response){
            console.log(response)
            response.json()
            .then(function(data){
                console.log(data);
                showSolvedMaze(data);
            })
        })
}

function checkMaze() {
    var maze = document.getElementById('maze');
    maze = maze.childNodes;

    var li = ['check', document.getElementById('username_nav').innerHTML];

    for(let mazeChild = 0; mazeChild < maze.length; mazeChild++) {
        var child = maze[mazeChild];
        if (child.className == 'rows') {
            child = child.childNodes;
            for(let i = 0; i < child.length; i++) {
                var but = child[i];
                if (but.nodeType == 1) {
                    li.push(but.className);
                }
            }
            li.push('\n');
        }
    }

    var data = "name=" + encodeURIComponent(li)
    console.log(data)
    fetch("http://localhost:5000/maze", {
        method: "POST", 
        body: data,
        redirect: "follow",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        }).then(function(response){
            response.json()
            .then(function(data){
                console.log(data);
                if (data['value'] == 'success') {
                    window.alert('Congratulations! You have completed the maze successfully!');
                    fetch("http://localhost:5000/maze");
                    window.location.reload();
                } else {
                    window.alert('You have not completed the maze.');
                }
            })
        })
}

function logoutMaze() {
    window.location.replace("http://localhost:5000/");
    document.cookie.split(';').forEach(function(c) {
        document.cookie = c.trim().split('=')[0] + '=;' + 'expires=Thu, 01 Jan 1970 00:00:00 UTC;';
    });
}

if (window.location != "http://localhost:5000/") {
    generate.onclick = generateMaze;
    complete.onclick = completeMaze;
    check.onclick = checkMaze;
    logout.onclick = logoutMaze;

    window.addEventListener('beforeunload', function (e) {

        // Cancel the event
        e.preventDefault();
        e.returnValue = '';
    });
}