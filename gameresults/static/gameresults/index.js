document.addEventListener('DOMContentLoaded', function() {
    
    // code for index page
    if (document.getElementById("index") != null) {

        // get list of all users for player selection
        fetch(`/players`)
        .then(response => response.json())
        .then(players => {
            createResult(players);
        });

    };
    
})

function createResult (players) {

    // display winner select options
    var instance_winners = new SelectPure(".select-pure-winners", {
        options: players,
        multiple: true,
        autocomplete: true,
        icon: "fa fa-times",
        onChange: value => {
            console.log(`winners: ${value}`)
            validatePlayers(value, document.getElementById("winners_validate"), 0);
        }
    });

    // add "select all" option to players select
    players.unshift({label: "select all", value: "0"});

    let player_list = [] // keep track of players in array

    // display player select
    var instance_players = new SelectPure(".select-pure-players", {
        options: players,
        multiple: true,
        autocomplete: true,
        icon: "fa fa-times",
        onChange: value => {
            // update player_list with value
            player_list = value;
            // if Select All is chosen, all players are added to value
            if (value.indexOf("0") != -1) {
                player_list = []
                for (i in players) {
                    player_list.push(players[i].value);
                };
                player_list.shift(); // remove "select all" from value
                value = player_list;
            }
            console.log(`players: ${player_list}`)
            // validate player selection
            validatePlayers(player_list, document.getElementById("players_validate"), 0);
        }
    });

    // on Submit Result, send result details to view
    document.getElementById("submit-result").addEventListener('click', function() {

        var game_selection = document.getElementById("id_game")
        var game_value = parseInt(game_selection.options[game_selection.selectedIndex].value);

        var game_valid = validateGame(game_value, document.getElementById("game_validate"))
        var players_valid = validatePlayers(player_list, document.getElementById("players_validate"), 1)
        var winners_valid = validatePlayers(instance_winners.value(), document.getElementById("winners_validate"), 0)

        if (game_valid !=false && players_valid != false && winners_valid != false) {
            fetch(`/addresult`, {
                method: 'POST',
                body: JSON.stringify({
                    players: player_list,
                    winner: instance_winners.value(),
                    game: game_value
                })
            })
            .then(response => response.json())
            location.reload();
            console.log("created result");
            return false;
        }
    })
}

function validatePlayers (input, output, player_len) {

    if (typeof input !== 'undefined' && input.length > player_len) {
        console.log("validated players")
    } else {
        console.log("players not selected");

        // toggle error visibility
        if (output.style.display === "none") {
            output.style.display = "block";
          } else {
            output.style.display = "none";
          }
        return false;
    }
}

function validateGame (input, output) {
    if (input > -1) {
        console.log("validated game")
    } else {
        console.log("game not selected");
        console.log(input)

        // toggle error visibility
        if (output.style.display === "none") {
            output.style.display = "block";
          } else {
            output.style.display = "none";
          }
        return false;
    }
}