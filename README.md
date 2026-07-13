# Pet Insurance Comparison Guide

This is a blazing-fast, static, SEO-optimized, and AdSense-ready website tailored for the pet insurance niche (specifically breed-specific guides).

## Architecture
The site is built completely statically using a custom Python script (`_src/generate_site.py`). This script reads templates and JSON data, then outputs the final HTML directly into the root folder.
This enables deploying directly to cPanel via Git with zero server-side rendering required, easily handling 10,000+ daily visitors via static caching.

## How to Add New Articles
1. Open `_src/_data/articles.json`.
2. Add a new JSON object to the array with the following structure:
   ```json
   {
       "id": 100,
       "title": "New Article Title",
       "slug": "new-article-slug",
       "breed": "Breed Name",
       "meta_description": "...",
       "category": "Small Breeds",
       "author": "Author Name",
       "publish_date": "2026-07-13T00:00:00Z",
       "content": "Markdown content goes here..."
   }
   ```
3. Run the generator: `cd _src && python generate_site.py`.
4. The script will automatically generate the new `new-article-slug.html` and update the sitemap, RSS feed, search index, and home page lists.

## How to Update AdSense
1. Open `_src/_data/site.json`.
2. Replace the `"adsense_client_id": "ca-pub-0000000000000000"` with your real Publisher ID.
3. If you want to modify specific Ad Slots (e.g., Above the Fold, Mid-Article, Sidebar), edit the `data-ad-slot` values in:
   - `_src/_templates/index.html` (Above the Fold)
   - `_src/_templates/article.html` (Mid-Article, End of Article, Sidebar)
   - `_src/_templates/category.html` (Above the Fold)
4. Re-run `cd _src && python generate_site.py`.

## Connecting the Newsletter
The newsletter forms are currently placeholders with `action="#"`.
To connect them to a provider (like Mailchimp, ConvertKit, etc.):
1. Edit `_src/_templates/base.html` (Footer Newsletter).
2. Edit `_src/_templates/article.html` (Inline Newsletter).
3. Update the `<form action="...">` to point to your provider's endpoint, and ensure the input fields have the correct `name` attributes (e.g., `name="EMAIL"`).
4. Re-run the generator.

## Git / cPanel Deployment
Simply commit everything (including the generated `.html` files in the root) and push to the branch connected to your cPanel Git Version Control.
cPanel is configured to serve the root directory directly, so no `.cpanel.yml` or manual file moves are needed!

## Service Worker (PWA)
The site includes a `sw.js` and `manifest.json`. It caches all assets (CSS, JS, Manifest) for offline viewing and instant repeat loads. 
To modify the cache strategy, edit `_src/_assets/sw.js` and re-run the generator.
