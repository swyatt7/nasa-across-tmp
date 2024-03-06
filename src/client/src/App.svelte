<script>
  let rand = -1;

  function getRand() {
    fetch("http://localhost:8000/rand")
    .then(value => value.text())
    .then(value => { rand = value; })
  };
</script>

<h1>Your number is {rand}!</h1>
<button on:click={getRand}>Get a random number</button>
