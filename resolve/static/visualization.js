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
    this.padding = 40;
    this.minRadius = 8;
    this.maxRadius = 20;
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
      const response = await fetch(`/api/articles/${this.pageId}/embeddings/`);
      if (!response.ok) return;
      const data = await response.json();
      this.nodes = data.nodes || [];
      this.edges = data.edges || [];
    } catch (e) {
      console.warn("Failed to load embedding data:", e);
    }
  }

  getNodeRadius(z) {
    // Map z (0-1) to radius range
    return this.minRadius + z * (this.maxRadius - this.minRadius);
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
      .attr("stroke", "#D5D5D5")
      .attr("stroke-width", (d) => d.similarity * 2)
      .attr("stroke-opacity", (d) => 0.2 + d.similarity * 0.4);

    // Draw nodes
    const nodeGroups = g
      .selectAll("g.node")
      .data(this.nodes)
      .enter()
      .append("g")
      .attr("class", "node")
      .attr("transform", (d) => `translate(${xScale(d.x)}, ${yScale(d.y)})`);

    // Node circles with z-based radius
    nodeGroups
      .append("circle")
      .attr("r", (d) => this.getNodeRadius(d.z))
      .attr("fill", (d) => this.getNodeColor(d.position))
      .attr("stroke", "#fff")
      .attr("stroke-width", 2)
      .style("cursor", "pointer");

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
          .attr("class", "embedding-tooltip")
          .style("position", "fixed")
          .style("background", "rgba(0, 0, 0, 0.8)")
          .style("color", "#fff")
          .style("padding", "8px 12px")
          .style("border-radius", "4px")
          .style("font-size", "12px")
          .style("max-width", "250px")
          .style("pointer-events", "none")
          .style("z-index", "1000")
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

    // Animate nodes fading in
    nodeGroups.style("opacity", 0).transition().duration(500).style("opacity", 1);
  }

}

// Initialize on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".visualization");
  if (!container) return;

  const pageId = container.dataset.pageId;
  if (!pageId) return;

  const viz = new EmbeddingVisualization(container, pageId);
  viz.init();
});
