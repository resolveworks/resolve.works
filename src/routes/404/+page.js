// Emit build/404.html (not build/404/index.html) so nginx can serve it as an
// error_page. Overrides the global `trailingSlash = 'always'` from the layout.
export const trailingSlash = 'never';
