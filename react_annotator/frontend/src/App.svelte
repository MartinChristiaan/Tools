<script>
  let squares = [];
  let selectedSquare = null;
  let startX, startY, startWidth, startHeight;

  function handleMouseDown(event, index) {
    const { clientX, clientY } = event;
    selectedSquare = squares[index];
    startX = clientX;
    startY = clientY;
    startWidth = selectedSquare.width || 50; // Set initial width if not present
    startHeight = selectedSquare.height || 50; // Set initial height if not present
  }

  function handleMouseMove(event) {
    if (selectedSquare) {
      const { clientX, clientY } = event;
      const deltaX = clientX - startX;
      const deltaY = clientY - startY;

      selectedSquare.width = startWidth + deltaX;
      selectedSquare.height = startHeight + deltaY;
    }
  }

  function handleMouseUp() {
    selectedSquare = null;
  }
</script>

<style>
  .canvas {
    position: relative;
    width: 1920px;
    height: 1080px;
    border: 1px solid #ccc;
    background-color: red;
    top: 0px;
    left: 0px;
  }

  .square {
    position: absolute;
    background-color: #3498db;
    cursor: pointer;
  }
</style>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="canvas" on:mousedown={handleMouseDown} on:mousemove={handleMouseMove} on:mouseup={handleMouseUp}>
  {#each squares as { x, y, width, height }, index (index)}
    <div bind:this={squares[index]} class="square" style="left:{x}px; top:{y}px; width:{width}px; height:{height}px;"></div>
  {/each}
</div>

