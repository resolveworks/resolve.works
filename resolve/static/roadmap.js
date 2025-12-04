// D3 Animated Arrow for Process Roadmap
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

const draw_arrow = function (container, index) {
  const svg = d3
    .select(container)
    .select(`ol > li:nth-child(${index})`)
    .append("svg");

  const width = svg.node().getBoundingClientRect().width;
  const height = svg.node().getBoundingClientRect().height;

  let startX, startY, endX, endY, controlX, controlY;

  if (index === 2) {
    // Top right to bottom left
    startX = width * 0.4;
    startY = height * 0.12;
    controlY = startY;
    endX = width * 0.75;
    endY = height * 0.6;
    controlX = startX + (endX - startX) * 0.75;
  } else {
    // Bottom left to top right
    startX = width * 0.2;
    startY = height * 0.55;
    endX = width * 0.6;
    endY = height * 0.8;
    controlY = endY;
    controlX = startX + (endX - startX) * 0.25;
  }

  const path = svg
    .append("path")
    .attr("d", `M${startX},${startY} Q${controlX},${controlY} ${endX},${endY}`)
    .attr("stroke", "#D5D5D5")
    .attr("stroke-width", 2)
    .attr("fill", "none");

  const totalLength = path.node().getTotalLength();

  path
    .attr("stroke-dasharray", totalLength + " " + totalLength)
    .attr("stroke-dashoffset", totalLength);

  return svg.node();
};

const drawSVGs = (container, intersectionObserver) => {
  const mediaQuery = window.matchMedia("(min-width: 1024px)");

  if (mediaQuery.matches) {
    [1, 2, 3].forEach((i) => {
      const svg = draw_arrow(container, i);
      intersectionObserver.observe(svg);
    });
  } else {
    d3.select(container).selectAll("ol > li > svg").remove();
  }
};

document.addEventListener("DOMContentLoaded", () => {
  // Find all process roadmap sections (sections with ol elements)
  const processRoadmapSections = document.querySelectorAll(".section > ol");

  processRoadmapSections.forEach((ol) => {
    const container = ol.parentElement;

    const intersectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const svg = entry.target;

            const path = d3.select(svg).select("path");
            path.transition().duration(1000).attr("stroke-dashoffset", 0);
            intersectionObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 1 },
    );

    const resizeObserver = new ResizeObserver(() => {
      requestAnimationFrame(() => {
        d3.select(container).selectAll("ol > li > svg").remove();
        drawSVGs(container, intersectionObserver);
      });
    });

    // Initial draw
    drawSVGs(container, intersectionObserver);

    // Observe the container for resize
    if (ol) resizeObserver.observe(ol);
  });
});
