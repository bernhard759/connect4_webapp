<script>
  import { onMount } from "svelte";
  import {
    Button,
    Card,
    CardBody,
    CardTitle,
    Container,
    Row,
    Col,
  } from "sveltestrap";
  import "./styles/gamestyle.css";

  // Variables
  let board = Array(6)
    .fill()
    .map(() => Array(7).fill(0)); // 6x7 grid
  let dropToken = null;
  let canPlay = true;
  let dropDiv;
  let dropDivSize = {};
  let theWidth = 0;
  let winner = null;
  let draw = false;
  let scores = [0, 0, 0, 0, 0, 0, 0];
  let playerColor = "red";
  let errorMessage = "";
  const apiBaseUrl =
    window.location.hostname === "localhost"
      ? "http://localhost:5000"
      : window.location.origin;

  //----------------------------------
  // Setup
  //----------------------------------

  // Fetch initial game state
  onMount(async () => {
    await startGame();
    updateDropDivSize();
    window.addEventListener("resize", updateDropDivSize);
    // Cleanup
    return () => {
      window.removeEventListener("resize", updateDropDivSize);
    };
  });

  // Start a new game
  async function startGame() {
    winner = null;
    canPlay = true;
    draw = false;
    errorMessage = ""
    console.log("init game state");
    console.log(board);
    const response = await fetch(`${apiBaseUrl}/init_game`, { method: "POST" });
    board = await response.json();
    console.log(board);
  }

  //----------------------------------
  // Token drag and drop
  //----------------------------------

  // Update size of the dropdiv area
  function updateDropDivSize() {
    if (dropDiv) {
      dropDivSize = dropDiv.getBoundingClientRect();
    }
  }

  // Pointerdown create game token
  function handlePointerDown(event) {
    createToken(event.offsetX);
  }

  // Token creation
  function createToken(offsetX) {
    theWidth = dropDivSize.width / 9;
    dropToken = {
      left: `${offsetX - theWidth / 2}px`,
      color: playerColor,
      width: theWidth,
      height: theWidth,
    };
  }

  // Pointer move moves token
  function handlePointerMove(event) {
    if (dropToken) {
      const newposX = event.clientX - dropDivSize.left - theWidth / 2;
      if (newposX > 0 && newposX < dropDivSize.width - theWidth) {
        dropToken.left = `${newposX}px`;
      }
    }
  }

  // Token drop
  async function handlePointerUp(event) {
    if (dropToken) {
      const newposX = event.clientX - dropDivSize.left;
      let column = Math.floor(newposX / (dropDivSize.width / 7));
      dropToken = null;

      // Column check
      if (column >= 0 && column < 7) {
        // Player move
        if (!(await playerMove(column))) {
          return;
        }
        if (winner) return;
        canPlay = false;

        // AI move
        await aiMove();
        if (winner) return;
        canPlay = true;
      }
    }
  }

  //----------------------------------
  // Moves
  //----------------------------------

  // Player move
  async function playerMove(column) {
    errorMessage = ""
    try {
      const response = await fetch(`${apiBaseUrl}/player_move`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ column }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        errorMessage = errorData.error || "An error occurred";
        return;
      }
      board = await response.json();

      // Check game status
      winner = await checkGameStatusWinner();
      draw = await checkGameStatusDraw();
      return true;
    } catch (error) {
      errorMessage = "Failed to make move. Please try again.";
      console.error("Error during player move:", error);
      return false;
    }
  }

  // AI move
  async function aiMove() {
    const response = await fetch(`${apiBaseUrl}/ai_move`, { method: "POST" });
    const data = await response.json();

    // Update the board with the new state from the AI move
    board = data.board;

    // Update scores array with the actual scores returned from the server
    scores = Array(7).fill(null);
    data.scores.forEach(([column, score]) => {
      scores[column] = score;
    });

    // Check game status
    winner = await checkGameStatusWinner();
    draw = await checkGameStatusDraw();
  }

  //----------------------------------
  // Checks
  //----------------------------------

  // Check winner
  async function checkGameStatusWinner() {
    console.log("checking winner");
    // Check game status
    const statusResponse = await fetch(
      `${apiBaseUrl}/check_game_status_winner`,
      {
        method: "GET",
      }
    );
    if (statusResponse.ok) {
      let winStatus = await statusResponse.json();
      console.log(winStatus.status);
      return winStatus.status != null;
    } else {
      console.error("Failed to check game status:", statusResponse.status);
      return undefined;
    }
  }

  // Check draw
  async function checkGameStatusDraw() {
    console.log("checking draw");
    // Check game status
    const statusResponse = await fetch(`${apiBaseUrl}/check_game_status_draw`, {
      method: "GET",
    });
    if (statusResponse.ok) {
      let winStatus = await statusResponse.json();
      console.log(winStatus.status);
      return winStatus.status;
    } else {
      console.error("Failed to check game status:", statusResponse.status);
      return undefined;
    }
  }
</script>

<Container>
  <Row>
    <Col md={{ size: 6 }} class="mx-auto">
      <Card>
        <CardBody>
          <h2 class="card-title">Connect 4 game</h2>

          <section class="game">
            <!-- Controls and Info -->
            <div
              class=" mt-2 p-3 d-flex justify-content-between align-items-center"
            >
              <Button color="secondary" on:click={startGame} class="mt-2"
                >Reset Game</Button
              >
              {#if winner}
                <div class="alert alert-info p-1 mt-2 mb-0">{canPlay ? "You" : "AI"} won the game</div>
              {/if}
              {#if draw}
                <div class="alert alert-info -1 mt-2 mb-0">This game is a draw!</div>
              {/if}
              {#if !winner}
              <span class="badge bg-info text-dark"
                >{canPlay ? "Your turn" : "AI turn"}</span
              >
              {/if}
            </div>
            <!-- Game -->
            <div class="gamediv mt-2">
              {#if errorMessage}
                <div class="alert alert-danger mx-4">{errorMessage}</div>
              {/if}
              <!-- Dropzone -->
              <div
                class="dropdiv {canPlay && !winner ? '' : 'no-hover'}"
                bind:this={dropDiv}
                on:pointerdown={canPlay && !winner ? handlePointerDown : null}
                on:pointermove={canPlay && !winner ? handlePointerMove : null}
                on:pointerup={canPlay && !winner ? handlePointerUp : null}
              >
                {#if dropToken}
                  <div
                    class="droptoken {dropToken.color}"
                    style="position: absolute; left: {dropToken.left}; width: {dropToken.width}px; height: {dropToken.height}px;"
                  ></div>
                {/if}
              </div>
              <!-- Gameboard -->
              <div class="gameboard mt-3">
                {#each board as row}
                  {#each row as cell}
                    <div class="field" data-field={cell}></div>
                  {/each}
                {/each}
              </div>
              <!-- Scores -->
                <div class="minimax-scores minimax" style="display: {canPlay ? "grid" : "grid"};">
                  {#each scores as score, index}
                    <div
                      class="score-col-{index + 1} badge {index ==
                      scores.indexOf(Math.max(...scores))
                        ? 'bg-success'
                        : 'bg-secondary'}"
                    >
                      {score != null ? score : "-"}
                    </div>
                  {/each}
                </div>
            </div>
          </section>
        </CardBody>
      </Card>
    </Col>
  </Row>
</Container>

<style>
</style>
