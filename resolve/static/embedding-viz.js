// Embedding Visualization for Article Headers
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

class EmbeddingVisualization {
  constructor(container, pageId) {
    this.container = container;
    this.pageId = pageId;
    this.nodes = [];
    this.svg = null;
    this.width = 0;
    this.height = 0;
    this.padding = 20;
  }

  async init() {
    await this.fetchData();
    if (this.nodes.length === 0) {
      this.container.remove();
      return;
    }
    this.createSvg();
    this.render();
    this.setupResize();
  }

  async fetchData() {
    try {
      const response = await fetch(`/api/articles/${this.pageId}/embeddings/`);
      if (!response.ok) return;
      const data = await response.json();
      this.nodes = data.nodes || [];
    } catch (e) {
      console.warn("Failed to load embedding data:", e);
    }
  }

  createSvg() {
    const rect = this.container.getBoundingClientRect();
    this.width = rect.width;
    this.height = rect.height;

    this.svg = d3
      .select(this.container)
      .append("svg")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("viewBox", `0 0 ${this.width} ${this.height}`)
      .attr("preserveAspectRatio", "xMidYMid meet");

    // Add gradient definitions for node colors
    const defs = this.svg.append("defs");

    // Gradient from start (blue) to end (orange)
    const gradient = defs
      .append("linearGradient")
      .attr("id", "nodeGradient")
      .attr("x1", "0%")
      .attr("y1", "0%")
      .attr("x2", "100%")
      .attr("y2", "0%");

    gradient.append("stop").attr("offset", "0%").attr("stop-color", "#4A90A4");

    gradient.append("stop").attr("offset", "100%").attr("stop-color", "#E07A5F");
  }

  getNodeColor(position) {
    // Interpolate between colors based on position in article
    const startColor = d3.rgb("#4A90A4"); // Muted blue
    const endColor = d3.rgb("#E07A5F"); // Terra cotta
    return d3.interpolateRgb(startColor, endColor)(position);
  }

  render() {
    if (!this.svg || this.nodes.length === 0) return;

    const xScale = d3
      .scaleLinear()
      .domain([0, 1])
      .range([this.padding, this.width - this.padding]);

    const yScale = d3
      .scaleLinear()
      .domain([0, 1])
      .range([this.padding, this.height - this.padding]);

    // Clear existing content
    this.svg.selectAll("g").remove();

    const g = this.svg.append("g");

    // Draw edges between nearby nodes (in embedding space, not document order)
    const edges = this.computeEdges();
    g.selectAll("line")
      .data(edges)
      .enter()
      .append("line")
      .attr("x1", (d) => xScale(d.source.x))
      .attr("y1", (d) => yScale(d.source.y))
      .attr("x2", (d) => xScale(d.target.x))
      .attr("y2", (d) => yScale(d.target.y))
      .attr("stroke", "#D5D5D5")
      .attr("stroke-width", 1)
      .attr("stroke-opacity", 0.4);

    // Draw nodes
    const nodeGroups = g
      .selectAll("g.node")
      .data(this.nodes)
      .enter()
      .append("g")
      .attr("class", "node")
      .attr("transform", (d) => `translate(${xScale(d.x)}, ${yScale(d.y)})`);

    // Node circles
    nodeGroups
      .append("circle")
      .attr("r", 12)
      .attr("fill", (d) => this.getNodeColor(d.position))
      .attr("stroke", "#fff")
      .attr("stroke-width", 2)
      .style("cursor", "pointer");

    // Tooltips on hover
    const tooltip = d3
      .select("body")
      .append("div")
      .attr("class", "embedding-tooltip")
      .style("position", "absolute")
      .style("visibility", "hidden")
      .style("background", "rgba(0, 0, 0, 0.8)")
      .style("color", "#fff")
      .style("padding", "8px 12px")
      .style("border-radius", "4px")
      .style("font-size", "12px")
      .style("max-width", "250px")
      .style("pointer-events", "none")
      .style("z-index", "1000");

    nodeGroups
      .on("mouseenter", (event, d) => {
        d3.select(event.currentTarget).select("circle").attr("r", 16);
        tooltip.style("visibility", "visible").text(d.text);
      })
      .on("mousemove", (event) => {
        tooltip
          .style("top", event.pageY - 10 + "px")
          .style("left", event.pageX + 10 + "px");
      })
      .on("mouseleave", (event) => {
        d3.select(event.currentTarget).select("circle").attr("r", 12);
        tooltip.style("visibility", "hidden");
      });

    // Animate nodes fading in
    nodeGroups.style("opacity", 0).transition().duration(500).style("opacity", 1);
  }

  computeEdges() {
    // Connect nodes that are close in embedding space (using Euclidean distance)
    const edges = [];
    const threshold = 0.15; // Distance threshold for edge creation

    for (let i = 0; i < this.nodes.length; i++) {
      for (let j = i + 1; j < this.nodes.length; j++) {
        const dx = this.nodes[i].x - this.nodes[j].x;
        const dy = this.nodes[i].y - this.nodes[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < threshold) {
          edges.push({
            source: this.nodes[i],
            target: this.nodes[j],
          });
        }
      }
    }

    return edges;
  }

  setupResize() {
    const resizeObserver = new ResizeObserver(() => {
      requestAnimationFrame(() => {
        const rect = this.container.getBoundingClientRect();
        this.width = rect.width;
        this.height = rect.height;
        this.svg.attr("viewBox", `0 0 ${this.width} ${this.height}`);
        this.render();
      });
    });
    resizeObserver.observe(this.container);
  }
}

// Initialize on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".embedding-viz");
  if (!container) return;

  const pageId = container.dataset.pageId;
  if (!pageId) return;

  const viz = new EmbeddingVisualization(container, pageId);
  viz.init();
});
