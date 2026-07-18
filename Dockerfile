# syntax=docker/dockerfile:1
#
# Fully static site: build the prerendered HTML/assets with SvelteKit, then
# serve the `build/` output with nginx. No database, no Python, no runtime.

# --- build stage: SvelteKit static export ------------------------------------
FROM node:22-alpine AS build
RUN corepack enable
WORKDIR /app

# Install deps first (cached layer) using the exact pnpm version pinned in
# package.json via corepack.
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Build the static site into /app/build
COPY . .
RUN pnpm build

# --- runtime stage: nginx serves the static files ----------------------------
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
