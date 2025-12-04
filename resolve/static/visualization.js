// Embedding Visualization for Article Headers
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

class EmbeddingVisualization {
  constructor(container, pageId) {
    this.container = container;
    this.pageId = pageId;
    this.nodes = [];
    this.edges = [];
    this.svg = null;
    this.width = 0;
    this.height = 0;
  }

  async init() {
    await this.fetchData();
    if (this.nodes.length === 0) {
      this.container.remove();
      return;
    }
    this.createSvg();
    this.render();
  }

  async fetchData() {
    try {
      const response = await fetch(`/api/pages/${this.pageId}/embeddings/`);
      if (!response.ok) return;
      const data = await response.json();
      this.nodes = data.nodes || [];
      this.edges = data.edges || [];
    } catch (e) {
      console.warn("Failed to load embedding data:", e);
    }
  }

  getBaseSize() {
    return Math.min(this.width, this.height);
  }

  getNodeRadius(z) {
    const baseSize = this.getBaseSize();
    const minRadius = baseSize * 0.0075;
    const maxRadius = baseSize * 0.025;
    return minRadius + z * (maxRadius - minRadius);
  }

  getStrokeWidth() {
    return this.getBaseSize() * 0.002;
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

  }

  getNodeColor(position) {
    // Interpolate between colors based on position in article
    const startColor = d3.rgb("#4A90A4"); // Muted blue
    const endColor = d3.rgb("#E07A5F"); // Terra cotta
    return d3.interpolateRgb(startColor, endColor)(position);
  }

  render() {
    if (!this.svg || this.nodes.length === 0) return;

    // Calculate padding to ensure nodes with strokes stay within bounds
    const maxRadius = this.getNodeRadius(1); // z=1 gives max radius
    const strokeWidth = this.getStrokeWidth();
    const padding = maxRadius + strokeWidth / 2;

    const xScale = d3
      .scaleLinear()
      .domain([0, 1])
      .range([padding, this.width - padding]);

    const yScale = d3
      .scaleLinear()
      .domain([0, 1])
      .range([padding, this.height - padding]);

    // Clear existing content
    this.svg.selectAll("g").remove();

    const g = this.svg.append("g");

    // Build node lookup for edges
    const nodeById = new Map(this.nodes.map((n) => [n.id, n]));

    // Draw edges using precomputed similarities
    g.selectAll("line")
      .data(this.edges)
      .enter()
      .append("line")
      .attr("x1", (d) => xScale(nodeById.get(d.source).x))
      .attr("y1", (d) => yScale(nodeById.get(d.source).y))
      .attr("x2", (d) => xScale(nodeById.get(d.target).x))
      .attr("y2", (d) => yScale(nodeById.get(d.target).y))
      .attr("stroke-width", this.getStrokeWidth());

    // Draw nodes (sorted by z so larger nodes appear in front)
    const sortedNodes = [...this.nodes].sort((a, b) => a.z - b.z);
    const nodeGroups = g
      .selectAll("g.node")
      .data(sortedNodes)
      .enter()
      .append("g")
      .attr("class", "node")
      .attr("transform", (d) => `translate(${xScale(d.x)}, ${yScale(d.y)})`);

    // Node circles with z-based radius
    nodeGroups
      .append("circle")
      .attr("r", (d) => this.getNodeRadius(d.z))
      .attr("fill", (d) => this.getNodeColor(d.position))
      .attr("stroke-width", this.getStrokeWidth());

    // Tooltips on hover
    let tooltip = null;

    nodeGroups
      .on("mouseenter", (event, d) => {
        d3.select(event.currentTarget)
          .select("circle")
          .attr("r", this.getNodeRadius(d.z) + 4);
        tooltip = d3
          .select("body")
          .append("div")
          .attr("class", "tooltip")
          .style("top", event.clientY - 10 + "px")
          .style("left", event.clientX + 10 + "px")
          .text(d.text);
      })
      .on("mousemove", (event) => {
        if (tooltip) {
          tooltip
            .style("top", event.clientY - 10 + "px")
            .style("left", event.clientX + 10 + "px");
        }
      })
      .on("mouseleave", (event, d) => {
        d3.select(event.currentTarget)
          .select("circle")
          .attr("r", this.getNodeRadius(d.z));
        if (tooltip) {
          tooltip.remove();
          tooltip = null;
        }
      });

  }

}

// Initialize on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  const containers = document.querySelectorAll(".visualization");
  containers.forEach((container) => {
    const pageId = container.dataset.pageId;
    if (!pageId) return;

    const viz = new EmbeddingVisualization(container, pageId);
    viz.init();
  });
});
