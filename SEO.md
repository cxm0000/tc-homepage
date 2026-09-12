# Search and AI discovery

Canonical production homepage: https://tangcai.se/

The homepage is static HTML: company details, app descriptions, and links work without JavaScript. Inline JSON-LD connects the Organization, WebSite, WebPage, app list, and five SoftwareApplication entities. App metadata describes visible content; no prices, ratings, or release availability are invented. Personal details are excluded.

`robots.txt` allows public crawlers and advertises `sitemap.xml`. This also allows training crawlers under the existing unrestricted policy; no bot-specific restrictions are introduced. Robots rules are advisory and do not override CDN/firewall rules.

`llms.txt` is a supplementary plain-text company and product directory. It does not guarantee agent usage or improve Google rankings. Maintain it alongside visible copy and JSON-LD. Google does not require AI-specific markup: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

## Verification

Run `python3 scripts/check-seo.py` from the project root after editing content or URLs. It checks metadata, JSON-LD references, all five product links, image paths, section anchors, sitemap URLs, and robots access.

## Publication

The production site was still serving the older homepage during this update. These local changes are not yet live.

Deploy `index.html`, `styles.css`, `logo.png`, `assets/`, `robots.txt`, `sitemap.xml`, and `llms.txt`. Do not publish workspace files, scripts, or this document. Serve XML as `application/xml` and TXT as `text/plain; charset=utf-8`. Invalidate affected CloudFront paths after updating the S3 origin.

After deployment:
- Verify the canonical hostname uses HTTPS; redirect alternate hosts and `/index.html` to `https://tangcai.se/` at the host/CDN if applicable.
- Check that the homepage, linked assets, robots, and sitemap return 200 with no `X-Robots-Tag: noindex`. Missing URLs should return a real 404.
- Validate published structured data with Schema.org Validator. SoftwareApplication markup here is descriptive, not a claim of eligibility for Google's software rich results (no fabricated ratings or offers).
- Verify domain ownership in Google Search Console and Bing Webmaster Tools, submit the sitemap, and inspect the homepage. Reuse an existing verified property.
- Check mobile Core Web Vitals using production traffic or PageSpeed Insights. Local rendering alone does not verify production performance, indexing, rankings, or AI citations.
