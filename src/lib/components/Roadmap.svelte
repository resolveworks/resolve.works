<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let { children } = $props();
  let ol;

  const drawArrow = (container, index) => {
    const svg = d3.select(container).select(`ol > li:nth-child(${index})`).append('svg');
    const width = svg.node().getBoundingClientRect().width;
    const height = svg.node().getBoundingClientRect().height;

    // Keep each connector in the whitespace below its step.
    const startX = width * 0.2;
    const startY = height * 0.55;
    const endX = width * 0.6;
    const endY = height * 0.8;
    const controlX = startX + (endX - startX) * 0.25;
    const controlY = endY;

    const path = svg
      .append('path')
      .attr('d', `M${startX},${startY} Q${controlX},${controlY} ${endX},${endY}`)
      .attr('stroke', '#D5D5D5')
      .attr('stroke-width', 2)
      .attr('fill', 'none');

    const totalLength = path.node().getTotalLength();
    path.attr('stroke-dasharray', `${totalLength} ${totalLength}`).attr('stroke-dashoffset', totalLength);

    return svg.node();
  };

  const drawSVGs = (container, intersectionObserver) => {
    if (window.matchMedia('(min-width: 1024px)').matches) {
      [1, 2, 3].forEach((index) => {
        intersectionObserver.observe(drawArrow(container, index));
      });
    } else {
      d3.select(container).selectAll('ol > li > svg').remove();
    }
  };

  onMount(() => {
    const container = ol.parentElement;
    const intersectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            d3.select(entry.target).select('path').transition().duration(1000).attr('stroke-dashoffset', 0);
            intersectionObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 1 }
    );

    const resizeObserver = new ResizeObserver(() => {
      requestAnimationFrame(() => {
        d3.select(container).selectAll('ol > li > svg').remove();
        drawSVGs(container, intersectionObserver);
      });
    });

    drawSVGs(container, intersectionObserver);
    resizeObserver.observe(ol);

    return () => {
      intersectionObserver.disconnect();
      resizeObserver.disconnect();
    };
  });
</script>

<ol bind:this={ol}>
  {@render children()}
</ol>
